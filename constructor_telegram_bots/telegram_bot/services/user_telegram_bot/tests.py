from ..core import BaseTestCase
from .telegram_bot import UserTelegramBot

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.methods import TelegramMethod, SendMessage, DeleteMessage

from user.models import User as DjangoUser

from ...models import (
	TelegramBot as DjangoTelegramBot,
	TelegramBotCommand as DjangoTelegramBotCommand,
	TelegramBotCommandKeyboard as DjangoTelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton as DjangoTelegramBotCommandKeyboardButton,
)

from asgiref.sync import async_to_sync


class UserTelegramBotTests(BaseTestCase):
	def setUp(self) -> None:
		django_user: DjangoUser = DjangoUser.objects.create(telegram_id=123456789, first_name='exg1o')
		self.django_telegram_bot: DjangoTelegramBot = DjangoTelegramBot.objects.create(
			owner=django_user,
			api_token='123456789:qwertyuiop',
			is_private=False,
		)

		user_telegram_bot = UserTelegramBot(django_telegram_bot=self.django_telegram_bot)
		async_to_sync(user_telegram_bot.setup)()

		super().setUp(user_telegram_bot.bot, user_telegram_bot.dispatcher)

	async def test_send_command(self) -> None:
		await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={'text': 'Test...'},
			keyboard=None,
			api_request=None,
			database_record=None,
		)

		methods: list[TelegramMethod] | None = await self.send_message('/test')

		assert methods is not None

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text == 'Test...'

	async def test_send_command_with_default_keyboard(self) -> None:
		await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={'text': 'Test...'},
			keyboard={
				'mode': 'default',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': None,
					},
					{
						'row': 2,
						'text': '2',
						'url': None,
					},
					{
						'row': 2,
						'text': '3',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None,
		)

		methods: list[TelegramMethod] | None = await self.send_message('/test')

		assert methods is not None

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text == 'Test...'

		assert isinstance(method.reply_markup, ReplyKeyboardMarkup)
		assert method.reply_markup.keyboard[0][0].text == '1'
		assert method.reply_markup.keyboard[1][0].text == '2'
		assert method.reply_markup.keyboard[1][1].text == '3'

	async def test_send_command_with_inline_keyboard(self) -> None:
		await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={'text': 'Test...'},
			keyboard={
				'mode': 'inline',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': 'https://example.com/',
					},
					{
						'row': 2,
						'text': '2',
						'url': None,
					},
					{
						'row': 2,
						'text': '3',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None,
		)

		methods: list[TelegramMethod] | None = await self.send_message('/test')

		assert methods is not None

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text == 'Test...'

		assert isinstance(method.reply_markup, InlineKeyboardMarkup)
		assert method.reply_markup.inline_keyboard[0][0].text == '1'
		assert method.reply_markup.inline_keyboard[0][0].url == 'https://example.com/'
		assert method.reply_markup.inline_keyboard[1][0].text == '2'
		assert method.reply_markup.inline_keyboard[1][0].url is None
		assert method.reply_markup.inline_keyboard[1][1].text == '3'
		assert method.reply_markup.inline_keyboard[1][1].url is None

	async def test_click_default_keyboard_button(self) -> None:
		django_telegram_bot_command_1: DjangoTelegramBotCommand = await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test1',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={'text': 'Test1...'},
			keyboard={
				'mode': 'default',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None,
		)
		django_telegram_bot_command_2:  DjangoTelegramBotCommand = await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test2',
			command=None,
			image=None,
			message_text={'text': 'Test2...'},
			keyboard=None,
			api_request=None,
			database_record=None,
		)

		django_telegram_bot_command_1_keyboard: DjangoTelegramBotCommandKeyboard = await django_telegram_bot_command_1.aget_keyboard()
		django_telegram_bot_command_1_keyboard_button: DjangoTelegramBotCommandKeyboardButton = await django_telegram_bot_command_1_keyboard.buttons.afirst()
		django_telegram_bot_command_1_keyboard_button.telegram_bot_command = django_telegram_bot_command_2
		await django_telegram_bot_command_1_keyboard_button.asave()

		methods: list[TelegramMethod] | None = await self.send_message('1')

		assert methods is not None

		method: TelegramMethod = methods[0]

		assert isinstance(method, SendMessage)
		assert method.text == 'Test2...'

	async def test_click_inline_keyboard_button(self) -> None:
		django_telegram_bot_command_1: DjangoTelegramBotCommand = await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test1',
			command={
				'text': '/test',
				'is_show_in_menu': False,
				'description': None,
			},
			image=None,
			message_text={'text': 'Test1...'},
			keyboard={
				'mode': 'inline',
				'buttons': [
					{
						'row': None,
						'text': '1',
						'url': None,
					},
				],
			},
			api_request=None,
			database_record=None,
		)
		django_telegram_bot_command_2:  DjangoTelegramBotCommand = await DjangoTelegramBotCommand.objects.acreate(
			telegram_bot=self.django_telegram_bot,
			name='Test2',
			command=None,
			image=None,
			message_text={'text': 'Test2...'},
			keyboard=None,
			api_request=None,
			database_record=None,
		)

		django_telegram_bot_command_1_keyboard: DjangoTelegramBotCommandKeyboard = await django_telegram_bot_command_1.aget_keyboard()
		django_telegram_bot_command_1_keyboard_button: DjangoTelegramBotCommandKeyboardButton = await django_telegram_bot_command_1_keyboard.buttons.afirst()
		django_telegram_bot_command_1_keyboard_button.telegram_bot_command = django_telegram_bot_command_2
		await django_telegram_bot_command_1_keyboard_button.asave()

		methods: list[TelegramMethod] | None = await self.send_callback_query(str(django_telegram_bot_command_1_keyboard_button.id))

		assert methods is not None
		assert isinstance(methods[0], DeleteMessage)
		assert isinstance(methods[1], SendMessage)
		assert methods[1].text == 'Test2...'
