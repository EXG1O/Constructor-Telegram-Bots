from django.db.models import QuerySet

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import DatabaseRecord
from ..authentication import TokenAuthentication
from ..serializers import DatabaseRecordSerializer
from .mixins import TelegramBotMixin


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
