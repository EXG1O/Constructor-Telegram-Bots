from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import TelegramBot
from ..authentication import TokenAuthentication
from ..serializers import TelegramBotSerializer


class TelegramBotViewSet(IDLookupMixin, ReadOnlyModelViewSet[TelegramBot]):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramBotSerializer

    def get_queryset(self) -> QuerySet[TelegramBot]:
        return TelegramBot.objects.all()
