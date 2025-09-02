from django.db.models import QuerySet

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from users.authentication import JWTCookieAuthentication

from ..models import TelegramBot
from ..serializers import TelegramBotSerializer


class TelegramBotViewSet(IDLookupMixin, ModelViewSet[TelegramBot]):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramBotSerializer

    def get_queryset(self) -> QuerySet[TelegramBot]:
        return self.request.user.telegram_bots.all()  # type: ignore [union-attr]

    @action(detail=True, methods=['POST'])
    def start(self, request: Request, id: int) -> Response:
        telegram_bot: TelegramBot = self.get_object()
        telegram_bot.start()

        return Response(self.get_serializer(telegram_bot).data)

    @action(detail=True, methods=['POST'])
    def restart(self, request: Request, id: int) -> Response:
        telegram_bot: TelegramBot = self.get_object()
        telegram_bot.restart()

        return Response(self.get_serializer(telegram_bot).data)

    @action(detail=True, methods=['POST'])
    def stop(self, request: Request, id: int) -> Response:
        telegram_bot: TelegramBot = self.get_object()
        telegram_bot.stop()

        return Response(self.get_serializer(telegram_bot).data)
