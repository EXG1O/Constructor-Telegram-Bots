from aiogram import BaseMiddleware as BaseMiddleware_
from aiogram.types import (
	User as AiogramUser,
	Update,
	Message,
	CallbackQuery,
	ReplyKeyboardMarkup,
	KeyboardButton,
	InlineKeyboardMarkup,
	InlineKeyboardButton,
)

from django.core.exceptions import ObjectDoesNotExist

from constructor_telegram_bots.environment import areplace_text_variables_to_jinja_variables_values

from ...models import (
	TelegramBot as DjangoTelegramBot,
	TelegramBotCommand as DjangoTelegramBotCommand,
	TelegramBotCommandCommand as DjangoTelegramBotCommandCommand,
	TelegramBotCommandMessageText as DjangoTelegramBotCommandMessageText,
	TelegramBotCommandKeyboard as DjangoTelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton as DjangoTelegramBotCommandKeyboardButton,
	TelegramBotCommandApiRequest as DjangoTelegramBotCommandApiRequest,
	TelegramBotUser as DjangoTelegramBotUser,
)

from .. import database_telegram_bot
from ..typing import Handler

from aiohttp import ClientSession
from aiohttp.client_exceptions import InvalidURL, ContentTypeError

from typing import Callable, Awaitable, Any
import json


class BaseMiddleware(BaseMiddleware_):
	def __init__(self, django_telegram_bot: DjangoTelegramBot) -> None:
		self.django_telegram_bot = django_telegram_bot

class CreateDjangoTelegramBotUserMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		event_from_user: AiogramUser = data['event_from_user']

		data['django_telegram_bot_user'] = (await DjangoTelegramBotUser.objects.aget_or_create(
			telegram_bot=self.django_telegram_bot,
			user_id=event_from_user.id,
			defaults={'full_name': event_from_user.full_name},
		))[0]

		return await handler(event, data)

class CheckDjangoTelegramBotUserIsAllowedMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		django_telegram_bot_user: DjangoTelegramBotUser = data['django_telegram_bot_user']

		if not self.django_telegram_bot.is_private or self.django_telegram_bot.is_private and django_telegram_bot_user.is_allowed:
			return await handler(event, data)

class GenerateJinjaVariablesMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		event_from_user: AiogramUser = data['event_from_user']

		if isinstance(event.event, Message):
			user_message_id = event.event.message_id
			user_message_text = event.event.text
		elif isinstance(event.event, CallbackQuery):
			user_message_id = event.event.message.message_id
			user_message_text = event.event.message.text
		else:
			user_message_id = None
			user_message_text = None

		database_records = {}

		for database_record in database_telegram_bot.get_records(self.django_telegram_bot):
			database_records[database_record['_id']] = database_record

		data['jinja_variables'] = {
			'user_id':event_from_user.id,
			'user_username':event_from_user.username,
			'user_first_name':event_from_user.first_name,
			'user_last_name':event_from_user.last_name,
			'user_message_id': user_message_id,
			'user_message_text': user_message_text,
			'database_records': database_records,
		}

		return await handler(event, data)

class SearchDjangoTelegramBotCommandMiddleware(BaseMiddleware):
	class Base:
		def __init__(self, django_telegram_bot: DjangoTelegramBot) -> None:
			self.django_telegram_bot = django_telegram_bot
			self.event = None
			self.data = None

	class MessageEvent(Base):
		async def get_search_methods(self) -> list[Callable[[], Awaitable[DjangoTelegramBotCommand | None]]]:
			return [self.search_via_command, self.search_via_keyboard]

		async def search_via_command(self) -> DjangoTelegramBotCommand | None:
			async for django_telegram_bot_command in self.django_telegram_bot.commands.all():
				django_telegram_bot_command_command: DjangoTelegramBotCommandCommand | None = await django_telegram_bot_command.aget_command()

				if django_telegram_bot_command_command:
					django_telegram_bot_command_command_text: str = await areplace_text_variables_to_jinja_variables_values(
						self.django_telegram_bot,
						django_telegram_bot_command_command.text,
						self.data['jinja_variables'],
					)

					if django_telegram_bot_command_command_text == self.event.text:
						return django_telegram_bot_command

		async def search_via_keyboard(self) -> DjangoTelegramBotCommand | None:
			async for django_telegram_bot_command in self.django_telegram_bot.commands.all():
				django_telegram_bot_command_keyboard: DjangoTelegramBotCommandKeyboard | None = await django_telegram_bot_command.aget_keyboard()

				if django_telegram_bot_command_keyboard and  django_telegram_bot_command_keyboard.mode == 'default':
					async for django_telegram_bot_command_keyboard_button in django_telegram_bot_command_keyboard.buttons.all():
						if django_telegram_bot_command_keyboard_button.text == self.event.text:
							return await django_telegram_bot_command_keyboard_button.aget_telegram_bot_command()

	class CallbackQueryEvent(Base):
		async def get_search_methods(self) -> list[Callable[[], Awaitable[DjangoTelegramBotCommand | None]]]:
			return [self.search_via_keyboard]

		async def search_via_keyboard(self) -> DjangoTelegramBotCommand | None:
			try:
				django_telegram_bot_command_keyboard_button: DjangoTelegramBotCommandKeyboardButton = await DjangoTelegramBotCommandKeyboardButton.objects.aget(id=int(self.event.data))

				return await django_telegram_bot_command_keyboard_button.aget_telegram_bot_command()
			except ObjectDoesNotExist:
				return None

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		args = (self.django_telegram_bot,)

		self.message_event = self.MessageEvent(*args)
		self.callback_query_event = self.CallbackQueryEvent(*args)

	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		if isinstance(event.event, Message):
			self.message_event.event = event.event
			self.message_event.data = data

			search_methods = await self.message_event.get_search_methods()
		elif isinstance(event.event, CallbackQuery):
			self.callback_query_event.event = event.event
			self.callback_query_event.data = data

			search_methods = await self.callback_query_event.get_search_methods()
		else:
			search_methods = []

		for search_method in search_methods:
			django_telegram_bot_command: DjangoTelegramBotCommand | None = await search_method()

			if django_telegram_bot_command:
				data['django_telegram_bot_command'] = django_telegram_bot_command

				return await handler(event, data)

