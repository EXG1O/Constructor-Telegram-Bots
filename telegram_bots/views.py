from django.utils.translation import gettext as _
from django.db.models import QuerySet
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
	DestroyAPIView,
	ListCreateAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView,
)
from rest_framework.serializers import BaseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from constructor_telegram_bots.pagination import LimitOffsetPagination

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
from .parsers import CommandMultiPartParser
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
)

from typing import Literal


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

class TelegramBotsAPIView(ListCreateAPIView[TelegramBot]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = TelegramBotSerializer

	def get_queryset(self) -> QuerySet[TelegramBot]:
		return self.request.user.telegram_bots.all() # type: ignore [union-attr]

class TelegramBotAPIView(RetrieveUpdateDestroyAPIView[TelegramBot]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotSerializer

	def get_object(self) -> TelegramBot:
		return self.kwargs['telegram_bot']

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

class ConnectionsAPIView(CreateAPIView[Connection]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = ConnectionSerializer

class ConnectionAPIView(DestroyAPIView[Connection]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConnectionIsFound]

	def get_object(self) -> Connection:
		return self.kwargs['connection']

class CommandsAPIView(ListCreateAPIView[Command]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	parser_classes = [CommandMultiPartParser]

	def get_queryset(self) -> QuerySet[Command]:
		return self.kwargs['telegram_bot'].commands

	def get_serializer_class(self) -> type[BaseSerializer[Command]]:
		if self.request.method == 'POST':
			return CreateCommandSerializer
		else:
			return CommandSerializer

class CommandAPIView(RetrieveUpdateDestroyAPIView[Command]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]
	parser_classes = [CommandMultiPartParser]

	def get_object(self) -> Command:
		return self.kwargs['command']

	def get_serializer_class(self) -> type[BaseSerializer[Command]]:
		if self.request.method in ('PUT', 'PATCH'):
			return UpdateCommandSerializer
		else:
			return CommandSerializer

class ConditionsAPIView(ListCreateAPIView[Condition]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = ConditionSerializer

	def get_queryset(self) -> QuerySet[Condition]:
		return self.kwargs['telegram_bot'].conditions

class ConditionAPIView(RetrieveUpdateDestroyAPIView[Condition]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConditionIsIsFound]
	serializer_class = ConditionSerializer

	def get_object(self) -> Condition:
		return self.kwargs['condition']

class BackgroundTasksAPIView(ListCreateAPIView[BackgroundTask]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = BackgroundTaskSerializer

	def get_queryset(self) -> QuerySet[BackgroundTask]:
		return self.kwargs['telegram_bot'].background_tasks

class BackgroundTaskAPIView(RetrieveUpdateDestroyAPIView[BackgroundTask]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & BackgroundTaskIsIsFound]
	serializer_class = BackgroundTaskSerializer

	def get_object(self) -> BackgroundTask:
		return self.kwargs['background_task']

class DiagramCommandsAPIView(ListAPIView[Command]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = DiagramCommandSerializer

	def get_queryset(self) -> QuerySet[Command]:
		return self.kwargs['telegram_bot'].commands

class DiagramCommandAPIView(RetrieveUpdateAPIView[Command]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]
	serializer_class = DiagramCommandSerializer

	def get_object(self) -> Command:
		return self.kwargs['command']

class DiagramConditionsAPIView(ListAPIView[Condition]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = DiagramConditionSerializer

	def get_queryset(self) -> QuerySet[Condition]:
		return self.kwargs['telegram_bot'].conditions

class DiagramConditionAPIView(RetrieveUpdateAPIView[Condition]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & ConditionIsIsFound]
	serializer_class = DiagramConditionSerializer

	def get_object(self) -> Condition:
		return self.kwargs['condition']

class DiagramBackgroundTasksAPIView(ListAPIView[BackgroundTask]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = DiagramBackgroundTaskSerializer

	def get_queryset(self) -> QuerySet[BackgroundTask]:
		return self.kwargs['telegram_bot'].background_tasks

class DiagramBackgroundTaskAPIView(RetrieveUpdateAPIView[BackgroundTask]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & BackgroundTaskIsIsFound]
	serializer_class = DiagramBackgroundTaskSerializer

	def get_object(self) -> BackgroundTask:
		return self.kwargs['background_task']

class VariablesAPIView(ListCreateAPIView[Variable]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = VariableSerializer
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ('id', 'name')
	ordering = ('-id',)

	def get_queryset(self) -> QuerySet[Variable]:
		return self.kwargs['telegram_bot'].variables

class VariableAPIView(RetrieveUpdateDestroyAPIView[Variable]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & VariableIsFound]
	serializer_class = VariableSerializer

	def get_object(self) -> Variable:
		return self.kwargs['variable']

class UsersAPIView(ListAPIView[User]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = UserSerializer
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ('telegram_id', 'full_name')
	ordering_fields = ('is_allowed', 'is_blocked')
	ordering = ('-id',)

	def get_queryset(self) -> QuerySet[User]:
		return self.kwargs['telegram_bot'].users

class UserAPIView(RetrieveUpdateDestroyAPIView[User]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & UserIsFound]
	serializer_class = UserSerializer

	def get_object(self) -> User:
		return self.kwargs['user']