from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
	CreateModelMixin,
	DestroyModelMixin,
	ListModelMixin,
	RetrieveModelMixin,
	UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from constructor_telegram_bots.pagination import LimitOffsetPagination
from constructor_telegram_bots.parsers import MultiPartJSONParser

from .mixins import TelegramBotMixin
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
from .serializers import (
	BackgroundTaskSerializer,
	CommandSerializer,
	ConditionSerializer,
	ConnectionSerializer,
	DatabaseRecordSerializer,
	DiagramBackgroundTaskSerializer,
	DiagramCommandSerializer,
	DiagramConditionSerializer,
	TelegramBotSerializer,
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
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[TelegramBot]:
		return self.request.user.telegram_bots.all()  # type: ignore [union-attr]

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


class ConnectionViewSet(
	TelegramBotMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet[Connection]
):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = ConnectionSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[Connection]:
		return self.telegram_bot.connections.all()


class CommandViewSet(TelegramBotMixin, ModelViewSet[Command]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	parser_classes = [MultiPartJSONParser]
	serializer_class = CommandSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[Command]:
		return self.telegram_bot.commands.all()


class ConditionViewSet(TelegramBotMixin, ModelViewSet[Condition]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = ConditionSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[Condition]:
		return self.telegram_bot.conditions.all()


class BackgroundTaskViewSet(TelegramBotMixin, ModelViewSet[BackgroundTask]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = BackgroundTaskSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[BackgroundTask]:
		return self.telegram_bot.background_tasks.all()


class DiagramCommandViewSet(
	TelegramBotMixin,
	ListModelMixin,
	RetrieveModelMixin,
	UpdateModelMixin,
	GenericViewSet[Command],
):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = DiagramCommandSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[Command]:
		return self.telegram_bot.commands.all()


class DiagramConditionViewSet(
	TelegramBotMixin,
	ListModelMixin,
	RetrieveModelMixin,
	UpdateModelMixin,
	GenericViewSet[Condition],
):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = DiagramConditionSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[Condition]:
		return self.telegram_bot.conditions.all()


class DiagramBackgroundTaskViewSet(
	TelegramBotMixin,
	ListModelMixin,
	RetrieveModelMixin,
	UpdateModelMixin,
	GenericViewSet[BackgroundTask],
):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = DiagramBackgroundTaskSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'

	def get_queryset(self) -> QuerySet[BackgroundTask]:
		return self.telegram_bot.background_tasks.all()


class VariableViewSet(TelegramBotMixin, ModelViewSet[Variable]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = VariableSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['id', 'name']
	ordering = ['-id']

	def get_queryset(self) -> QuerySet[Variable]:
		return self.telegram_bot.variables.all()


class UserViewSet(
	TelegramBotMixin,
	ListModelMixin,
	RetrieveModelMixin,
	UpdateModelMixin,
	DestroyModelMixin,
	GenericViewSet[User],
):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
	search_fields = ['telegram_id', 'full_name']
	filterset_fields = ['is_allowed', 'is_blocked']
	ordering = ['-id']

	def get_queryset(self) -> QuerySet[User]:
		return self.telegram_bot.users.all()


class DatabaseRecordViewSet(TelegramBotMixin, ModelViewSet[DatabaseRecord]):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = DatabaseRecordSerializer
	lookup_value_converter = 'int'
	lookup_field = 'id'
	pagination_class = LimitOffsetPagination
	filter_backends = [SearchFilter]
	search_fields = ['data']

	def get_queryset(self) -> QuerySet[DatabaseRecord]:
		return self.telegram_bot.database_records.all()
