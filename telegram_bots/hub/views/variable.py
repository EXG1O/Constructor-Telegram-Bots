from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import Variable
from ..authentication import TokenAuthentication
from ..serializers import VariableSerializer
from .mixins import TelegramBotMixin


class VariableViewSet(IDLookupMixin, TelegramBotMixin, ModelViewSet[Variable]):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VariableSerializer

    def get_queryset(self) -> QuerySet[Variable]:
        return self.telegram_bot.variables.all()
