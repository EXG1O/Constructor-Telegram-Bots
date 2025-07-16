from django.db.models import QuerySet

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from constructor_telegram_bots.pagination import LimitOffsetPagination
from users.authentication import JWTCookieAuthentication

from ..models import Variable
from ..serializers import VariableSerializer
from .mixins import TelegramBotMixin


class VariableViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Variable]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VariableSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'name']
    ordering = ['-id']

    def get_queryset(self) -> QuerySet[Variable]:
        return self.telegram_bot.variables.all()
