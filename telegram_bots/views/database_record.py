from django.db.models import QuerySet

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from constructor_telegram_bots.pagination import LimitOffsetPagination
from users.authentication import JWTAuthentication

from ..models import DatabaseRecord
from ..serializers import DatabaseRecordSerializer
from .mixins import TelegramBotMixin


class DatabaseRecordViewSet(
    IDLookupMixin, TelegramBotMixin, ModelViewSet[DatabaseRecord]
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DatabaseRecordSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['data']
    ordering = ['-id']

    def get_queryset(self) -> QuerySet[DatabaseRecord]:
        return self.telegram_bot.database_records.all()
