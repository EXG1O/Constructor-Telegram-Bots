from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import Command, CommandKeyboardButton
from ..authentication import TokenAuthentication
from ..serializers import CommandKeyboardButtonSerializer, CommandSerializer
from .mixins import TelegramBotMixin


class CommandViewSet(IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Command]):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommandSerializer

    def get_queryset(self) -> QuerySet[Command]:
        commands: QuerySet[Command] = self.telegram_bot.commands.all()

        if self.action in ['list', 'retrieve']:
            return commands.select_related(
                'settings', 'message', 'keyboard'
            ).prefetch_related(
                'images',
                'documents',
                'keyboard__buttons__source_connections__source_object',
                'keyboard__buttons__source_connections__target_object',
                'source_connections__source_object',
                'source_connections__target_object',
            )

        return commands


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
