from django.utils.translation import gettext as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.conf import settings

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
	Connection,
	Command,
	Variable,
	User,
)
from .permissions import (
	TelegramBotIsFound,
	ConnectionIsFound,
	CommandIsFound,
	VariableIsFound,
	UserIsFound,
)
from .serializers import (
	TelegramBotSerializer,
	TelegramBotActionSerializer,
	ConnectionSerializer,
	CommandSerializer,
	CreateCommandSerializer,
	UpdateCommandSerializer,
	DiagramCommandSerializer,
	VariableSerializer,
	UserSerializer,
	UserActionSerializer,
)

from typing import Literal, Any
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
		serializer = TelegramBotSerializer(data=request.data, context={'site_user': request.user})
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
		serializer = TelegramBotActionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		action: Literal['start', 'restart', 'stop'] = serializer.validated_data['action']

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

class CommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(
			CommandSerializer(
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

		serializer = CreateCommandSerializer(data=data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно добавили команду Telegram боту.'),
			data={'telegram_bot_command': serializer.data},
			status=201,
		)

class CommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		return Response(CommandSerializer(command).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, command: Command) -> MessageResponse:
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

		serializer = UpdateCommandSerializer(command, data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно изменили команду Telegram бота.'),
			data={'telegram_bot_command': serializer.data},
		)

	def delete(self, request: Request, telegram_bot: TelegramBot, command: Command) -> MessageResponse:
		command.delete()

		return MessageResponse(_('Вы успешно удалили команду Telegram бота.'))

class DiagramCommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(
			DiagramCommandSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

class DiagramCommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]

	def patch(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		serializer = DiagramCommandSerializer(command, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response()

class ConnectionsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def post(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
		serializer = ConnectionSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(_('Вы успешно подключили блок диаграммы к другому блоку'))

class ConnectionAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConnectionIsFound]

	def delete(self, request: Request, telegram_bot: TelegramBot, connection: Connection) -> MessageResponse:
		connection.delete()

		return MessageResponse(_('Вы успешно отсоединили блок диаграммы от другого блока'))

class VariablesAPIView(APIView, PaginationMixin):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	pagination_class = LimitOffsetPagination

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		queryset: 'QuerySet[Variable]' = telegram_bot.variables.all()
		results: list[Variable] | None = self.paginate_queryset(request, queryset)

		if results is None:
			return Response(VariableSerializer(queryset, many=True).data)
		else:
			return self.get_paginated_response(VariableSerializer(results, many=True).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> MessageResponse:
		serializer = VariableSerializer(
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

class VariableAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & VariableIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> Response:
		return Response(VariableSerializer(variable).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> Response:
		serializer = VariableSerializer(variable, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return MessageResponse(
			_('Вы успешно обновили переменную Telegram бота.'),
			data={'telegram_bot_variable': serializer.data},
		)

	def delete(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> MessageResponse:
		variable.delete()

		return MessageResponse(_('Вы успешно удалили переменную Telegram бота.'))

class UsersAPIView(APIView, PaginationMixin):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	pagination_class = LimitOffsetPagination

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		queryset: 'QuerySet[User]' = telegram_bot.users.all()
		results: list[User] | None = self.paginate_queryset(request, queryset)

		if results is None:
			return Response(UserSerializer(queryset, many=True).data)
		else:
			return self.get_paginated_response(UserSerializer(results, many=True).data)

class UserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & UserIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, user: User) -> Response:
		return Response(UserSerializer(user).data)

	def post(self, request: Request, telegram_bot: TelegramBot, user: User) -> Response:
		serializer = UserActionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		action: Literal['allow', 'unallow', 'block', 'unblock'] = serializer.validated_data['action']

		if action == 'allow':
			user.is_allowed = True
		elif action == 'unallow':
			user.is_allowed = False
		elif action == 'block':
			user.is_blocked = True
		else:
			user.is_blocked = False

		user.save()

		success_messages = {
			'allow': _('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.'),
			'unallow': _('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.'),
			'block': _('Вы успешно добавили пользователя в список заблокированных пользователей Telegram бота.'),
			'unblock': _('Вы успешно удалили пользователя из списка заблокированных пользователей Telegram бота.'),
		}

		return MessageResponse(success_messages[action])

	def delete(self, request: Request, telegram_bot: TelegramBot, user: User) -> MessageResponse:
		user.delete()

		return MessageResponse(_('Вы успешно удалили пользователя Telegram бота.'))