from aiogram import Bot as Bot_, Dispatcher
from aiogram.types import Chat, User, Update, Message, CallbackQuery
from aiogram.methods import TelegramMethod, SetMyCommands

from django.test import TestCase
from django.conf import settings

from typing import TypeVar, Any
from datetime import datetime
import asyncio


T = TypeVar('T')


class Bot(Bot_):
	def __init__(self, api_token: str, parse_mode: str | None = None, *args: Any, **kwargs: Any) -> None:
		super().__init__(api_token, parse_mode=parse_mode, *args, **kwargs) # type: ignore [misc]

		self.call_results: list[TelegramMethod[Any]] = []

	async def __call__(self, method: TelegramMethod[T], *args: Any, **kwargs: Any) -> T | None: # type: ignore [override, return]
		if not isinstance(method, SetMyCommands):
			self.call_results.append(method)

		if not settings.TEST:
			return await super().__call__(method, *args, **kwargs) # type: ignore [arg-type]

class BaseTelegramBot:
	def __init__(self, api_token: str, parse_mode: str | None = None) -> None:
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = Bot(api_token, parse_mode)
		self.dispatcher = Dispatcher()

class BaseTestCase(TestCase):
	chat_ = Chat(id=1, type='private')
	user_ = User(id=1, first_name='Test', username='test', is_bot=False)

	def setUp(self, bot: Bot, dispatcher: Dispatcher): # type: ignore [override]
		self.bot = bot
		self.dispatcher = dispatcher

	async def send_message(self, text: str) -> list[TelegramMethod[Any]] | None:
		await self.dispatcher._process_update(self.bot, Update(
			update_id=1,
			message=Message(
				message_id=1,
				text=text,
				chat=self.chat_,
				from_user=self.user_,
				date=datetime.now(),
			),
		))

		return self.bot.call_results

	async def send_callback_query(self, data: str) -> list[TelegramMethod[Any]] | None:
		await self.dispatcher._process_update(self.bot, Update(
			update_id=1,
			callback_query=CallbackQuery(
				id='1',
				chat_instance=str(self.chat_.id),
				from_user=self.user_,
				message=Message(
					message_id=1,
					text='Test',
					chat=self.chat_,
					from_user=self.user_,
					date=datetime.now(),
				),
				data=data,
			),
		))

		return self.bot.call_results