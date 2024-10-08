from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from users.models import User as SiteUser

from ..models import (
	BackgroundTask,
	Command,
	CommandMessage,
	CommandSettings,
	Condition,
	TelegramBot,
	Variable,
)
from .models import TelegramBotsHub


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()
		self.site_user: SiteUser = SiteUser.objects.create(
			telegram_id=123456789, first_name='exg1o'
		)
		self.telegram_bot: TelegramBot = self.site_user.telegram_bots.create(
			api_token='Hi!'
		)
		self.hub: TelegramBotsHub = TelegramBotsHub.objects.create(
			url='http://127.0.0.1', microservice_token='Token :-)'
		)

	def auth_client(self) -> None:
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.hub.service_token}')


class TelegramBotViewSetTests(BaseTestCase):
	list_url: str = reverse('api:telegram-bots-hub:telegram-bot-list')

	def setUp(self) -> None:
		super().setUp()

		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-detail',
			kwargs={'id': self.telegram_bot.id},
		)
		self.detail_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-detail', kwargs={'id': 0}
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.detail_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommandViewSetTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command: Command = self.telegram_bot.commands.create(name='Test name')
		CommandSettings.objects.create(command=self.command)
		CommandMessage.objects.create(command=self.command, text='...')

		self.list_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-command-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-command-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.command.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.command.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-command-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConditionViewSetTests(BaseTestCase):
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
			'api:telegram-bots-hub:telegram-bot-condition-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-condition-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.condition.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.condition.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-condition-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class BackgroundTaskViewSetTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.background_task: BackgroundTask = (
			self.telegram_bot.background_tasks.create(name='Test name', interval=1)
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-background-task-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-background-task-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-background-task-detail',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'id': self.background_task.id,
			},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-background-task-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.background_task.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-background-task-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class VariablesAPIViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.variable: Variable = self.telegram_bot.variables.create(
			name='Test name', value='The test value :)', description='The test variable'
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-variable-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-variable-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.variable.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.variable.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-variable-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.user = self.telegram_bot.users.create(telegram_id=123456789)

		self.list_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-user-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-user-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.user.id},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.user.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-user-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create(self) -> None:
		response: HttpResponse = self.client.post(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.post(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		old_user_count: int = self.telegram_bot.users.count()

		response = self.client.post(
			self.list_true_url, {'telegram_id': 987654321, 'full_name': 'exg1o <3'}
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		self.assertEqual(self.telegram_bot.users.count(), old_user_count + 1)


class DatabaseRecordViewSetTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.database_record = self.telegram_bot.database_records.create(
			data={'key': 'value'}
		)

		self.list_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-database-record-list',
			kwargs={'telegram_bot_id': self.telegram_bot.id},
		)
		self.list_false_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-database-record-list',
			kwargs={'telegram_bot_id': 0},
		)
		self.detail_true_url: str = reverse(
			'api:telegram-bots-hub:telegram-bot-database-record-detail',
			kwargs={
				'telegram_bot_id': self.telegram_bot.id,
				'id': self.database_record.id,
			},
		)
		self.detail_false_url_1: str = reverse(
			'api:telegram-bots-hub:telegram-bot-database-record-detail',
			kwargs={'telegram_bot_id': 0, 'id': self.database_record.id},
		)
		self.detail_false_url_2: str = reverse(
			'api:telegram-bots-hub:telegram-bot-database-record-detail',
			kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
		)

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		response = self.client.get(self.list_false_url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.list_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_retrieve(self) -> None:
		response: HttpResponse = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		self.auth_client()

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		response = self.client.get(self.detail_true_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
