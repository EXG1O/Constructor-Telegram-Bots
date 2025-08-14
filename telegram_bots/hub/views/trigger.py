from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import Trigger
from ..authentication import TokenAuthentication
from ..serializers import TriggerSerializer
from .mixins import TelegramBotMixin


class TriggerViewSet(IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[Trigger]):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TriggerSerializer

    def get_queryset(self) -> QuerySet[Trigger]:
        triggers: QuerySet[Trigger] = self.telegram_bot.triggers.all()

        if self.action in ['list', 'retrieve']:
            return triggers.select_related('command', 'message')

        return triggers
