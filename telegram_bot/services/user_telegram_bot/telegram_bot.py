from ..core import Bot as BaseBot

from aiogram import Dispatcher
from aiogram.types import (
	Chat,
	User as AiogramUser,
	Message,
	CallbackQuery,
	FSInputFile,
	InputMediaPhoto,
	InputMediaDocument,
	BotCommand,
	ReplyKeyboardMarkup,
	InlineKeyboardMarkup,
)
from aiogram.methods import (
	TelegramMethod,
	SendMediaGroup,
	SendPhoto,
	SendDocument,
	SendMessage,
)
from aiogram.utils.backoff import BackoffConfig
from aiogram.exceptions import (
	TelegramRetryAfter,
	TelegramForbiddenError,
	TelegramNotFound,
)

from ...models import (
	TelegramBot as DjangoTelegramBot,
	TelegramBotCommand as DjangoTelegramBotCommand,
	TelegramBotCommandSettings as DjangoTelegramBotCommandSettings,
	TelegramBotCommandCommand as DjangoTelegramBotCommandCommand,
)
from .middlewares import (
	CreateDjangoTelegramBotUserMiddleware,
	CheckDjangoTelegramBotUserPermissionsMiddleware,
	SearchDjangoTelegramBotCommandMiddleware,
	GenerateMessageTextMiddleware,
	GenerateKeyboardMiddleware,
)

from typing import TypeVar, Literal, Callable, Awaitable, Any
from asgiref.sync import sync_to_async
import asyncio
import string
import re


T = TypeVar('T')


class Bot(BaseBot):
	def __init__(self, api_token: str, parse_mode: str | None = None, *args: Any, **kwargs: Any) -> None:
		super().__init__(api_token, parse_mode, *args, **kwargs)

		self.last_messages: dict[int, list[Message]] = {}

	async def __call__(self, method: TelegramMethod[T], *args: Any, **kwargs: Any) -> T | None: # type: ignore [override]
		result: T | None = await super().__call__(method, *args, **kwargs) # type: ignore [arg-type]

		if result:
			if isinstance(result, list):
				for instance in result:
					if isinstance(instance, Message):
						self.last_messages.setdefault(instance.chat.id, []).append(instance)
			elif isinstance(result, Message):
				self.last_messages.setdefault(result.chat.id, []).append(result)

		return result # type: ignore [return-value]

	async def get_chat_last_messages(self, chat_id: int) -> list[Message]:
		return self.last_messages.setdefault(chat_id, [])

