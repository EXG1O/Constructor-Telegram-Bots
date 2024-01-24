from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from user.models import User

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandMessageText,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotVariable,
	TelegramBotUser,
)

import json


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()
		self.user: User = User.objects.create(
			telegram_id=123456789,
			first_name='exg1o',
		)
		self.token: Token = Token.objects.create(user=self.user)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.user,
			api_token='Hi!',
		)

class TelegramBotsAPIViewTests(CustomTestCase):
	url: str = reverse('api:telegram-bots:index')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.post(self.url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post( # type: ignore [no-redef]
			self.url,
			{
				'api_token': 'Hi!',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post( # type: ignore [no-redef]
			self.url,
			{
				'api_token': 'Bye!',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 201)

class TelegramBotAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:index',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:index',
			kwargs={'telegram_bot_id': 0},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.post(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.post(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=start') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=stop') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.patch(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.patch(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch( # type: ignore [no-redef]
			self.true_url,
			{'api_token': '...'},
			format='json',
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch( # type: ignore [no-redef]
			self.true_url,
			{'is_private': True},
			format='json',
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch( # type: ignore [no-redef]
			self.true_url,
			{
				'api_token': '...',
				'is_private': True,
			},
			format='json',
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.delete(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.delete(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandsAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:commands',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:commands',
			kwargs={'telegram_bot_id': 0},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.post(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.post(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post( # type: ignore [no-redef]
			self.true_url,
			{
				'data': json.dumps({
					'name': 'Test name',
					'settings': {
						'is_reply_to_user_message': False,
						'is_delete_user_message': False,
						'is_send_as_new_message': False,
					},
					'message_text': {
						'text': 'The test message :)',
					},
				}),
			},
		)
		self.assertEqual(response.status_code, 201)

class TelegramBotCommandAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_command = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name',
		)
		TelegramBotCommandMessageText.objects.create(
			telegram_bot_command=self.telegram_bot_command,
			text='...',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_command_id': self.telegram_bot_command.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': 0,
				'telegram_bot_command_id': self.telegram_bot_command.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_command_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.get(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.patch(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.patch(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.patch( # type: ignore [no-redef]
			self.true_url,
			{
				'data': json.dumps({
					'name': 'Test name',
					'settings': {
						'is_reply_to_user_message': False,
						'is_delete_user_message': False,
						'is_send_as_new_message': False,
					},
					'message_text': {
						'text': 'The test message :)',
					},
				}),
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.delete(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.delete(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandsDiagramAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:commands',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:diagram:commands',
			kwargs={'telegram_bot_id': 0},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandDiagramAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_command_1: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 1',
		)
		TelegramBotCommandMessageText.objects.create(
			telegram_bot_command=self.telegram_bot_command_1,
			text='...',
		)
		self.telegram_bot_command_keyboard_1: TelegramBotCommandKeyboard = TelegramBotCommandKeyboard.objects.create(telegram_bot_command=self.telegram_bot_command_1)
		self.telegram_bot_command_keyboard_button_1: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create(
			telegram_bot_command_keyboard=self.telegram_bot_command_keyboard_1,
			text='Button',
		)

		self.telegram_bot_command_2: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 2',
		)
		TelegramBotCommandMessageText.objects.create(
			telegram_bot_command=self.telegram_bot_command_2,
			text='...',
		)
		self.telegram_bot_command_keyboard_2: TelegramBotCommandKeyboard = TelegramBotCommandKeyboard.objects.create(telegram_bot_command=self.telegram_bot_command_2)
		self.telegram_bot_command_keyboard_button_2: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create(
			telegram_bot_command_keyboard=self.telegram_bot_command_keyboard_2,
			text='Button',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_command_id': self.telegram_bot_command_1.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': 0,
				'telegram_bot_command_id': self.telegram_bot_command_1.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_command_id': 0,
			}
		)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.post(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.post(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post( # type: ignore [no-redef]
			self.true_url,
			{
				'telegram_bot_command_keyboard_button_id': self.telegram_bot_command_keyboard_button_1.id,
				'telegram_bot_command_id': self.telegram_bot_command_2.id,
				'start_diagram_connector': 'start',
				'end_diagram_connector': 'end',
			}
		)
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.patch(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.patch(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.patch(self.true_url, {'x': 150, 'y': 300}) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.delete(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.delete(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.delete( # type: ignore [no-redef]
			self.true_url,
			{'telegram_bot_command_keyboard_button_id': self.telegram_bot_command_keyboard_button_1.id},
		)
		self.assertEqual(response.status_code, 200)

class TelegramBotVariablesAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:variables',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:variables',
			kwargs={'telegram_bot_id': 0}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.post(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.post(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post( # type: ignore [no-redef]
			self.true_url,
			{
				'name': 'Test name',
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 201)

class TelegramBotVariableAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_variable: TelegramBotVariable = TelegramBotVariable.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name',
			value='The test value :)',
			description='The test variable',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_variable_id': self.telegram_bot_variable.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': 0,
				'telegram_bot_variable_id': self.telegram_bot_variable.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_variable_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.get(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.patch(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.patch(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.patch( # type: ignore [no-redef]
			self.true_url,
			{
				'name': 'Test name',
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.delete(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.delete(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

class TelegramBotUsersAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:users',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:users',
			kwargs={'telegram_bot_id': 0}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response: HttpResponse = self.client.get(self.false_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

class TelegramBotUserAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.telegram_bot_user = TelegramBotUser.objects.create(
			telegram_bot=self.telegram_bot,
			telegram_id=123456789,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_user_id': self.telegram_bot_user.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': 0,
				'telegram_bot_user_id': self.telegram_bot_user.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'telegram_bot_user_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.get(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.get(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.post(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.post(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 400)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=allow') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=unallow') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=block') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.post(f'{self.true_url}?action=unblock') # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response: HttpResponse = self.client.delete(url) # type: ignore [no-redef]
			self.assertEqual(response.status_code, 403)

		response: HttpResponse = self.client.delete(self.true_url) # type: ignore [no-redef]
		self.assertEqual(response.status_code, 200)