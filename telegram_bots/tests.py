from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import User as SiteUser

from .models import (
	BackgroundTask,
	Command,
	CommandKeyboard,
	CommandKeyboardButton,
	CommandMessage,
	CommandSettings,
	Condition,
	Connection,
	DatabaseRecord,
	TelegramBot,
	User,
	Variable,
)

from typing import Any
import json


class StatsAPIViewTests(TestCase):
	url: str = reverse('api:telegram-bots:stats')

	def setUp(self) -> None:
		self.client: APIClient = APIClient()

	def test_get_method(self) -> None:
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()
		self.site_user: SiteUser = SiteUser.objects.create(
			telegram_id=123456789, first_name='exg1o'
		)
		self.token: Token = Token.objects.create(user=self.site_user)
		self.telegram_bot: TelegramBot = self.site_user.telegram_bots.create(
			api_token='Hi!'
		)


class TelegramBotViewSetTests(CustomTestCase):
	list_url: str = reverse('api:telegram-bots:telegram-bot-list')

	def setUp(self) -> None:
		super().setUp()

		true_kwargs: dict[str, Any] = {'id': self.telegram_bot.id}
		false_kwargs: dict[str, Any] = {'id': 0}

		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-detail', kwargs=true_kwargs
		)
		self.detail_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-detail', kwargs=false_kwargs
		)
		self.start_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-start', kwargs=true_kwargs
		)
		self.start_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-start', kwargs=false_kwargs
		)
		self.restart_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-restart', kwargs=true_kwargs
		)
		self.restart_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-restart', kwargs=false_kwargs
		)
		self.stop_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-stop', kwargs=true_kwargs
		)
		self.stop_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-stop', kwargs=false_kwargs
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_url)
		self.assertEqual(response.status_code, 400)

		old_telegram_bot_count: int = self.site_user.telegram_bots.count()

		response = self.client.post(
			self.list_url, {'api_token': 'Bye!', 'is_private': False}
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(
			self.site_user.telegram_bots.count(), old_telegram_bot_count + 1
		)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.detail_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_start(self) -> None:
		response: HttpResponse = self.client.post(self.start_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.start_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.start_true_url)
		self.assertEqual(response.status_code, 200)

	def test_restart(self) -> None:
		response: HttpResponse = self.client.post(self.restart_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.restart_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.restart_true_url)
		self.assertEqual(response.status_code, 200)

	def test_stop(self) -> None:
		response: HttpResponse = self.client.post(self.stop_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.stop_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.stop_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.put(self.detail_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_api_token_1: str = '123456789:exg1o'

		response = self.client.put(self.detail_true_url, {'api_token': new_api_token_1})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token_1)

		response = self.client.put(self.detail_true_url, {'is_private': True})
		self.assertEqual(response.status_code, 400)

		new_api_token_2: str = '987654321:exg1o'

		response = self.client.put(
			self.detail_true_url, {'api_token': new_api_token_2, 'is_private': True}
		)
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token_2)
		self.assertTrue(self.telegram_bot.is_private)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.patch(self.detail_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_api_token: str = '123456789:exg1o'

		response = self.client.patch(self.detail_true_url, {'api_token': new_api_token})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token)

		response = self.client.patch(self.detail_true_url, {'is_private': True})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertTrue(self.telegram_bot.is_private)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.delete(self.detail_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.telegram_bot.refresh_from_db()
			raise self.failureException(
				'Telegram bot has not been deleted from database!'
			)
		except TelegramBot.DoesNotExist:
			pass


class ConnectionViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command_1: Command = self.telegram_bot.commands.create(name='Test name 1')

		self.command_2: Command = self.telegram_bot.commands.create(name='Test name 1')
		self.command_2_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
			command=self.command_2, type='default'
		)
		self.command_2_keyboard_button: CommandKeyboardButton = (
			self.command_2_keyboard.buttons.create(row=0, position=0, text='Button')
		)

		self.connection: Connection = self.telegram_bot.connections.create(
			source_object=self.command_2_keyboard_button, target_object=self.command_1
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-connection-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-connection-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-connection-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.connection.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-connection-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.connection.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-connection-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		old_command_1_target_connection_count: int = (
			self.command_1.target_connections.count()
		)
		old_command_2_keyboard_button_source_connection_count: int = (
			self.command_2_keyboard_button.source_connections.count()
		)

		response = self.client.post(
			self.list_true_url,
			{
				'source_object_type': 'command_keyboard_button',
				'source_object_id': self.command_2_keyboard_button.id,
				'target_object_type': 'command',
				'target_object_id': self.command_1.id,
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(
			self.command_1.target_connections.count(),
			old_command_1_target_connection_count + 1,
		)
		self.assertEqual(
			self.command_2_keyboard_button.source_connections.count(),
			old_command_2_keyboard_button_source_connection_count + 1,
		)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.connection.refresh_from_db()
			raise self.failureException(
				'Connection has not been deleted from database!'
			)
		except Connection.DoesNotExist:
			pass


class CommandViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = self.telegram_bot.commands.create(name='Test name')
		CommandSettings.objects.create(command=self.command)
		CommandMessage.objects.create(command=self.command, text='...')

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-command-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-command-list', kwargs={'telegram_bot_id': 0}
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.command.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.command.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			self.list_true_url,
			{
				'data': json.dumps(
					{'name': 'Test name', 'message': {'text': 'The test message :)'}}
				)
			},
		)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			self.list_true_url,
			{
				'data': json.dumps(
					{
						'name': 'Test name',
						'settings': {
							'is_reply_to_user_message': False,
							'is_delete_user_message': False,
							'is_send_as_new_message': False,
						},
					}
				)
			},
		)
		self.assertEqual(response.status_code, 400)

		old_command_count: int = self.telegram_bot.commands.count()

		response = self.client.post(
			self.list_true_url,
			{
				'data': json.dumps(
					{
						'name': 'Test name',
						'settings': {
							'is_reply_to_user_message': False,
							'is_delete_user_message': False,
							'is_send_as_new_message': False,
						},
						'message': {'text': 'The test message :)'},
					}
				)
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.commands.count(), old_command_count + 1)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(
			self.detail_true_url, {'data': json.dumps({'name': new_name})}
		)
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.detail_true_url,
			{
				'data': json.dumps(
					{
						'name': new_name,
						'settings': {
							'is_reply_to_user_message': False,
							'is_delete_user_message': False,
							'is_send_as_new_message': False,
						},
						'message': {'text': 'The test message :)'},
					}
				)
			},
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(
			self.detail_true_url, {'data': json.dumps({'name': new_name})}
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.command.refresh_from_db()
			raise self.failureException('Command has not been deleted from database!')
		except Command.DoesNotExist:
			pass


class ConditionViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.condition: Condition = self.telegram_bot.conditions.create(
			name='Test name'
		)
		self.condition.parts.create(
			type='+',
			first_value='first_value',
			operator='==',
			second_value='second_value',
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-condition-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-condition-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.condition.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.condition.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			self.list_true_url, {'name': 'Test name', 'parts': []}, format='json'
		)
		self.assertEqual(response.status_code, 400)

		old_condition_count: int = self.telegram_bot.conditions.count()

		response = self.client.post(
			self.list_true_url,
			{
				'name': 'Test name',
				'parts': [
					{
						'type': '+',
						'first_value': 'first_value',
						'operator': '==',
						'second_value': 'second_value',
					}
				],
			},
			format='json',
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.conditions.count(), old_condition_count + 1)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(
			self.detail_true_url, {'name': new_name, 'parts': []}, format='json'
		)
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.detail_true_url,
			{
				'name': new_name,
				'parts': [
					{
						'type': '+',
						'first_value': 'first_value',
						'operator': '==',
						'second_value': 'second_value',
					}
				],
			},
			format='json',
		)
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.name, new_name)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.detail_true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.name, new_name)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.condition.refresh_from_db()
			raise self.failureException('Condition has not been deleted from database!')
		except Condition.DoesNotExist:
			pass


class BackgroundTaskViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.background_task: BackgroundTask = (
			self.telegram_bot.background_tasks.create(name='Test name', interval=1)
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-background-task-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-background-task-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-background-task-detail',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'id': self.background_task.id,
			},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-background-task-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.background_task.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-background-task-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 400)

		old_background_task_count: int = self.telegram_bot.background_tasks.count()

		response = self.client.post(
			self.list_true_url, {'name': 'Test name', 'interval': 1}
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(
			self.telegram_bot.background_tasks.count(), old_background_task_count + 1
		)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(self.detail_true_url, {'name': new_name})
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.detail_true_url, {'name': new_name, 'interval': 1}
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.detail_true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.background_task.refresh_from_db()
			raise self.failureException(
				'Background task has not been deleted from database!'
			)
		except BackgroundTask.DoesNotExist:
			pass


class DiagramCommandViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = self.telegram_bot.commands.create(name='Test name')

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-command-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-command-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.command.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-command-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.command.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.detail_true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.x, new_x)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.detail_true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.x, new_x)


class DiagramConditionViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.condition: Condition = self.telegram_bot.conditions.create(
			name='Test name'
		)
		self.condition.parts.create(
			type='+',
			first_value='first_value',
			operator='==',
			second_value='second_value',
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-condition-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-condition-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.condition.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-condition-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.condition.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.detail_true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.x, new_x)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.detail_true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.x, new_x)


class DiagramBackgroundTaskViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.background_task: BackgroundTask = (
			self.telegram_bot.background_tasks.create(name='Test name', interval=1)
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-background-task-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-background-task-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-background-task-detail',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'id': self.background_task.id,
			},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-background-task-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.background_task.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-diagram-background-task-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.detail_true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.detail_true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)


class VariablesAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.variable: Variable = self.telegram_bot.variables.create(
			name='Test name', value='The test value :)', description='The test variable'
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-variable-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-variable-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.variable.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.variable.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 400)

		old_variable_count: int = self.telegram_bot.variables.count()

		response = self.client.post(
			self.list_true_url,
			{
				'name': 'Test name',
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.variables.count(), old_variable_count + 1)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(
			self.detail_true_url,
			{
				'name': new_name,
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.detail_true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.variable.refresh_from_db()
			raise self.failureException('Variable has not been deleted from database!')
		except Variable.DoesNotExist:
			pass


class UserViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.user = self.telegram_bot.users.create(telegram_id=123456789)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-user-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-user-list', kwargs={'telegram_bot_id': 0}
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.user.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.user.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.put(
			self.detail_true_url, {'is_allowed': False, 'is_blocked': True}
		)
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.detail_true_url, {'is_blocked': True})
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.user.refresh_from_db()
			raise self.failureException('User has not been deleted from database!')
		except User.DoesNotExist:
			pass


class DatabaseRecordViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.database_record = self.telegram_bot.database_records.create(
			data={'key': 'value'}
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-database-record-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots:telegram-bot-database-record-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots:telegram-bot-database-record-detail',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'id': self.database_record.id,
			},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots:telegram-bot-database-record-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.database_record.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots:telegram-bot-database-record-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, 404)

		old_database_record_count: int = self.telegram_bot.database_records.count()

		response = self.client.post(
			self.list_true_url, {'data': {'key': 'value'}}, format='json'
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(
			self.telegram_bot.database_records.count(), old_database_record_count + 1
		)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		response: HttpResponse = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.put(self.detail_true_url)
		self.assertEqual(response.status_code, 400)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		response = self.client.put(
			self.detail_true_url, {'data': new_data}, format='json'
		)
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_partial_update(self) -> None:
		response: HttpResponse = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.detail_true_url)
		self.assertEqual(response.status_code, 200)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		response = self.client.patch(
			self.detail_true_url, {'data': new_data}, format='json'
		)
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_destroy(self) -> None:
		response: HttpResponse = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.detail_true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.database_record.refresh_from_db()
			raise self.failureException(
				'Database record has not been deleted from database!'
			)
		except DatabaseRecord.DoesNotExist:
			pass
