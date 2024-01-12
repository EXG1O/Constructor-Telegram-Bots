from ..core import Bot

from aiogram import Dispatcher
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from user.models import User as DjangoUser

from .middlewares import CreateDjangoUserMiddleware

from asgiref.sync import sync_to_async
import asyncio


class ConstructorTelegramBot:
	def __init__(self, api_token: str) -> None:
		self.loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

		self.bot = Bot(api_token, 'html')
		self.dispatcher = Dispatcher()

	async def start_command(self, message: Message) -> None:
		await message.reply((
			f'Hello, {message.from_user.full_name}!\n' # type: ignore [union-attr]
			'I am a Telegram bot for Constructor Telegram Bots site.\n'
			'Thank you for being with us ❤️'
		))

		try:
			if message.text.split()[1] == 'login': # type: ignore [union-attr]
				await self.login_command(message)
		except IndexError:
			pass

	async def login_command(self, message: Message) -> None:
		django_user: DjangoUser = await DjangoUser.objects.aget(telegram_id=message.from_user.id) # type: ignore [union-attr]

		await message.reply(
			'Click on the button below to login on the site.',
			reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
				InlineKeyboardButton(text='Login', url=await sync_to_async(lambda: django_user.login_url)()),
			]])
		)

	async def setup(self) -> None:
		await self.bot.set_my_commands([
			BotCommand(command='start', description='Starting command'),
			BotCommand(command='login', description='Authorization'),
		])

		self.dispatcher.update.outer_middleware.register(CreateDjangoUserMiddleware())

		self.dispatcher.message.register(self.start_command, Command('start'))
		self.dispatcher.message.register(self.login_command, Command('login'))

	async def start(self) -> None:
		await self.setup()
		await self.dispatcher.start_polling(self.bot, handle_signals=False)