class UserTelegramBot:
	def __init__(self, django_telegram_bot: DjangoTelegramBot) -> None:
		self.django_telegram_bot = django_telegram_bot
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = Bot(django_telegram_bot.api_token, 'html')
		self.dispatcher = Dispatcher()

	async def send_message(
		self,
		event: Message,
		event_chat: Chat,
		event_from_user: AiogramUser,
		django_telegram_bot_command: DjangoTelegramBotCommand,
		message_text: str,
		keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
		**kwargs: Any,
	) -> None:
		last_bot_messages: list[Message] = await self.bot.get_chat_last_messages(event_chat.id)
		method_type: Literal['answer', 'reply'] = 'answer'
		settings: DjangoTelegramBotCommandSettings | None = None
		images: list[InputMediaPhoto] = []
		files: list[InputMediaDocument] = []
		message_is_sent = False

		try:
			settings = await sync_to_async(lambda: django_telegram_bot_command.settings)()
		except DjangoTelegramBotCommandSettings.DoesNotExist:
			pass

		if settings and settings.is_reply_to_user_message:
			method_type = 'reply'

		send_media_group: Callable[..., Awaitable[SendMediaGroup]] = getattr(event, f'{method_type}_media_group')
		send_photo: Callable[..., Awaitable[SendPhoto]] = getattr(event, f'{method_type}_photo')
		send_document: Callable[..., Awaitable[SendDocument]] = getattr(event, f'{method_type}_document')
		send_message: Callable[..., Awaitable[SendMessage]] = getattr(event, method_type)

		async for image in django_telegram_bot_command.images.all():
			images.append(InputMediaPhoto(media=FSInputFile(image.image.path)))

		async for file in django_telegram_bot_command.files.all():
			files.append(InputMediaDocument(media=FSInputFile(file.file.path)))

		async def delete_last_bot_message(message: Message) -> None:
			try:
				await last_bot_message.delete()
			except TelegramRetryAfter as exception:
				await asyncio.sleep(exception.retry_after)
				await delete_last_bot_message(message)
			except (TelegramNotFound, TelegramForbiddenError):
				pass

		if not settings or settings and not settings.is_send_as_new_message:
			for last_bot_message in last_bot_messages:
				await delete_last_bot_message(last_bot_message)

		last_bot_messages.clear()

		try:
			if images and files:
				await send_media_group(images)
				await send_media_group(files)
			elif images:
				if len(images) == 1:
					await send_photo(
						images[0].media,
						message_text,
						reply_markup=keyboard,
					)

					message_is_sent = True
				else:
					await send_media_group(images)
			elif files:
				if len(files) == 1:
					await send_document(
						files[0].media,
						caption=message_text,
						reply_markup=keyboard,
					)

					message_is_sent = True
				else:
					await send_media_group(files)

			if not message_is_sent:
				await send_message(message_text, reply_markup=keyboard)

			if not event_from_user.is_bot and settings and settings.is_delete_user_message:
				await event.delete()
		except TelegramRetryAfter as exception:
			await asyncio.sleep(exception.retry_after)
			await self.send_message(
				event,
				event_chat,
				event_from_user,
				django_telegram_bot_command,
				message_text,
				keyboard,
			)
		except (TelegramNotFound, TelegramForbiddenError):
			pass

	async def message_handler(self, event: Message, **kwargs: Any) -> None:
		await self.send_message(event, **kwargs)

	async def callback_query_handler(self, event: CallbackQuery, **kwargs: Any) -> None:
		if event.message:
			await self.send_message(event.message, **kwargs)

	async def setup(self) -> None:
		commands: list[BotCommand] = []

		async for django_telegram_bot_command in self.django_telegram_bot.commands.all():
			try:
				django_telegram_bot_command_command: DjangoTelegramBotCommandCommand | None = await sync_to_async(lambda: django_telegram_bot_command.command)()

				if (
					django_telegram_bot_command_command and
					django_telegram_bot_command_command.description
				):
					commands.append(
						BotCommand(
							command=re.sub(f'[{string.punctuation}]', '', django_telegram_bot_command_command.text),
							description=django_telegram_bot_command_command.description,
						)
					)
			except DjangoTelegramBotCommandCommand.DoesNotExist:
				pass

		await self.bot.set_my_commands(commands)

		self.dispatcher.update.outer_middleware.register(CreateDjangoTelegramBotUserMiddleware(self.django_telegram_bot))
		self.dispatcher.update.outer_middleware.register(CheckDjangoTelegramBotUserPermissionsMiddleware(self.django_telegram_bot))
		self.dispatcher.update.outer_middleware.register(SearchDjangoTelegramBotCommandMiddleware(self.django_telegram_bot))
		self.dispatcher.update.outer_middleware.register(GenerateMessageTextMiddleware(self.django_telegram_bot))
		self.dispatcher.update.outer_middleware.register(GenerateKeyboardMiddleware(self.django_telegram_bot))

		self.dispatcher.message.register(self.message_handler)
		self.dispatcher.callback_query.register(self.callback_query_handler)

	async def start(self) -> None:
		self.loop.create_task(self.stop())

		await self.setup()
		await self.dispatcher.start_polling(
			self.bot,
			backoff_config=BackoffConfig(
				min_delay=1,
				max_delay=3600,
				factor=2.5,
				jitter=0.1,
			),
			handle_signals=False,
		)

		self.django_telegram_bot.is_stopped = True
		await self.django_telegram_bot.asave()

	async def stop(self) -> None:
		while self.django_telegram_bot.is_running:
			try:
				await self.django_telegram_bot.arefresh_from_db()
			except DjangoTelegramBot.DoesNotExist:
				break

			await asyncio.sleep(15)

		await self.dispatcher.stop_polling()