from django.db.models import QuerySet

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from constructor_telegram_bots.mixins import IDLookupMixin

from ..models import (
    BackgroundTask,
    Command,
    CommandKeyboardButton,
    CommandTrigger,
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
    CommandKeyboardButtonSerializer,
    CommandSerializer,
    CommandTriggerSerializer,
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
        commands: QuerySet[Command] = self.telegram_bot.commands.all()

        if self.action in ['list', 'retrieve']:
            return commands.select_related(
                'settings',
                'message',
                'keyboard',
                'api_request',
                'database_record',
            ).prefetch_related(
                'images',
                'files',
                'keyboard__buttons__source_connections__source_object',
                'keyboard__buttons__source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return commands


class CommandTriggerViewSet(
    IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[CommandTrigger]
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommandTriggerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['text']

    def get_queryset(self) -> QuerySet[CommandTrigger]:
        return CommandTrigger.objects.filter(command__telegram_bot=self.telegram_bot)


class CommandKeyboardButtonViewSet(
    IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[CommandKeyboardButton]
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommandKeyboardButtonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'text']

    def get_queryset(self) -> QuerySet[CommandKeyboardButton]:
        return CommandKeyboardButton.objects.filter(
            keyboard__command__telegram_bot=self.telegram_bot
        ).prefetch_related(
            'source_connections__source_object',
            'source_connections__target_object',
        )


class ConditionViewSet(
    IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Condition]
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConditionSerializer

    def get_queryset(self) -> QuerySet[Condition]:
        conditions: QuerySet[Condition] = self.telegram_bot.conditions.all()

        if self.action in ['list', 'retrieve']:
            return conditions.prefetch_related(
                'parts',
                'source_connections__source_object',
                'source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return conditions


class BackgroundTaskViewSet(
    IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[BackgroundTask]
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BackgroundTaskSerializer

    def get_queryset(self) -> QuerySet[BackgroundTask]:
        background_tasks: QuerySet[BackgroundTask] = (
            self.telegram_bot.background_tasks.all()
        )

        if self.action in ['list', 'retrieve']:
            return background_tasks.select_related('api_request').prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
            )

        return background_tasks


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
    IDLookupMixin,
    TelegramBotMixin,
    CreateModelMixin,
    ReadOnlyModelViewSet[DatabaseRecord],
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DatabaseRecordSerializer

    def get_queryset(self) -> QuerySet[DatabaseRecord]:
        return self.telegram_bot.database_records.all()
