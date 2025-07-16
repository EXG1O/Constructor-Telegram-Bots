from django.db.models import QuerySet

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from users.authentication import JWTCookieAuthentication

from ..models import Connection
from ..serializers import ConnectionSerializer
from .mixins import TelegramBotMixin


class ConnectionViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet[Connection],
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self) -> QuerySet[Connection]:
        return self.telegram_bot.connections.all()
