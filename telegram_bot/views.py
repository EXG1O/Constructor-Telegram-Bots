from django.utils.translation import gettext as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.db.models import QuerySet

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from constructor_telegram_bots.responses import MessageResponse
from constructor_telegram_bots.mixins import PaginationMixin

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotVariable,
	TelegramBotUser,
)
from .permissions import (
	TelegramBotIsFound,
	TelegramBotCommandIsFound,
	TelegramBotVariableIsFound,
	TelegramBotUserIsFound,
)
from .serializers import (
	TelegramBotSerializer,
	TelegramBotCommandSerializer,
	CreateTelegramBotCommandSerializer,
	UpdateTelegramBotCommandSerializer,
	TelegramBotCommandDiagramSerializer,
	ConnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	UpdateTelegramBotCommandDiagramPositionSerializer,
	TelegramBotVariableSerializer,
	TelegramBotUserSerializer,
)

from typing import Any
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

	def post(self, request: Request) -> MessageResponse:
		serializer = TelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно добавили Telegram бота.'),
			data={'telegram_bot': serializer.data},
			status=201,
		)

class TelegramBotAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(TelegramBotSerializer(telegram_bot).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response | MessageResponse:
		action: str | None = request.query_params.get('action')

		if action not in ('start', 'stop'):
			return MessageResponse(_('Укажите действие в параметрах запроса!'), status=400)

		if not settings.TEST:
			if action == 'start':
				telegram_bot.start()
			elif action == 'restart':
				telegram_bot.restart()
			else:
				telegram_bot.stop()

		return Response()

	def patch(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
		serializer = TelegramBotSerializer(telegram_bot, request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		validated_data: dict[str, Any] = serializer.validated_data
		api_token: str | None = validated_data.get('api_token')
		is_private: bool | None = validated_data.get('is_private')

		match (api_token, is_private):
			case (str(), None):
				success_message = _('Вы успешно изменили API-токен Telegram бота.')
			case (None, True):
				success_message = _('Вы успешно сделали Telegram бота приватным.')
			case (None, False):
				success_message = _('Вы успешно сделали Telegram бота не приватным.')
			case __:
				success_message = _('Вы успешно обновили Telegram бота.')

		return MessageResponse(success_message, data={'telegram_bot': serializer.data})

	def delete(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
		telegram_bot.delete()

		return MessageResponse(_('Вы успешно удалили Telegram бота.'))

class TelegramBotCommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(
			TelegramBotCommandSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

	def post(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
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

		serializer = CreateTelegramBotCommandSerializer(data=data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно добавили команду Telegram боту.'),
			data={'telegram_bot_command': serializer.data},
			status=201,
		)

class TelegramBotCommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
		return Response(TelegramBotCommandSerializer(telegram_bot_command).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> MessageResponse:
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
		data.update(sorted_files)

		serializer = UpdateTelegramBotCommandSerializer(
			telegram_bot_command,
			data,
			context={'telegram_bot': telegram_bot},
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно изменили команду Telegram бота.'),
			data={'telegram_bot_command': serializer.data},
		)

	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> MessageResponse:
		telegram_bot_command.delete()

		return MessageResponse(_('Вы успешно удалили команду Telegram бота.'))

class TelegramBotCommandsDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(
			TelegramBotCommandDiagramSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

class TelegramBotCommandDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def post(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> MessageResponse:
		serializer = ConnectTelegramBotCommandDiagramKeyboardButtonSerializer(
			telegram_bot_command,
			request.data,
			context={'telegram_bot': telegram_bot},
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(_('Вы успешно подключили кнопку клавиатуры к другой команде'))

	def patch(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> Response:
		serializer = UpdateTelegramBotCommandDiagramPositionSerializer(telegram_bot_command, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response()

	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_command: TelegramBotCommand) -> MessageResponse:
		serializer = DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer(telegram_bot_command, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(_('Вы успешно отсоединили кнопку клавиатуры от другой команды'))

class TelegramBotVariablesAPIView(APIView, PaginationMixin):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	pagination_class = LimitOffsetPagination

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		queryset: 'QuerySet[TelegramBotVariable]' = telegram_bot.variables.all()
		results: list[TelegramBotVariable] | None = self.paginate_queryset(request, queryset)

		if results is None:
			return Response(
				TelegramBotVariableSerializer(queryset, many=True).data
			)
		else:
			return self.get_paginated_response(
				TelegramBotVariableSerializer(results, many=True).data
			)

	def post(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
		serializer = TelegramBotVariableSerializer(
			data=request.data,
			context={'telegram_bot': telegram_bot},
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно создали новую переменную Telegram бота.'),
			data={'telegram_bot_variable': serializer.data},
			status=201,
		)

class TelegramBotVariableAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotVariableIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, telegram_bot_variable: TelegramBotVariable) -> Response:
		return Response(TelegramBotVariableSerializer(telegram_bot_variable).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, telegram_bot_variable: TelegramBotVariable) -> Response:
		serializer = TelegramBotVariableSerializer(telegram_bot_variable, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно обновили переменную Telegram бота.'),
			data={'telegram_bot_variable': serializer.data},
		)

	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_variable: TelegramBotVariable) -> MessageResponse:
		telegram_bot_variable.delete()

		return MessageResponse(_('Вы успешно удалили переменную Telegram бота.'))

class TelegramBotUsersAPIView(APIView, PaginationMixin):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	pagination_class = LimitOffsetPagination

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		queryset: 'QuerySet[TelegramBotUser]' = telegram_bot.users.all()
		results: list[TelegramBotUser] | None = self.paginate_queryset(request, queryset)

		if results is None:
			return Response(
				TelegramBotUserSerializer(queryset, many=True).data
			)
		else:
			return self.get_paginated_response(
				TelegramBotUserSerializer(results, many=True).data
			)

class TelegramBotUserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotUserIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> Response:
		return Response(TelegramBotUserSerializer(telegram_bot_user).data)

	def post(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> Response:
		action: str | None = request.query_params.get('action')

		if action in ('allow', 'unallow', 'block', 'unblock'):
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

			return MessageResponse(success_messages[action])
		else:
			return MessageResponse(_('Не удалось найти и выполнить указанное действие в параметрах запроса!'), status=400)

	def delete(self, request: Request, telegram_bot: TelegramBot, telegram_bot_user: TelegramBotUser) -> MessageResponse:
		telegram_bot_user.delete()

		return MessageResponse(_('Вы успешно удалили пользователя Telegram бота.'))