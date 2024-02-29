from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from users.models import User as SiteUser

from .models import (
	TelegramBot,
	Connection,
	CommandMessage,
	CommandKeyboardButton,
	CommandKeyboard,
	Command,
	Variable,
	User,
)

import json


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()
		self.site_user: SiteUser = SiteUser.objects.create(
			telegram_id=123456789,
			first_name='exg1o',
		)
		self.token: Token = Token.objects.create(user=self.site_user)
		self.telegram_bot: TelegramBot = TelegramBot.objects.create(
			owner=self.site_user,
			api_token='Hi!',
		)

class TelegramBotsAPIViewTests(CustomTestCase):
	url: str = reverse('api:telegram-bots:list')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.url, {
			'api_token': 'Hi!',
			'is_private': False,
		})
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.url, {
			'api_token': 'Bye!',
			'is_private': False,
		})
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

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.true_url, data={'action': 'start'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post(self.true_url, data={'action': 'restart'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post(self.true_url, data={'action': 'stop'})
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.patch(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.true_url, {'api_token': '...'})
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.true_url, {'is_private': True})
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.true_url, {
			'api_token': '...',
			'is_private': True,
		})
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.delete(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 200)

class CommandsAPIViewTests(CustomTestCase):
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

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.true_url, {
			'data': json.dumps({
				'name': 'Test name',
				'settings': {
					'is_reply_to_user_message': False,
					'is_delete_user_message': False,
					'is_send_as_new_message': False,
				},
				'message': {
					'text': 'The test message :)',
				},
			}),
		})
		self.assertEqual(response.status_code, 201)

class CommandAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name',
		)
		CommandMessage.objects.create(
			command=self.command,
			text='...',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': self.command.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': 0,
				'command_id': self.command.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.patch(self.true_url, {
			'data': json.dumps({
				'name': 'Test name',
				'settings': {
					'is_reply_to_user_message': False,
					'is_delete_user_message': False,
					'is_send_as_new_message': False,
				},
				'message': {
					'text': 'The test message :)',
				},
			}),
		})
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 200)

class DiagramCommandsAPIViewTests(CustomTestCase):
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

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

class DiagramCommandAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': self.command.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': 0,
				'command_id': self.command.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': 0,
			}
		)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.true_url, {'x': 150, 'y': 300})
		self.assertEqual(response.status_code, 200)

class ConnectionsAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command_1: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 1',
		)
		self.command_2: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 1',
		)
		self.command_2_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
			command=self.command_2,
			type='default',
		)
		self.command_2_keyboard_button: CommandKeyboardButton = CommandKeyboardButton.objects.create(
			keyboard=self.command_2_keyboard,
			text='Button',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:connections',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:diagram:connections',
			kwargs={'telegram_bot_id': 0}
		)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.post(self.true_url, {
			'source_object_type': 'command_keyboard_button',
			'source_object_id': self.command_2_keyboard_button.id,
			'target_object_type': 'command',
			'target_object_id': self.command_1.id,
		})
		self.assertEqual(response.status_code, 200)

class ConnectionAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command_1: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 1',
		)
		self.command_2: Command = Command.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name 1',
		)
		self.command_2_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
			command=self.command_2,
			type='default',
		)
		self.command_2_keyboard_button: CommandKeyboardButton = CommandKeyboardButton.objects.create(
			keyboard=self.command_2_keyboard,
			text='Button',
		)
		self.connection: Connection = Connection.objects.create(
			telegram_bot=self.telegram_bot,
			source_object=self.command_2_keyboard_button,
			target_object=self.command_1,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:connection',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'connection_id': self.connection.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:diagram:connection',
			kwargs={
				'telegram_bot_id': 0,
				'connection_id': self.connection.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:connection',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'connection_id': 0,
			}
		)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 200)

class VariablesAPIViewTests(CustomTestCase):
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

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.true_url, {
			'name': 'Test name',
			'value': 'The test value :)',
			'description': 'The test variable',
		})
		self.assertEqual(response.status_code, 201)

class VariableAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.variable: Variable = Variable.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test name',
			value='The test value :)',
			description='The test variable',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'variable_id': self.variable.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': 0,
				'variable_id': self.variable.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'variable_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.patch(self.true_url, {
			'name': 'Test name',
			'value': 'The test value :)',
			'description': 'The test variable',
		})
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 200)

class UsersAPIViewTests(CustomTestCase):
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

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

class UserAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.user = User.objects.create(
			telegram_bot=self.telegram_bot,
			telegram_id=123456789,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'user_id': self.user.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': 0,
				'user_id': self.user.id,
			}
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'user_id': 0,
			}
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.post(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(self.true_url, {'action': 'allow'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post(self.true_url, {'action': 'unallow'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post(self.true_url, {'action': 'block'})
		self.assertEqual(response.status_code, 200)

		response = self.client.post(self.true_url, {'action': 'unblock'})
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in (self.false_url_1, self.false_url_2):
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 200)