from aiogram import (
	Bot as Bot_,
	Dispatcher,
)
from aiogram.types import Chat, User, Update, Message, CallbackQuery
from aiogram.methods import TelegramMethod, SetMyCommands

from django.test import TestCase
from django.conf import settings

from typing import TypeVar
from datetime import datetime
import asyncio


T = TypeVar('T')


class Bot(Bot_):
	def __init__(self, api_token: str, parse_mode: str | None = None, *args, **kwargs) -> None:
		super().__init__(token=api_token, parse_mode=parse_mode, *args, **kwargs)

		self.call_results = []

	async def __call__(self, method: TelegramMethod[T], *args, **kwargs) -> T | None:
		if not isinstance(method, SetMyCommands):
			self.call_results.append(method)

		if not settings.TEST:
			return await super().__call__(method, *args, **kwargs)

class BaseTelegramBot:
	def __init__(self, api_token: str, parse_mode: str | None = None) -> None:
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = Bot(api_token, parse_mode)
		self.dispatcher = Dispatcher()

class BaseTestCase(TestCase):
	chat_ = Chat(id=1, type='private')
	user_ = User(id=1, first_name='Test', username='test', is_bot=False)

	def setUp(self, bot: Bot, dispatcher: Dispatcher):
		self.bot = bot
		self.dispatcher = dispatcher

	async def send_message(self, text: str) -> list[TelegramMethod] | None:
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

	async def send_callback_query(self, data: str) -> list[TelegramMethod] | None:
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
