from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from aiogram import Bot as BaseBot, Dispatcher
from aiogram.types import Update, Message, CallbackQuery, Chat, User
from aiogram.methods import TelegramMethod, SetMyCommands

from typing import TypeVar, Any


T = TypeVar('T')


class Bot(BaseBot):
	def __init__(self, api_token: str, parse_mode: str | None = None, *args: Any, **kwargs: Any) -> None:
		super().__init__(api_token, parse_mode=parse_mode, *args, **kwargs) # type: ignore [misc]

		self.call_results: list[TelegramMethod] = []

	async def __call__(self, method: TelegramMethod[T], *args: Any, **kwargs: Any) -> T | None: # type: ignore [override, return]
		if settings.TEST:
			if not isinstance(method, SetMyCommands):
				self.call_results.append(method)
		else:
			return await super().__call__(method, *args, **kwargs) # type: ignore [arg-type]

class BaseTestCase(TestCase):
	chat = Chat(id=1, type='private')
	user = User(id=1, first_name='Test', username='test', is_bot=False)

	def setUp(self, bot: Bot, dispatcher: Dispatcher) -> None: # type: ignore [override]
		self.bot = bot
		self.dispatcher = dispatcher

	async def send_message(self, text: str) -> list[TelegramMethod] | None:
		await self.dispatcher._process_update(
			self.bot,
			Update(
				update_id=1,
				message=Message(
					message_id=1,
					text=text,
					chat=self.chat,
					from_user=self.user,
					date=timezone.now(),
				),
			),
		)

		return self.bot.call_results

	async def send_callback_query(self, data: str) -> list[TelegramMethod] | None:
		await self.dispatcher._process_update(
			self.bot,
			Update(
				update_id=1,
				callback_query=CallbackQuery(
					id='1',
					chat_instance=str(self.chat.id),
					from_user=self.user,
					message=Message(
						message_id=1,
						text='Test',
						chat=self.chat,
						from_user=self.user,
						date=timezone.now(),
					),
					data=data,
				),
			),
		)

		return self.bot.call_results