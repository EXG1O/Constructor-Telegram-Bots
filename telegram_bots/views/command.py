from django.db.models import QuerySet

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from constructor_telegram_bots.parsers import MultiPartJSONParser
from users.authentication import JWTCookieAuthentication

from ..models import Command
from ..serializers import CommandSerializer, DiagramCommandSerializer
from .mixins import TelegramBotMixin


class CommandViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Command]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartJSONParser]
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
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return commands


class DiagramCommandViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet[Command],
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiagramCommandSerializer

    def get_queryset(self) -> QuerySet[Command]:
        commands: QuerySet[Command] = self.telegram_bot.commands.all()

        if self.action in ['list', 'retrieve']:
            return commands.select_related('message', 'keyboard').prefetch_related(
                'keyboard__buttons__source_connections__source_object',
                'keyboard__buttons__source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return commands
