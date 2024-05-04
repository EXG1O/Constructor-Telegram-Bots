from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	ListCreateAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import (
	BackgroundTask,
	Command,
	Condition,
	Connection,
	DatabaseRecord,
	TelegramBot,
	User,
	Variable,
)
from .parsers import CommandMultiPartParser
from .permissions import (
	BackgroundTaskIsIsFound,
	CommandIsFound,
	ConditionIsIsFound,
	ConnectionIsFound,
	DatabaseRecordIsFound,
	TelegramBotIsFound,
	UserIsFound,
	VariableIsFound,
)
from .serializers import (
	BackgroundTaskSerializer,
	CommandSerializer,
	ConditionSerializer,
	ConnectionSerializer,
	CreateCommandSerializer,
	DatabaseRecordSerializer,
	DiagramBackgroundTaskSerializer,
	DiagramCommandSerializer,
	DiagramConditionSerializer,
	TelegramBotSerializer,
	UpdateCommandSerializer,
	UserSerializer,
	VariableSerializer,
)


class StatsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response(
			{
				'telegram_bots': {
					'total': TelegramBot.objects.count(),
					'enabled': TelegramBot.objects.filter(is_enabled=True).count(),
				},
				'users': {
					'total': User.objects.count(),
				},
			}
		)


class TelegramBotViewSet(ModelViewSet[TelegramBot]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = TelegramBotSerializer
	lookup_field = 'id'
	lookup_value_converter = 'int'

	def get_queryset(self) -> QuerySet[TelegramBot]:
		return self.request.user.telegram_bots.all()  # type: ignore [union-attr]

	def get_object(self) -> TelegramBot:
		return get_object_or_404(self.request.user.telegram_bots, id=self.kwargs['id'])  # type: ignore [union-attr]

	@action(detail=True, methods=['POST'])
	def start(self, request: Request, id: int | None = None) -> Response:
		telegram_bot: TelegramBot = self.get_object()
		telegram_bot.start()

		return Response(self.get_serializer(telegram_bot).data)

	@action(detail=True, methods=['POST'])
	def restart(self, request: Request, id: int | None = None) -> Response:
		telegram_bot: TelegramBot = self.get_object()
		telegram_bot.restart()

		return Response(self.get_serializer(telegram_bot).data)

	@action(detail=True, methods=['POST'])
	def stop(self, request: Request, id: int | None = None) -> Response:
		telegram_bot: TelegramBot = self.get_object()
		telegram_bot.stop()

		return Response(self.get_serializer(telegram_bot).data)


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
		return self.kwargs['telegram_bot'].commands.all()

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
		return self.kwargs['telegram_bot'].conditions.all()


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
		return self.kwargs['telegram_bot'].background_tasks.all()


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
		return self.kwargs['telegram_bot'].commands.all()


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
		return self.kwargs['telegram_bot'].conditions.all()


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
		return self.kwargs['telegram_bot'].background_tasks.all()


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
	search_fields = ['id', 'name']
	ordering = ['-id']

	def get_queryset(self) -> QuerySet[Variable]:
		return self.kwargs['telegram_bot'].variables.all()


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
	filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
	search_fields = ['telegram_id', 'full_name']
	filterset_fields = ['is_allowed', 'is_blocked']
	ordering = ['-id']

	def get_queryset(self) -> QuerySet[User]:
		return self.kwargs['telegram_bot'].users.all()


class UserAPIView(RetrieveUpdateDestroyAPIView[User]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & UserIsFound]
	serializer_class = UserSerializer

	def get_object(self) -> User:
		return self.kwargs['user']


class DatabaseRecordsAPIView(ListCreateAPIView[DatabaseRecord]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = DatabaseRecordSerializer
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter]
	search_fields = ['data']

	def get_queryset(self) -> QuerySet[DatabaseRecord]:
		return self.kwargs['telegram_bot'].database_records.all()


class DatabaseRecordAPIView(RetrieveUpdateDestroyAPIView[DatabaseRecord]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & DatabaseRecordIsFound]
	serializer_class = DatabaseRecordSerializer

	def get_object(self) -> DatabaseRecord:
		return self.kwargs['database_record']
