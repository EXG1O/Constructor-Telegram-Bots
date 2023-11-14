from django.test import TestCase, Client

from user.models import User
from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser,
)


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='123456789:qwertyuiop',
			is_private=True,
		)
		self.telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
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
						'row': 1,
						'text': '1',
						'url': None,
					},
					{
						'row': 1,
						'text': '2',
						'url': 'http://example.com/',
					},
				],
			},
			api_request={
				'url': 'http://example.com/',
				'method': 'get',
				'headers': None,
				'data': None,
			},
			database_record={'key': 'value'},
		)
		self.telegram_bot_user: TelegramBotUser = TelegramBotUser.objects.create(
			telegram_bot=self.telegram_bot,
			user_id=123456789,
			full_name='Test user',
		)

		self.base_headers = {'Authorization': f'Token {self.user.auth_token.key}'}

class TelegramBotModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot.owner, self.user)
		self.assertEqual(self.telegram_bot.username, '123456789_test_telegram_bot')
		self.assertEqual(self.telegram_bot.api_token, '123456789:qwertyuiop')
		self.assertTrue(self.telegram_bot.is_private)
		self.assertFalse(self.telegram_bot.is_running)
		self.assertTrue(self.telegram_bot.is_stopped)

class TelegramBotCommandModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.name, 'Test')
		self.assertEqual(self.telegram_bot_command.image, None)
		self.assertDictEqual(self.telegram_bot_command.database_record, {'key': 'value'})
		self.assertEqual(self.telegram_bot_command.x, 0)
		self.assertEqual(self.telegram_bot_command.y, 0)

	def test_get_command(self) -> None:
		self.assertEqual(self.telegram_bot_command.get_command(), self.telegram_bot_command.command)

	def test_get_keyboard(self) -> None:
		self.assertEqual(self.telegram_bot_command.get_keyboard(), self.telegram_bot_command.keyboard)

	def test_get_api_request(self) -> None:
		self.assertEqual(self.telegram_bot_command.get_api_request(), self.telegram_bot_command.api_request)

class TelegramBotCommandCommandModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.command.text, '/test')
		self.assertFalse(self.telegram_bot_command.command.is_show_in_menu)
		self.assertIsNone(self.telegram_bot_command.command.description)

class TelegramBotCommandMessageTextModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.message_text.text, 'Test...')

class TelegramBotCommandKeyboardModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.keyboard.mode, 'default')

class TelegramBotCommandKeyboardButtonModelTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = self.telegram_bot_command.keyboard.buttons.all()[0]

	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command_keyboard_button.row, 1)
		self.assertEqual(self.telegram_bot_command_keyboard_button.text, '1')
		self.assertIsNone(self.telegram_bot_command_keyboard_button.url)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.telegram_bot_command)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.start_diagram_connector)
		self.assertIsNone(self.telegram_bot_command_keyboard_button.end_diagram_connector)

class TelegramBotCommandApiRequestModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_command.api_request.url, 'http://example.com/')
		self.assertEqual(self.telegram_bot_command.api_request.method, 'get')
		self.assertIsNone(self.telegram_bot_command.api_request.headers)
		self.assertIsNone(self.telegram_bot_command.api_request.data)

class TelegramBotUserModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.telegram_bot_user.user_id, 123456789)
		self.assertEqual(self.telegram_bot_user.full_name, 'Test user')
		self.assertEqual(self.telegram_bot_user.is_allowed, False)
