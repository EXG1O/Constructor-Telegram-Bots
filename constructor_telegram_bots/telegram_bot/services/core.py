from aiogram import (
	Bot as Bot_,
	Dispatcher,
)
from aiogram.types import Chat, User, Update, Message, CallbackQuery
from aiogram.methods import TelegramMethod, SetMyCommands

from django.test import TestCase
from django.conf import settings

from typing import Optional, List, Any
from datetime import datetime
import asyncio


class Bot(Bot_):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		if settings.TEST:
			self.results = []

	async def __call__(self, method: TelegramMethod, *args, **kwargs) -> Optional[Any]:
		if settings.TEST:
			if not isinstance(method, SetMyCommands):
				self.results.append(method)
		else:
			return await super().__call__(method, *args, **kwargs)

	async def get_results(self) -> Optional[List[TelegramMethod]]:
		if settings.TEST:
			return self.results

class BaseTelegramBot:
	def __init__(self, api_token: str) -> None:
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = Bot(token=api_token)
		self.dispatcher = Dispatcher()

class BaseTestCase(TestCase):
	chat_ = Chat(id=1, type='private')
	user_ = User(id=1, first_name='Test', username='test', is_bot=False)

	def setUp(self, bot: Bot, dispatcher: Dispatcher):
		self.bot = bot
		self.dispatcher = dispatcher

	async def send_message(self, text: str) -> Optional[List[TelegramMethod]]:
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
		return await self.bot.get_results()

	async def send_callback_query(self, data: str) -> Optional[List[TelegramMethod]]:
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
		return await self.bot.get_results()