class MakeDjangoTelegramBotCommandApiRequestMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		django_telegram_bot_command: DjangoTelegramBotCommand = data['django_telegram_bot_command']
		django_telegram_bot_command_api_request: DjangoTelegramBotCommandApiRequest | None = await django_telegram_bot_command.aget_api_request()

		if django_telegram_bot_command_api_request:
			jinja_variables: dict[str, Any] = data['jinja_variables']

			method: str = django_telegram_bot_command_api_request.method
			url: str = await areplace_text_variables_to_jinja_variables_values(
				self.django_telegram_bot,
				django_telegram_bot_command_api_request.url,
				jinja_variables,
			)
			headers = None
			json_data = None

			if django_telegram_bot_command_api_request.headers:
				headers: dict = json.loads(await areplace_text_variables_to_jinja_variables_values(
					self.django_telegram_bot,
					django_telegram_bot_command_api_request.headers,
					jinja_variables,
				))

			if django_telegram_bot_command_api_request.data:
				json_data: dict = json.loads(await areplace_text_variables_to_jinja_variables_values(
					self.django_telegram_bot,
					django_telegram_bot_command_api_request.data,
					jinja_variables,
				))

			try:
				async with ClientSession() as session:
					async with session.request(method, url, headers=headers, json=json_data) as response:
						data['jinja_variables']['api_response'] = await response.json()
			except (InvalidURL, ContentTypeError):
				pass

		return await handler(event, data)

class InsertDjangoTelegramBotCommandDatabaseRecordToDatabaseMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		django_telegram_bot_command: DjangoTelegramBotCommand = data['django_telegram_bot_command']
		jinja_variables: dict[str, Any]  = data['jinja_variables']

		if django_telegram_bot_command.database_record:
			django_telegram_bot_command_database_record: dict = json.loads(await areplace_text_variables_to_jinja_variables_values(
				self.django_telegram_bot,
				django_telegram_bot_command.database_record,
				jinja_variables,
			))

			database_telegram_bot.insert_record(self.django_telegram_bot, django_telegram_bot_command_database_record)

		return await handler(event, data)

class GetDjangoTelegramBotCommandMessageTextMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		django_telegram_bot_command: DjangoTelegramBotCommand = data['django_telegram_bot_command']
		django_telegram_bot_command_message_text: DjangoTelegramBotCommandMessageText = await django_telegram_bot_command.aget_message_text()
		jinja_variables: dict[str, Any]  = data['jinja_variables']

		message_text: str = await areplace_text_variables_to_jinja_variables_values(
			self.django_telegram_bot,
			django_telegram_bot_command_message_text.text,
			jinja_variables,
		)

		if message_text and len(message_text) <= 4096:
			data['message_text'] = message_text

			return await handler(event, data)

class GetDjangoTelegramBotCommandKeyboardMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		django_telegram_bot_command: DjangoTelegramBotCommand = data['django_telegram_bot_command']
		django_telegram_bot_command_keyboard: DjangoTelegramBotCommandKeyboard = await django_telegram_bot_command.aget_keyboard()
		keyboard = None

		if django_telegram_bot_command_keyboard:
			keyboard = [[] for _ in range(await django_telegram_bot_command_keyboard.buttons.acount())]
			keyboard_row = 0

			async for django_telegram_bot_command_keyboard_button in django_telegram_bot_command_keyboard.buttons.all():
				if django_telegram_bot_command_keyboard_button.row:
					keyboard_row_buttons: list = keyboard[django_telegram_bot_command_keyboard_button.row - 1]
				else:
					keyboard_row_buttons: list = keyboard[keyboard_row]

				if django_telegram_bot_command_keyboard.mode == 'default':
					keyboard_row_buttons.append(KeyboardButton(text=django_telegram_bot_command_keyboard_button.text))
				else:
					keyboard_row_buttons.append(InlineKeyboardButton(
						text=django_telegram_bot_command_keyboard_button.text,
						url=django_telegram_bot_command_keyboard_button.url,
						callback_data=str(django_telegram_bot_command_keyboard_button.id),
					))

				keyboard_row += 1

			if django_telegram_bot_command_keyboard.mode == 'default':
				keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
			else:
				keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

		data['keyboard'] = keyboard

		return await handler(event, data)
