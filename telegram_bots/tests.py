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
			telegram_id=123456789,
			first_name='exg1o',
		)
		self.token: Token = Token.objects.create(user=self.site_user)
		self.telegram_bot: TelegramBot = self.site_user.telegram_bots.create(api_token='Hi!')


class TelegramBotsAPIViewTests(CustomTestCase):
	url: str = reverse('api:telegram-bots:telegram-bot-list')

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

		old_telegram_bot_count: int = self.site_user.telegram_bots.count()

		response = self.client.post(
			self.url,
			{
				'api_token': 'Bye!',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(
			self.site_user.telegram_bots.count(),
			old_telegram_bot_count + 1,
		)


class TelegramBotAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse('api:telegram-bots:telegram-bot-detail', kwargs={'id': self.telegram_bot.id})
		self.false_url: str = reverse('api:telegram-bots:telegram-bot-detail', kwargs={'id': 0})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method_for_start_action(self) -> None:
		self.true_url = reverse('api:telegram-bots:telegram-bot-start', kwargs={'id': self.telegram_bot.id})
		self.false_url = reverse('api:telegram-bots:telegram-bot-start', kwargs={'id': 0})

		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method_for_restart_action(self) -> None:
		self.true_url = reverse('api:telegram-bots:telegram-bot-restart', kwargs={'id': self.telegram_bot.id})
		self.false_url = reverse('api:telegram-bots:telegram-bot-restart', kwargs={'id': 0})

		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_post_method_for_stop_action(self) -> None:
		self.true_url = reverse('api:telegram-bots:telegram-bot-stop', kwargs={'id': self.telegram_bot.id})
		self.false_url = reverse('api:telegram-bots:telegram-bot-stop', kwargs={'id': 0})

		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.put(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_api_token_1: str = '123456789:exg1o'

		response = self.client.put(self.true_url, {'api_token': new_api_token_1})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token_1)

		response = self.client.put(self.true_url, {'is_private': True})
		self.assertEqual(response.status_code, 400)

		new_api_token_2: str = '987654321:exg1o'

		response = self.client.put(
			self.true_url,
			{
				'api_token': new_api_token_2,
				'is_private': True,
			},
		)
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token_2)
		self.assertTrue(self.telegram_bot.is_private)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.patch(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_api_token: str = '123456789:exg1o'

		response = self.client.patch(self.true_url, {'api_token': new_api_token})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token)

		response = self.client.patch(self.true_url, {'is_private': True})
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertTrue(self.telegram_bot.is_private)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.delete(self.false_url)
		self.assertEqual(response.status_code, 404)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.telegram_bot.refresh_from_db()
			raise self.failureException('Telegram bot has not been deleted from database!')
		except TelegramBot.DoesNotExist:
			pass


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
		self.command_2_keyboard_button: CommandKeyboardButton = self.command_2_keyboard.buttons.create(text='Button')

		self.true_url: str = reverse(
			'api:telegram-bots:detail:connections',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse('api:telegram-bots:detail:connections', kwargs={'telegram_bot_id': 0})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.false_url)
		self.assertEqual(response.status_code, 403)

		old_command_1_target_connection_count: int = self.command_1.target_connections.count()
		old_command_2_keyboard_button_source_connection_count: int = (
			self.command_2_keyboard_button.source_connections.count()
		)

		response = self.client.post(
			self.true_url,
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
		self.command_2_keyboard_button: CommandKeyboardButton = self.command_2_keyboard.buttons.create(text='Button')

		self.connection: Connection = self.telegram_bot.connections.create(
			source_object=self.command_2_keyboard_button,
			target_object=self.command_1,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:connection',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'connection_id': self.connection.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:connection',
			kwargs={
				'telegram_bot_id': 0,
				'connection_id': self.connection.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:connection',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'connection_id': 0,
			},
		)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.connection.refresh_from_db()
			raise self.failureException('Connection has not been deleted from database!')
		except Connection.DoesNotExist:
			pass


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

		response = self.client.post(
			self.true_url,
			{
				'data': json.dumps(
					{
						'name': 'Test name',
						'message': {
							'text': 'The test message :)',
						},
					}
				),
			},
		)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			self.true_url,
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
				),
			},
		)
		self.assertEqual(response.status_code, 400)

		old_command_count: int = self.telegram_bot.commands.count()

		response = self.client.post(
			self.true_url,
			{
				'data': json.dumps(
					{
						'name': 'Test name',
						'settings': {
							'is_reply_to_user_message': False,
							'is_delete_user_message': False,
							'is_send_as_new_message': False,
						},
						'message': {
							'text': 'The test message :)',
						},
					}
				),
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.commands.count(), old_command_count + 1)


class CommandAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = self.telegram_bot.commands.create(name='Test name')
		CommandSettings.objects.create(command=self.command)
		CommandMessage.objects.create(command=self.command, text='...')

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
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(self.true_url, {'data': json.dumps({'name': new_name})})
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.true_url,
			{
				'data': json.dumps(
					{
						'name': new_name,
						'settings': {
							'is_reply_to_user_message': False,
							'is_delete_user_message': False,
							'is_send_as_new_message': False,
						},
						'message': {
							'text': 'The test message :)',
						},
					}
				),
			},
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.true_url, {'data': json.dumps({'name': new_name})})
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.command.refresh_from_db()
			raise self.failureException('Command has not been deleted from database!')
		except Command.DoesNotExist:
			pass


class ConditionsAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:conditions',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:conditions',
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

		response = self.client.post(
			self.true_url,
			{
				'name': 'Test name',
				'parts': [],
			},
			format='json',
		)
		self.assertEqual(response.status_code, 400)

		old_condition_count: int = self.telegram_bot.conditions.count()

		response = self.client.post(
			self.true_url,
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


class ConditionAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.condition: Condition = self.telegram_bot.conditions.create(name='Test name')
		self.condition.parts.create(
			type='+',
			first_value='first_value',
			operator='==',
			second_value='second_value',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:condition',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'condition_id': self.condition.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:condition',
			kwargs={
				'telegram_bot_id': 0,
				'condition_id': self.condition.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:condition',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'condition_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(
			self.true_url,
			{
				'name': new_name,
				'parts': [],
			},
			format='json',
		)
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.true_url,
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

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.name, new_name)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.condition.refresh_from_db()
			raise self.failureException('Condition has not been deleted from database!')
		except Condition.DoesNotExist:
			pass


class BackgroundTasksAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:background-tasks',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:background-tasks',
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

		old_background_task_count: int = self.telegram_bot.background_tasks.count()

		response = self.client.post(
			self.true_url,
			{
				'name': 'Test name',
				'interval': 1,
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.background_tasks.count(), old_background_task_count + 1)


class BackgroundTaskAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.background_task: BackgroundTask = self.telegram_bot.background_tasks.create(
			name='Test name',
			interval=1,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:background-task',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'background_task_id': self.background_task.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:background-task',
			kwargs={
				'telegram_bot_id': 0,
				'background_task_id': self.background_task.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:background-task',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'background_task_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(self.true_url, {'name': new_name})
		self.assertEqual(response.status_code, 400)

		response = self.client.put(
			self.true_url,
			{
				'name': new_name,
				'interval': 1,
			},
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.background_task.refresh_from_db()
			raise self.failureException('Background task has not been deleted from database!')
		except BackgroundTask.DoesNotExist:
			pass


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

		self.command: Command = self.telegram_bot.commands.create(name='Test name')

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
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:command',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'command_id': 0,
			},
		)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.x, new_x)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.x, new_x)


class DiagramConditionsAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:conditions',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:diagram:conditions',
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


class DiagramConditionAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.condition: Condition = self.telegram_bot.conditions.create(name='Test name')
		self.condition.parts.create(
			type='+',
			first_value='first_value',
			operator='==',
			second_value='second_value',
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:condition',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'condition_id': self.condition.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:diagram:condition',
			kwargs={
				'telegram_bot_id': 0,
				'condition_id': self.condition.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:condition',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'condition_id': 0,
			},
		)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.x, new_x)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.x, new_x)


class DiagramBackgroundTasksAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:background-tasks',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:diagram:background-tasks',
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


class DiagramBackgroundTaskAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.background_task: BackgroundTask = self.telegram_bot.background_tasks.create(
			name='Test name',
			interval=1,
		)

		self.true_url: str = reverse(
			'api:telegram-bots:detail:diagram:background-task',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'background_task_id': self.background_task.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:diagram:background-task',
			kwargs={
				'telegram_bot_id': 0,
				'background_task_id': self.background_task.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:diagram:background-task',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'background_task_id': 0,
			},
		)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.put(self.true_url, {'x': new_x, 'y': 200})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		response = self.client.patch(self.true_url, {'x': new_x})
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)


class VariablesAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:variables',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse('api:telegram-bots:detail:variables', kwargs={'telegram_bot_id': 0})

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

		old_variable_count: int = self.telegram_bot.variables.count()

		response = self.client.post(
			self.true_url,
			{
				'name': 'Test name',
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.variables.count(), old_variable_count + 1)


class VariableAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.variable: Variable = self.telegram_bot.variables.create(
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
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:variable',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'variable_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		response = self.client.put(
			self.true_url,
			{
				'name': new_name,
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		response = self.client.patch(self.true_url, {'name': new_name})
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.variable.refresh_from_db()
			raise self.failureException('Variable has not been deleted from database!')
		except Variable.DoesNotExist:
			pass


class UsersAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:users',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:users',
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


class UserAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.user = self.telegram_bot.users.create(telegram_id=123456789)

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
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:user',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'user_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.put(
			self.true_url,
			{
				'is_allowed': False,
				'is_blocked': True,
			},
		)
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		response = self.client.patch(self.true_url, {'is_blocked': True})
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.user.refresh_from_db()
			raise self.failureException('User has not been deleted from database!')
		except User.DoesNotExist:
			pass


class DatabaseRecordsAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.true_url: str = reverse(
			'api:telegram-bots:detail:database-records',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.false_url: str = reverse(
			'api:telegram-bots:detail:database-records',
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

		old_database_record_count: int = self.telegram_bot.database_records.count()

		response = self.client.post(self.true_url, {'data': {'key': 'value'}}, format='json')
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.database_records.count(), old_database_record_count + 1)


class DatabaseRecordAPIViewTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.database_record = self.telegram_bot.database_records.create(data={'key': 'value'})

		self.true_url: str = reverse(
			'api:telegram-bots:detail:database-record',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'database_record_id': self.database_record.id,
			},
		)
		self.false_url_1: str = reverse(
			'api:telegram-bots:detail:database-record',
			kwargs={
				'telegram_bot_id': 0,
				'database_record_id': self.database_record.id,
			},
		)
		self.false_url_2: str = reverse(
			'api:telegram-bots:detail:database-record',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'database_record_id': 0,
			},
		)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.get(self.true_url)
		self.assertEqual(response.status_code, 200)

	def test_put_method(self) -> None:
		response: HttpResponse = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.put(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.put(self.true_url)
		self.assertEqual(response.status_code, 400)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		response = self.client.put(self.true_url, {'data': new_data}, format='json')
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.patch(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.patch(self.true_url)
		self.assertEqual(response.status_code, 200)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		response = self.client.patch(self.true_url, {'data': new_data}, format='json')
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		for url in [self.false_url_1, self.false_url_2]:
			response = self.client.delete(url)
			self.assertEqual(response.status_code, 403)

		response = self.client.delete(self.true_url)
		self.assertEqual(response.status_code, 204)

		try:
			self.database_record.refresh_from_db()
			raise self.failureException('Database record has not been deleted from database!')
		except DatabaseRecord.DoesNotExist:
			pass
