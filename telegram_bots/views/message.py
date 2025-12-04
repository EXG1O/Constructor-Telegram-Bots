from django.db.models import QuerySet

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from constructor_telegram_bots.parsers import MultiPartJSONParser
from users.authentication import JWTCookieAuthentication

from ..models import Message
from ..serializers import DiagramMessageSerializer, MessageSerializer
from .mixins import TelegramBotMixin


class MessageViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Message]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartJSONParser]
    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet[Message]:
        messages: QuerySet[Message] = self.telegram_bot.messages.all()

        if self.action in ['list', 'retrieve']:
            return messages.select_related('settings', 'keyboard').prefetch_related(
                'images',
                'documents',
                'keyboard__buttons__source_connections__source_object',
                'keyboard__buttons__source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return messages


class DiagramMessageViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet[Message],
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiagramMessageSerializer

    def get_queryset(self) -> QuerySet[Message]:
        messages: QuerySet[Message] = self.telegram_bot.messages.all()

        if self.action in ['list', 'retrieve']:
            return messages.select_related('keyboard').prefetch_related(
                'keyboard__buttons__source_connections__source_object',
                'keyboard__buttons__source_connections__target_object',
                'source_connections__source_object',
                'source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return messages
