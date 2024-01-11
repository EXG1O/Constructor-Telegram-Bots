from django.utils import timezone

from aiogram import BaseMiddleware
from aiogram.types import (
	Update,
	Message,
	CallbackQuery,
	User as AiogramUser,
	ReplyKeyboardMarkup,
	InlineKeyboardMarkup,
	KeyboardButton,
	InlineKeyboardButton,
)

from ...models import (
	TelegramBot as DjangoTelegramBot,
	TelegramBotCommand as DjangoTelegramBotCommand,
	TelegramBotCommandCommand as DjangoTelegramBotCommandCommand,
	TelegramBotCommandKeyboard as DjangoTelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton as DjangoTelegramBotCommandKeyboardButton,
	TelegramBotUser as DjangoTelegramBotUser,
)
from ..typing import Handler

from typing import Any, TypeVar, Generic, Callable, Awaitable
from asgiref.sync import sync_to_async


T = TypeVar('T')


class CustomBaseMiddleware(BaseMiddleware):
	def __init__(self, django_telegram_bot: DjangoTelegramBot) -> None:
		self.django_telegram_bot = django_telegram_bot

class CreateDjangoTelegramBotUserMiddleware(CustomBaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any: # type: ignore [override]
		aiogram_user: AiogramUser | None = data.get('event_from_user')

		if aiogram_user:
			django_telegram_bot_user, created = await DjangoTelegramBotUser.objects.aget_or_create(
				telegram_bot=self.django_telegram_bot,
				telegram_id=aiogram_user.id,
				defaults={'full_name': aiogram_user.full_name}
			)

			if not created:
				django_telegram_bot_user.last_activity_date = timezone.now()
				django_telegram_bot_user.save()

			data['django_telegram_bot_user'] = django_telegram_bot_user

			return await handler(event, data)

class CheckDjangoTelegramBotUserPermissionsMiddleware(CustomBaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any: # type: ignore [override]
		django_telegram_bot_user: DjangoTelegramBotUser = data['django_telegram_bot_user']

		match (
			self.django_telegram_bot.is_private,
			django_telegram_bot_user.is_allowed,
			django_telegram_bot_user.is_blocked,
		):
			case (True, True, False) | (False, _, False):
				return await handler(event, data)

class SearchDjangoTelegramBotCommandMiddleware(CustomBaseMiddleware):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		self.message_event = self.MessageEvent(self.django_telegram_bot)
		self.callback_query_event = self.CallbackQueryEvent(self.django_telegram_bot)

	class Base(Generic[T]):
		def __init__(self, django_telegram_bot: DjangoTelegramBot) -> None:
			self.django_telegram_bot = django_telegram_bot
			self.event: T | None = None
			self.data: dict[str, Any] | None = None

	class MessageEvent(Base[Message]):
		async def get_search_methods(self) -> list[Callable[[], Awaitable[DjangoTelegramBotCommand | None]]]:
			return [self.search_via_command, self.search_via_keyboard]

		async def search_via_command(self) -> DjangoTelegramBotCommand | None:
			if self.event and self.event.text:
				async for django_telegram_bot_command in self.django_telegram_bot.commands.all():
					try:
						django_telegram_bot_command_command: DjangoTelegramBotCommandCommand = await sync_to_async(lambda: django_telegram_bot_command.command)()

						if django_telegram_bot_command_command.text == self.event.text:
							return django_telegram_bot_command
					except DjangoTelegramBotCommandCommand.DoesNotExist:
						pass

			return None

		async def search_via_keyboard(self) -> DjangoTelegramBotCommand | None:
			if self.event and self.event.text:
				async for django_telegram_bot_command in self.django_telegram_bot.commands.all():
					try:
						django_telegram_bot_command_keyboard: DjangoTelegramBotCommandKeyboard = await sync_to_async(lambda: django_telegram_bot_command.keyboard)()

						if django_telegram_bot_command_keyboard.type == 'default':
							async for django_telegram_bot_command_keyboard_button in django_telegram_bot_command_keyboard.buttons.all():
								if django_telegram_bot_command_keyboard_button.text == self.event.text:
									return await sync_to_async(lambda: django_telegram_bot_command_keyboard_button.telegram_bot_command)()
					except DjangoTelegramBotCommandKeyboard.DoesNotExist:
						pass

			return None

	class CallbackQueryEvent(Base[CallbackQuery]):
		async def get_search_methods(self) -> list[Callable[[], Awaitable[DjangoTelegramBotCommand | None]]]:
			return [self.search_via_keyboard]

		async def search_via_keyboard(self) -> DjangoTelegramBotCommand | None:
			if self.event and self.event.data:
				try:
					django_telegram_bot_command_keyboard_button: DjangoTelegramBotCommandKeyboardButton = await DjangoTelegramBotCommandKeyboardButton.objects.aget(id=int(self.event.data))

					return await sync_to_async(lambda: django_telegram_bot_command_keyboard_button.telegram_bot_command)()
				except DjangoTelegramBotCommandKeyboardButton.DoesNotExist:
					pass

			return None

	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any: # type: ignore [override]
		search_methods: list[Callable[[], Awaitable[DjangoTelegramBotCommand | None]]] = []

		if isinstance(event.event, Message):
			self.message_event.event = event.event
			self.message_event.data = data

			search_methods = await self.message_event.get_search_methods()
		elif isinstance(event.event, CallbackQuery):
			self.callback_query_event.event = event.event
			self.callback_query_event.data = data

			search_methods = await self.callback_query_event.get_search_methods()

		for search_method in search_methods:
			django_telegram_bot_command: DjangoTelegramBotCommand | None = await search_method()

			if django_telegram_bot_command:
				data['django_telegram_bot_command'] = django_telegram_bot_command

				return await handler(event, data)

class GenerateMessageTextMiddleware(CustomBaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any: # type: ignore [override]
		django_telegram_bot_command: DjangoTelegramBotCommand | None = data.get('django_telegram_bot_command')

		if django_telegram_bot_command:
			try:
				data['message_text'] = await sync_to_async(lambda: django_telegram_bot_command.message_text.text)()

				return await handler(event, data)
			except DjangoTelegramBotCommand.DoesNotExist:
				pass

class GenerateKeyboardMiddleware(CustomBaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any: # type: ignore [override]
		django_telegram_bot_command: DjangoTelegramBotCommand | None = data.get('django_telegram_bot_command')

		if django_telegram_bot_command:
			try:
				django_telegram_bot_command_keyboard: DjangoTelegramBotCommandKeyboard = await sync_to_async(lambda: django_telegram_bot_command.keyboard)()

				if django_telegram_bot_command_keyboard:
					keyboard: list[list[KeyboardButton | InlineKeyboardButton]] = [[] for _ in range(await django_telegram_bot_command_keyboard.buttons.acount())]
					keyboard_row = 0

					async for django_telegram_bot_command_keyboard_button in django_telegram_bot_command_keyboard.buttons.all():
						keyboard_row_buttons: list[KeyboardButton | InlineKeyboardButton] | None = None

						if django_telegram_bot_command_keyboard_button.row:
							try:
								keyboard_row_buttons = keyboard[django_telegram_bot_command_keyboard_button.row - 1]
							except IndexError:
								pass

						if keyboard_row_buttons is None:
							keyboard_row_buttons = keyboard[keyboard_row]

						if django_telegram_bot_command_keyboard.type == 'default':
							keyboard_row_buttons.append(KeyboardButton(text=django_telegram_bot_command_keyboard_button.text))
						else:
							keyboard_row_buttons.append(
								InlineKeyboardButton(
									text=django_telegram_bot_command_keyboard_button.text,
									url=django_telegram_bot_command_keyboard_button.url,
									callback_data=str(django_telegram_bot_command_keyboard_button.id),
								)
							)

						keyboard_row += 1

					if django_telegram_bot_command_keyboard.type == 'default':
						data['keyboard'] = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True) # type: ignore [arg-type]
					else:
						data['keyboard'] = InlineKeyboardMarkup(inline_keyboard=keyboard) # type: ignore [arg-type]
			except DjangoTelegramBotCommandKeyboard.DoesNotExist:
				pass

		return await handler(event, data)