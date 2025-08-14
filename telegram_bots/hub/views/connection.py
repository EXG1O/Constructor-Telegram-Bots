from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import Connection
from ..authentication import TokenAuthentication
from ..serializers import ConnectionSerializer
from .mixins import TelegramBotMixin


class ConnectionViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    ReadOnlyModelViewSet[Connection],
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self) -> QuerySet[Connection]:
        return self.telegram_bot.connections.all()
