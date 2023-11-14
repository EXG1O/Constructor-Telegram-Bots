from django.http import HttpResponse
from django import urls

from ..tests import BaseTestCase
from ..services import database_telegram_bot


class TelegramBotsViewTests(BaseTestCase):
	url: str = urls.reverse('telegram_bots')

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(
			self.url,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '123456789:qwertyuiop',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '987654321:dwawdadwa',
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot', kwargs={'telegram_bot_id': 0})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(
			self.url_2,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': None,
			},
		)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': None,
			},
		)
		self.assertEqual(response.status_code, 500)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '',
				'is_private': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '123456789:qwertyuiop',
				'is_private': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': '987654321:dwawdadwa',
				'is_private': None,
			},
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': False,
			},
		)
		self.assertEqual(response.status_code, 200)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'api_token': None,
				'is_private': True,
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class StartOrStopTelegramBotViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('start_or_stop_telegram_bot', kwargs={'telegram_bot_id': 0})

	def test_start_or_stop_telegram_bot_view(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class UpdateTelegramBotDiagramCurrentScaleViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('update_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('update_telegram_bot_diagram_current_scale', kwargs={'telegram_bot_id': 0})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2,  headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={'diagram_current_scale': 0.8},
		)
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandsViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_commands', kwargs={'telegram_bot_id': 0})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': '',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': ''},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '',
					'is_show_in_menu': False,
					'description': None
				},
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '/start',
					'is_show_in_menu': True,
					'description': ''
				},
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': ''},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '',
							'url': None,
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '1',
							'url': '',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': None,
							'row': None,
							'text': '1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': {
					'url': '',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': {
					'url': 'test',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
		})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': '',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': ''},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '',
					'is_show_in_menu': False,
					'description': None,
				},
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': {
					'text': '/start',
					'is_show_in_menu': True,
					'description': '',
				},
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '',
							'url': None,
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '1',
							'url': '',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': {
					'mode': 'default',
					'buttons': [
						{
							'id': '1',
							'row': None,
							'text': '1',
							'url': '-',
						},
					],
				},
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': {
					'url': '',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'blank')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': {
					'url': 'test',
					'method': 'get',
					'headers': None,
					'data': None,
				},
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json()['code'], 'invalid')

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'name': 'Test',
				'command': None,
				'message_text': {'text': 'Test...'},
				'keyboard': None,
				'api_request': None,
				'database_record': None,
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class UpdateTelegramBotCommandPositionViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_2: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
		})
		self.url_3: str = urls.reverse('update_telegram_bot_command_position', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
		})

	def test_patch_method(self) -> None:
		response: HttpResponse = self.client.patch(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.patch(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.patch(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'x': 123,
				'y': 321,
			},
		)
		self.assertEqual(response.status_code, 200)

class TelegramBotCommandKeyboardButtonTelegramBotCommandViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		telegram_bot_command_keyboard_button_id: int = self.telegram_bot_command.keyboard.buttons.all()[0].id

		self.url_1: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_2: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_3: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': 0,
			'telegram_bot_command_keyboard_button_id': telegram_bot_command_keyboard_button_id,
		})
		self.url_4: str = urls.reverse('telegram_bot_command_keyboard_button_telegram_bot_command', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_command_id': self.telegram_bot_command.id,
			'telegram_bot_command_keyboard_button_id': 0,
		})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_4, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_3,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'telegram_bot_command_id': 0,
				'start_diagram_connector': 'test',
				'end_diagram_connector': 'test',
			},
		)
		self.assertEqual(response.status_code, 404)

		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(
			telegram_bot=self.telegram_bot,
			name='Test',
			command=None,
			image=None,
			message_text={'text': 'Test...'},
			keyboard = None,
			api_request = None,
			database_record = None,
		)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={
				'telegram_bot_command_id': telegram_bot_command.id,
				'start_diagram_connector': 'test',
				'end_diagram_connector': 'test',
			},
		)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_4, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotUsersViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_users', kwargs={'telegram_bot_id': 0})

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.get(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotUserViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': 0,
		})

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotAllowedUserViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_2: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': 0,
			'telegram_bot_user_id': self.telegram_bot_user.id,
		})
		self.url_3: str = urls.reverse('telegram_bot_allowed_user', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'telegram_bot_user_id': 0,
		})

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.delete(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_3, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.delete(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)

class TelegramBotDatabeseRecordsViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_databese_records', kwargs={'telegram_bot_id': self.telegram_bot.id})
		self.url_2: str = urls.reverse('telegram_bot_databese_records', kwargs={'telegram_bot_id': 0})

	def tearDown(self) -> None:
		database_telegram_bot.delete_collection(self.telegram_bot)

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.post(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		response: HttpResponse = self.client.post(
			self.url_1,
			headers=self.base_headers,
			content_type='application/json',
			data={'record': {'key': 'value'}},
		)
		self.assertEqual(response.status_code, 200)

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url_1)
		self.assertEqual(response.status_code, 401)

		response: HttpResponse = self.client.get(self.url_2, headers=self.base_headers)
		self.assertEqual(response.status_code, 404)

		database_telegram_bot.insert_record(self.telegram_bot, {'key': 'value'})

		response: HttpResponse = self.client.get(self.url_1, headers=self.base_headers)
		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(response.content, [{'_id': 1, 'key': 'value'}])

class TelegramBotDatabeseRecordViewTests(BaseTestCase):
	def setUp(self) -> None:
		super().setUp()

		self.url_1: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'record_id': 1,
		})
		self.url_2: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': 0,
			'record_id': 0,
		})
		self.url_3: str = urls.reverse('telegram_bot_databese_record', kwargs={
			'telegram_bot_id': self.telegram_bot.id,
			'record_id': 0,
		})

	def tearDown(self) -> None:
		database_telegram_bot.delete_collection(self.telegram_bot)

	def test_patch_method(self) -> None:
		# TODO: Надо написать тесты для PATCH метода.
		pass

	def test_delete_method(self) -> None:
		# TODO: Надо написать тесты для DELETE метода.
		pass
