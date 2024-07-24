from django.db.models import QuerySet

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ..models import (
	BackgroundTask,
	Command,
	Condition,
	DatabaseRecord,
	TelegramBot,
	User,
	Variable,
)
from .authentication import TokenAuthentication
from .mixins import TelegramBotMixin
from .serializers import (
	BackgroundTaskSerializer,
	CommandSerializer,
	ConditionSerializer,
	DatabaseRecordSerializer,
	TelegramBotSerializer,
	UserSerializer,
	VariableSerializer,
)


class TelegramBotViewSet(IDLookupMixin, ReadOnlyModelViewSet[TelegramBot]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = TelegramBotSerializer

	def get_queryset(self) -> QuerySet[TelegramBot]:
		return TelegramBot.objects.all()


class CommandViewSet(IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Command]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = CommandSerializer

	def get_queryset(self) -> QuerySet[Command]:
		return self.telegram_bot.commands.all()


class ConditionViewSet(
	IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Condition]
):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = ConditionSerializer

	def get_queryset(self) -> QuerySet[Condition]:
		return self.telegram_bot.conditions.all()


class BackgroundTaskViewSet(
	IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[BackgroundTask]
):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = BackgroundTaskSerializer

	def get_queryset(self) -> QuerySet[BackgroundTask]:
		return self.telegram_bot.background_tasks.all()


class VariableViewSet(IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Variable]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = VariableSerializer

	def get_queryset(self) -> QuerySet[Variable]:
		return self.telegram_bot.variables.all()


class UserViewSet(
	IDLookupMixin, TelegramBotMixin, CreateModelMixin, ReadOnlyModelViewSet[User]
):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer

	def get_queryset(self) -> QuerySet[User]:
		return self.telegram_bot.users.all()


class DatabaseRecordViewSet(
	IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[DatabaseRecord]
):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = DatabaseRecordSerializer

	def get_queryset(self) -> QuerySet[DatabaseRecord]:
		return self.telegram_bot.database_records.all()
