from ..core import BaseTestCase
from .telegram_bot import ConstructorTelegramBot

from aiogram.methods import TelegramMethod, SendMessage

from user.models import User as DjangoUser


class ConstructorTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		self.constructor_telegram_bot = ConstructorTelegramBot()
		self.constructor_telegram_bot.loop.run_until_complete(self.constructor_telegram_bot.setup())

		super().setUp(self.constructor_telegram_bot.bot, self.constructor_telegram_bot.dispatcher)

	async def test_start_command_handler(self):
		method: TelegramMethod = (await self.send_message('/start'))[0]

		assert isinstance(method, SendMessage)
		assert method.text == (
			'Hello, @test!\n'
			'I am a Telegram bot for Constructor Telegram Bots site.\n'
			'Thank you for being with us ❤️'
		)

	async def test_login_command_handler(self):
		method: TelegramMethod = (await self.send_message('/login'))[0]

		django_user: DjangoUser = await DjangoUser.objects.afirst()
		django_user_login_url: str = await django_user.alogin_url

		assert isinstance(method, SendMessage)
		assert method.text == f'Click on the button below to login on the site or follow this link: {django_user_login_url}.'
		assert method.reply_markup.inline_keyboard[0][0].text == 'Login'
		assert method.reply_markup.inline_keyboard[0][0].url == django_user_login_url
