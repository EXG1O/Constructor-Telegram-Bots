from django.utils.translation import gettext as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import QuerySet
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from constructor_telegram_bots.mixins import PaginationMixin

from .models import (
	TelegramBot,
	Connection,
	Command,
	Condition,
	BackgroundTask,
	Variable,
	User,
)
from .permissions import (
	TelegramBotIsFound,
	ConnectionIsFound,
	CommandIsFound,
	ConditionIsIsFound,
	BackgroundTaskIsIsFound,
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
	ConditionSerializer,
	BackgroundTaskSerializer,
	DiagramCommandSerializer,
	DiagramConditionSerializer,
	DiagramBackgroundTaskSerializer,
	VariableSerializer,
	UserSerializer,
	UserActionSerializer,
)

import json
from json import JSONDecodeError

from typing import Literal, Any


class StatsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response({
			'telegram_bots': {
				'total': TelegramBot.objects.count(),
				'enabled': TelegramBot.objects.filter(is_enabled=True).count(),
			},
			'users': {
				'total': User.objects.count(),
			},
		})

class TelegramBotsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		return Response(TelegramBotSerializer(request.user.telegram_bots.all(), many=True).data) # type: ignore [union-attr]

	def post(self, request: Request) -> Response:
		serializer = TelegramBotSerializer(data=request.data, context={'site_user': request.user})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class TelegramBotAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(TelegramBotSerializer(telegram_bot).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = TelegramBotActionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		if not settings.TEST:
			action: Literal['start', 'restart', 'stop'] = serializer.validated_data['action']

			if action == 'start':
				telegram_bot.start()
			elif action == 'restart':
				telegram_bot.restart()
			else:
				telegram_bot.stop()

		return Response()

	def patch(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = TelegramBotSerializer(telegram_bot, request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

	def delete(self, request: Request, telegram_bot: TelegramBot) -> Response:
		telegram_bot.delete()

		return Response()

class ConnectionsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = ConnectionSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class ConnectionAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConnectionIsFound]

	def delete(self, request: Request, telegram_bot: TelegramBot, connection: Connection) -> Response:
		connection.delete()

		return Response()

class CommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(CommandSerializer(telegram_bot.commands.all(), many=True).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		try:
			data: dict[str, Any] = json.loads(request.data['data'])
		except (KeyError, JSONDecodeError):
			raise ParseError()

		sorted_files: dict[str, list[InMemoryUploadedFile]] = {
			'images': [],
			'files': [],
		}

		for key, file in request.FILES.items():
			_type: str = f"{key.split(':')[0]}s"

			if _type in sorted_files:
				sorted_files[_type].append(file)

		data.update(sorted_files)

		serializer = CreateCommandSerializer(data=data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class CommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		return Response(CommandSerializer(command).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		try:
			data: dict[str, Any] = json.loads(request.data['data'])
		except (KeyError, JSONDecodeError):
			raise ParseError()

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

		data.update(sorted_files)

		serializer = UpdateCommandSerializer(command, data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

	def delete(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		command.delete()

		return Response()

class ConditionsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(ConditionSerializer(telegram_bot.conditions, many=True).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = ConditionSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class ConditionAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConditionIsIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, condition: Condition) -> Response:
		return Response(ConditionSerializer(condition).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, condition: Condition) -> Response:
		serializer = ConditionSerializer(condition, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

	def delete(self, request: Request, telegram_bot: TelegramBot, condition: Condition) -> Response:
		condition.delete()

		return Response()

class BackgroundTasksAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(BackgroundTaskSerializer(telegram_bot.background_tasks, many=True).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = BackgroundTaskSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class BackgroundTaskAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & BackgroundTaskIsIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, background_task: BackgroundTask) -> Response:
		return Response(BackgroundTaskSerializer(background_task).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, background_task: BackgroundTask) -> Response:
		serializer = BackgroundTaskSerializer(background_task, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

	def delete(self, request: Request, telegram_bot: TelegramBot, background_task: BackgroundTask) -> Response:
		background_task.delete()

		return Response()

class DiagramCommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(DiagramCommandSerializer(telegram_bot.commands.all(), many=True).data)

class DiagramCommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]

	def patch(self, request: Request, telegram_bot: TelegramBot, command: Command) -> Response:
		serializer = DiagramCommandSerializer(command, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response()

class DiagramConditionsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(DiagramConditionSerializer(telegram_bot.conditions, many=True).data)

class DiagramConditionAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConditionIsIsFound]

	def patch(self, request: Request, telegram_bot: TelegramBot, condition: Condition) -> Response:
		serializer = DiagramConditionSerializer(condition, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response()

class DiagramBackgroundTasksAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(DiagramBackgroundTaskSerializer(telegram_bot.background_tasks, many=True).data)

class DiagramBackgroundTaskAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & BackgroundTaskIsIsFound]

	def patch(self, request: Request, telegram_bot: TelegramBot, background_task: BackgroundTask) -> Response:
		serializer = DiagramBackgroundTaskSerializer(background_task, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response()

class VariablesAPIView(APIView, PaginationMixin):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	pagination_class = LimitOffsetPagination

	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		name: str | None = request.query_params.get('name')
		queryset: QuerySet[Variable]

		if name:
			queryset = telegram_bot.variables.filter(name__icontains=name)
		else:
			queryset = telegram_bot.variables.all()

		results: list[Variable] | None = self.paginate_queryset(request, queryset.order_by('-id'))

		if results is None:
			return Response(VariableSerializer(queryset, many=True).data)
		else:
			return self.get_paginated_response(VariableSerializer(results, many=True).data)

	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = VariableSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class VariableAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & VariableIsFound]

	def get(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> Response:
		return Response(VariableSerializer(variable).data)

	def patch(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> Response:
		serializer = VariableSerializer(variable, request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data)

	def delete(self, request: Request, telegram_bot: TelegramBot, variable: Variable) -> Response:
		variable.delete()

		return Response()

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

		return Response()

	def delete(self, request: Request, telegram_bot: TelegramBot, user: User) -> Response:
		user.delete()

		return Response()