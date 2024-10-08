from django.test import TestCase
from django.urls import reverse

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from users.models import User as SiteUser
from users.tokens import AccessToken, RefreshToken

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
from .views import (
	BackgroundTaskViewSet,
	CommandViewSet,
	ConditionViewSet,
	ConnectionViewSet,
	DatabaseRecordViewSet,
	DiagramBackgroundTaskViewSet,
	DiagramCommandViewSet,
	DiagramConditionViewSet,
	TelegramBotViewSet,
	UserViewSet,
	VariableViewSet,
)

from contextlib import suppress
from typing import TYPE_CHECKING, Any
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
		self.factory = APIRequestFactory()
		self.site_user: SiteUser = SiteUser.objects.create(
			telegram_id=123456789, first_name='exg1o'
		)
		self.refresh_token: RefreshToken = RefreshToken.for_user(self.site_user)
		self.access_token: AccessToken = self.refresh_token.access_token
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
		view = TelegramBotViewSet.as_view({'get': 'list'})

		request: Request = self.factory.get(self.list_url)

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = TelegramBotViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_url)

		response = view(request)
		self.assertEqual(response.status_code, 403)

		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
			self.list_url, {'api_token': 'Bye!', 'is_private': False}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		old_telegram_bot_count: int = self.site_user.telegram_bots.count()

		response = view(request)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(
			self.site_user.telegram_bots.count(), old_telegram_bot_count + 1
		)

	def test_retrieve(self) -> None:
		view = TelegramBotViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.detail_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_start(self) -> None:
		view = TelegramBotViewSet.as_view({'post': 'start'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.start_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.start_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.start_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_restart(self) -> None:
		view = TelegramBotViewSet.as_view({'post': 'restart'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.restart_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.restart_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.restart_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_stop(self) -> None:
		view = TelegramBotViewSet.as_view({'post': 'stop'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.stop_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.stop_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.stop_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = TelegramBotViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.put(self.detail_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url, format='json')
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		new_api_token: str = '123456789:exg1o'
		data: dict[str, Any] = {'api_token': new_api_token}

		request = self.factory.put(self.detail_true_url, data, format='json')
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token)

	def test_partial_update(self) -> None:
		view = TelegramBotViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.patch(self.detail_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

		new_api_token: str = '123456789:exg1o'

		request = self.factory.patch(
			self.detail_true_url, {'api_token': new_api_token}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

		self.telegram_bot.refresh_from_db()
		self.assertEqual(self.telegram_bot.api_token, new_api_token)

	def test_destroy(self) -> None:
		view = TelegramBotViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.delete(self.detail_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 204)

		with suppress(TelegramBot.DoesNotExist):
			self.telegram_bot.refresh_from_db()
			raise self.failureException(
				'Telegram bot has not been deleted from database!'
			)


class ConnectionViewSetTests(CustomTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.command_1: Command = self.telegram_bot.commands.create(name='Test name 1')

		self.command_2: Command = self.telegram_bot.commands.create(name='Test name 2')
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
		view = ConnectionViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(
			self.list_true_url, telegram_bot_id=self.telegram_bot.id
		)

		response = view(request)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(
			self.list_true_url,
			{
				'source_object_type': 'command_keyboard_button',
				'source_object_id': self.command_2_keyboard_button.id,
				'target_object_type': 'command',
				'target_object_id': self.command_1.id,
			},
			format='json',
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		old_command_1_target_connection_count: int = (
			self.command_1.target_connections.count()
		)
		old_command_2_keyboard_button_source_connection_count: int = (
			self.command_2_keyboard_button.source_connections.count()
		)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
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
		view = ConnectionViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.connection.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=self.telegram_bot.id, id=0)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.connection.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(Connection.DoesNotExist):
			self.connection.refresh_from_db()
			raise self.failureException(
				'Connection has not been deleted from database!'
			)


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
		view = CommandViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = CommandViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
			self.list_true_url,
			{
				'data': json.dumps(
					{'name': 'Test name', 'message': {'text': 'The test message :)'}}
				)
			},
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
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
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
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
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		old_command_count: int = self.telegram_bot.commands.count()

		response = view(request, telegram_bot_id=self.telegram_bot.id)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(self.telegram_bot.commands.count(), old_command_count + 1)

	def test_retrieve(self) -> None:
		view = CommandViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = CommandViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		request = self.factory.put(
			self.detail_true_url, {'data': json.dumps({'name': new_name})}
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 400)

		request = self.factory.put(
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
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_partial_update(self) -> None:
		view = CommandViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		request = self.factory.patch(
			self.detail_true_url, {'data': json.dumps({'name': new_name})}
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.name, new_name)

	def test_destroy(self) -> None:
		view = CommandViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)
		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)

		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(Command.DoesNotExist):
			self.command.refresh_from_db()
			raise self.failureException('Command has not been deleted from database!')


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
		view = ConditionViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = ConditionViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
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
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		old_condition_count: int = self.telegram_bot.conditions.count()

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(self.telegram_bot.conditions.count(), old_condition_count + 1)

	def test_retrieve(self) -> None:
		view = ConditionViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = ConditionViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		new_name: str = 'Test name 2'

		request = self.factory.put(
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
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.name, new_name)

	def test_partial_update(self) -> None:
		view = ConditionViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		request = self.factory.patch(
			self.detail_true_url, {'name': new_name}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.name, new_name)

	def test_destroy(self) -> None:
		view = ConditionViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(Condition.DoesNotExist):
			self.condition.refresh_from_db()
			raise self.failureException('Condition has not been deleted from database!')


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
		view = BackgroundTaskViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = BackgroundTaskViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		request = self.factory.post(
			self.list_true_url,
			{'name': 'Test name', 'interval': 1},
			format='json',
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		old_background_task_count: int = self.telegram_bot.background_tasks.count()

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(
			self.telegram_bot.background_tasks.count(), old_background_task_count + 1
		)

	def test_retrieve(self) -> None:
		view = BackgroundTaskViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = BackgroundTaskViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		new_name: str = 'Test name 2'

		request = self.factory.put(
			self.detail_true_url, {'name': new_name}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 400)

		request = self.factory.put(
			self.detail_true_url,
			{'name': new_name, 'interval': 1},
			format='json',
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_partial_update(self) -> None:
		view = BackgroundTaskViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		request = self.factory.patch(
			self.detail_true_url, {'name': new_name}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.name, new_name)

	def test_destroy(self) -> None:
		view = BackgroundTaskViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(BackgroundTask.DoesNotExist):
			self.background_task.refresh_from_db()
			raise self.failureException(
				'Background task has not been deleted from database!'
			)


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
		view = DiagramCommandViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

	def test_list(self) -> None:
		view = DiagramCommandViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = DiagramCommandViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.put(
			self.detail_true_url, {'x': new_x, 'y': 200}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		self.command.refresh_from_db()
		self.assertEqual(self.command.x, new_x)

	def test_partial_update(self) -> None:
		view = DiagramCommandViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.command.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.patch(self.detail_true_url, {'x': new_x}, format='json')
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.command.id
		)
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
		view = DiagramConditionViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		view = DiagramConditionViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = DiagramConditionViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.put(
			self.detail_true_url, {'x': new_x, 'y': 200}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		self.condition.refresh_from_db()
		self.assertEqual(self.condition.x, new_x)

	def test_partial_update(self) -> None:
		view = DiagramConditionViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.condition.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.patch(self.detail_true_url, {'x': new_x}, format='json')
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
		)
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
		view = DiagramBackgroundTaskViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		view = DiagramBackgroundTaskViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = DiagramBackgroundTaskViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.put(
			self.detail_true_url, {'x': new_x, 'y': 200}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)

	def test_partial_update(self) -> None:
		view = DiagramBackgroundTaskViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.background_task.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		new_x: int = 150

		request = self.factory.patch(self.detail_true_url, {'x': new_x}, format='json')
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
		)
		self.assertEqual(response.status_code, 200)

		self.background_task.refresh_from_db()
		self.assertEqual(self.background_task.x, new_x)


class VariableViewSetTests(CustomTestCase):
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
		view = VariableViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = VariableViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.post(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 400)

		old_variable_count: int = self.telegram_bot.variables.count()

		request = self.factory.post(
			self.list_true_url,
			{
				'name': 'Test name',
				'value': 'The test value :)',
				'description': 'The test variable',
			},
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(self.telegram_bot.variables.count(), old_variable_count + 1)

	def test_retrieve(self) -> None:
		view = VariableViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.variable.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = VariableViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.variable.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 400)

		new_name: str = 'Test name 2'

		request = self.factory.put(
			self.detail_true_url,
			{
				'name': new_name,
				'value': 'The test value :)',
				'description': 'The test variable',
			},
			format='json',
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_partial_update(self) -> None:
		view = VariableViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.variable.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 200)

		new_name: str = 'Test name 2'

		request = self.factory.patch(
			self.detail_true_url, {'name': new_name}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 200)

		self.variable.refresh_from_db()
		self.assertEqual(self.variable.name, new_name)

	def test_destroy(self) -> None:
		view = VariableViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.variable.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(Variable.DoesNotExist):
			self.variable.refresh_from_db()
			raise self.failureException('Variable has not been deleted from database!')


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
		view = UserViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_retrieve(self) -> None:
		view = UserViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.user.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = UserViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.user.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 200)

		request = self.factory.put(
			self.detail_true_url,
			{'is_allowed': False, 'is_blocked': True},
			format='json',
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_partial_update(self) -> None:
		view = UserViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.user.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 200)

		request = self.factory.patch(
			self.detail_true_url, {'is_blocked': True}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()
		self.assertTrue(self.user.is_blocked)

	def test_destroy(self) -> None:
		view = UserViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.user.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id, id=self.user.id)
		self.assertEqual(response.status_code, 204)

		with suppress(User.DoesNotExist):
			self.user.refresh_from_db()
			raise self.failureException('User has not been deleted from database!')


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
		view = DatabaseRecordViewSet.as_view({'get': 'list'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.get(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.list_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 200)

	def test_create(self) -> None:
		view = DatabaseRecordViewSet.as_view({'post': 'create'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.post(self.list_true_url)

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 403)

		request = self.factory.post(self.list_false_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=0)
		self.assertEqual(response.status_code, 404)

		old_database_record_count: int = self.telegram_bot.database_records.count()

		request = self.factory.post(
			self.list_true_url, {'data': {'key': 'value'}}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(request, telegram_bot_id=self.telegram_bot.id)
		self.assertEqual(response.status_code, 201)

		self.assertEqual(
			self.telegram_bot.database_records.count(), old_database_record_count + 1
		)

	def test_retrieve(self) -> None:
		view = DatabaseRecordViewSet.as_view({'get': 'retrieve'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.get(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.get(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.database_record.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.get(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 200)

	def test_update(self) -> None:
		view = DatabaseRecordViewSet.as_view({'put': 'update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.put(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.put(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.database_record.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.put(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 400)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		request = self.factory.put(
			self.detail_true_url, {'data': new_data}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_partial_update(self) -> None:
		view = DatabaseRecordViewSet.as_view({'patch': 'partial_update'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.patch(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.patch(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.database_record.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.patch(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 200)

		new_data: dict[str, Any] = {'new_key': 'new_value'}

		request = self.factory.patch(
			self.detail_true_url, {'data': new_data}, format='json'
		)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 200)

		self.database_record.refresh_from_db()
		self.assertEqual(
			self.telegram_bot.database_records.get(data__contains=new_data).id,
			self.database_record.id,
		)

	def test_destroy(self) -> None:
		view = DatabaseRecordViewSet.as_view({'delete': 'destroy'})

		if TYPE_CHECKING:
			request: Request
			response: Response

		request = self.factory.delete(self.detail_true_url)

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 403)

		for url in [self.detail_false_url_1, self.detail_false_url_2]:
			request = self.factory.delete(url)
			force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

			response = view(request, telegram_bot_id=0, id=self.database_record.id)
			self.assertEqual(response.status_code, 404)

		request = self.factory.delete(self.detail_true_url)
		force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

		response = view(
			request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
		)
		self.assertEqual(response.status_code, 204)

		with suppress(DatabaseRecord.DoesNotExist):
			self.database_record.refresh_from_db()
			raise self.failureException(
				'Database record has not been deleted from database!'
			)
