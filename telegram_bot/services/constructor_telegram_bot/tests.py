from ..core import BaseTestCase
from .telegram_bot import ConstructorTelegramBot

from aiogram.types import InlineKeyboardMarkup
from aiogram.methods import TelegramMethod, SendMessage

from asgiref.sync import async_to_sync


class ConstructorTelegramBotTests(BaseTestCase):
	def setUp(self) -> None: # type: ignore [override]
		constructor_telegram_bot = ConstructorTelegramBot(api_token='123456789:qwertyuiop')
		async_to_sync(constructor_telegram_bot.setup)()

		super().setUp(constructor_telegram_bot.bot, constructor_telegram_bot.dispatcher)

	async def test_start_command_handler(self) -> None:
		methods: list[TelegramMethod] | None = await self.send_message('/start')

		assert methods

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text

	async def test_login_command_handler(self) -> None:
		methods: list[TelegramMethod] | None = await self.send_message('/login')

		assert methods

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text

		assert isinstance(method.reply_markup, InlineKeyboardMarkup)
		assert method.reply_markup.inline_keyboard[0][0].text
		assert method.reply_markup.inline_keyboard[0][0].url
