from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from users.authentication import JWTCookieAuthentication

from ..mixins import TelegramBotMixin
from ..models import Trigger
from ..serializers import DiagramTriggerSerializer, TriggerSerializer


class TriggerViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Trigger]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TriggerSerializer

    def get_queryset(self) -> QuerySet[Trigger]:
        triggers: QuerySet[Trigger] = self.telegram_bot.triggers.all()

        if self.action in ['list', 'retrieve']:
            return triggers.select_related('command', 'message')

        return triggers


class DiagramTriggerViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Trigger]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiagramTriggerSerializer

    def get_queryset(self) -> QuerySet[Trigger]:
        triggers: QuerySet[Trigger] = self.telegram_bot.triggers.all()

        if self.action in ['list', 'retrieve']:
            return triggers.prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
            )

        return triggers
