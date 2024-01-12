from django.utils.translation import gettext as _, pgettext
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.template import defaultfilters as django_filters
from django.db.models import QuerySet

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from utils.drf import CustomResponse

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser,
)
from .permissions import (
	TelegramBotIsFound,
	TelegramBotCommandIsFound,
	TelegramBotUserIsFound,
)
from .serializers import (
	TelegramBotSerializer,
	TelegramBotCommandModelSerializer,
	TelegramBotCommandDiagramSerializer,
	TelegramBotUserSerializer,
	CreateTelegramBotSerializer,
	UpdateTelegramBotSerializer,
	CreateTelegramBotCommandSerializer,
	UpdateTelegramBotCommandSerializer,
	ConnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	UpdateTelegramBotCommandDiagramPositionSerializer,
)
from .tasks import start_telegram_bot

from typing import Any
from datetime import datetime, timedelta
import json


class TelegramBotsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		return Response(
			TelegramBotSerializer(
				request.user.telegram_bots.all(), # type: ignore [union-attr]
				many=True,
			).data
		)

	def post(self, request: Request) -> CustomResponse:
		serializer = CreateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = TelegramBot.objects.create(owner=request.user, **serializer.validated_data) # type: ignore [misc]

		return CustomResponse(
			_('Вы успешно добавили Telegram бота.'),
			data={'telegram_bot': TelegramBotSerializer(telegram_bot).data},
		)

class TelegramBotAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(TelegramBotSerializer(telegram_bot).data)

	def post(self, request: Request) -> CustomResponse:
		if not settings.TEST:
			telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
			action: str | None = request.query_params.get('action')

			if action == 'start':
				start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)
			elif action == 'stop':
				telegram_bot.stop()
			else:
				return CustomResponse(_('Не удалось найти и выполнить указанное действие в параметрах запроса!'), status=400)

		return CustomResponse()

	def patch(self, request: Request) -> CustomResponse:
		serializer = UpdateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		validated_data: dict[str, Any] = serializer.validated_data
		api_token: str | None = validated_data['api_token']
		is_private: bool | None = validated_data['is_private']

		if api_token is not None:
			telegram_bot.api_token = api_token
			telegram_bot.is_running = False
			telegram_bot.update_username(save=False)
			telegram_bot.save()

			return CustomResponse(
				_('Вы успешно изменили API-токен Telegram бота.'),
				data={'telegram_bot': TelegramBotSerializer(telegram_bot).data},
			)
		elif is_private is not None:
			telegram_bot.is_private = is_private
			telegram_bot.save()

			if is_private:
				success_message = _('Вы успешно сделали Telegram бота приватным.')
			else:
				success_message = _('Вы успешно сделали Telegram бота не приватным.')

			return CustomResponse(success_message, data={'telegram_bot': TelegramBotSerializer(telegram_bot).data})
		else:
			return CustomResponse(status=400)

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
		telegram_bot.delete()

		return CustomResponse(_('Вы успешно удалили Telegram бота.'))

class TelegramBotCommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotCommandModelSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

	def post(self, request: Request) -> CustomResponse:
		sorted_files: dict[str, list[InMemoryUploadedFile]] = {
			'images': [],
			'files': [],
		}

		for key, file in request.FILES.items():
			_type: str = key.split(':')[0] + 's'

			if _type in sorted_files:
				sorted_files[_type].append(file)

		data: dict[str, Any] = json.loads(request.data.get('data', '{}'))
		data.update(sorted_files)

		serializer = CreateTelegramBotCommandSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		TelegramBotCommand.objects.create(telegram_bot=telegram_bot, **serializer.validated_data)

		return CustomResponse(_('Вы успешно добавили команду Telegram боту.'))

class TelegramBotCommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		return Response(TelegramBotCommandModelSerializer(telegram_bot_command).data)

	def patch(self, request: Request) -> CustomResponse:
		sorted_files: dict[str, list[InMemoryUploadedFile | int]] = {
			'images': [],
			'images_id': [],
			'files': [],
			'files_id': [],
		}

		for key, value in request.data.items():
			name: str = key.split(':')[0] + 's'

			if name in sorted_files:
				if isinstance(value, InMemoryUploadedFile):
					sorted_files[name].append(value)
				elif isinstance(value, str) and value.isdigit():
					sorted_files[name + '_id'].append(int(value))

		data: dict[str, Any] = json.loads(request.data.get('data', '{}'))
		data['images'] = sorted_files['images']
		data['files'] = sorted_files['files']

		serializer = UpdateTelegramBotCommandSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		validated_data['images_id'] = sorted_files['images_id']
		validated_data['files_id'] = sorted_files['files_id']

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')
		telegram_bot_command.update(**validated_data)

		return CustomResponse(_('Вы успешно изменили команду Telegram бота.'))

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')
		telegram_bot_command.delete()

		return CustomResponse(_('Вы успешно удалили команду Telegram бота.'))

class TelegramBotCommandsDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotCommandDiagramSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

class TelegramBotCommandDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def post(self, request: Request) -> CustomResponse:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		serializer = ConnectTelegramBotCommandDiagramKeyboardButtonSerializer(
			data=request.data,
			context={
				'telegram_bot': telegram_bot,
				'telegram_bot_command': telegram_bot_command,
			},
		)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = telegram_bot_command.keyboard.buttons.get(
			id=validated_data['telegram_bot_command_keyboard_button_id']
		)
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot.commands.get(id=validated_data['telegram_bot_command_id'])
		telegram_bot_command_keyboard_button.start_diagram_connector = validated_data['start_diagram_connector']
		telegram_bot_command_keyboard_button.end_diagram_connector = validated_data['end_diagram_connector']
		telegram_bot_command_keyboard_button.save()

		return CustomResponse(_('Вы успешно подключили кнопку клавиатуры к другой команде'))

	def patch(self, request: Request) -> CustomResponse:
		serializer = UpdateTelegramBotCommandDiagramPositionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		validated_data: dict[str, Any] = serializer.validated_data

		telegram_bot_command.x = validated_data['x']
		telegram_bot_command.y = validated_data['y']
		telegram_bot_command.save()

		return CustomResponse()

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		serializer = DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer(
			data=request.data,
			context={'telegram_bot_command': telegram_bot_command},
		)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		telegram_bot_command_keyboard_button_id: int = validated_data['telegram_bot_command_keyboard_button_id']

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = telegram_bot_command.keyboard.buttons.get(
			id=telegram_bot_command_keyboard_button_id
		)
		telegram_bot_command_keyboard_button.telegram_bot_command = None
		telegram_bot_command_keyboard_button.start_diagram_connector = None
		telegram_bot_command_keyboard_button.end_diagram_connector = None
		telegram_bot_command_keyboard_button.save()

		return CustomResponse(_('Вы успешно отсоединили кнопку клавиатуры от другой команды'))

class TelegramBotUsersAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotUserSerializer(
				telegram_bot.users.all(),
				many=True,
			).data
		)

class TelegramBotUserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotUserIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')

		return Response(TelegramBotUserSerializer(telegram_bot_user).data)

	def post(self, request: Request) -> Response:
		action: str | None = request.query_params.get('action')

		if action in ['allow', 'unallow', 'block', 'unblock']:
			telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')

			if action == 'allow':
				telegram_bot_user.is_allowed = True
			elif action == 'unallow':
				telegram_bot_user.is_allowed = False
			elif action == 'block':
				telegram_bot_user.is_blocked = True
			elif action == 'unblock':
				telegram_bot_user.is_blocked = False

			telegram_bot_user.save()

			success_messages = {
				'allow': _('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.'),
				'unallow': _('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.'),
				'block': _('Вы успешно добавили пользователя в список заблокированных пользователей Telegram бота.'),
				'unblock': _('Вы успешно удалили пользователя из списка заблокированных пользователей Telegram бота.'),
			}

			return CustomResponse(success_messages[action], status=400)
		else:
			return CustomResponse(_('Не удалось найти и выполнить указанное действие в параметрах запроса!'), status=400)

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.delete()

		return CustomResponse(_('Вы успешно удалили пользователя Telegram бота.'))