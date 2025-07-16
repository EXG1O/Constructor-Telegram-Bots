from django.db.models import QuerySet

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from users.authentication import JWTCookieAuthentication

from ..models import BackgroundTask
from ..serializers import BackgroundTaskSerializer, DiagramBackgroundTaskSerializer
from .mixins import TelegramBotMixin


class BackgroundTaskViewSet(
    IDLookupMixin, TelegramBotMixin, ModelViewSet[BackgroundTask]
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BackgroundTaskSerializer

    def get_queryset(self) -> QuerySet[BackgroundTask]:
        background_tasks: QuerySet[BackgroundTask] = (
            self.telegram_bot.background_tasks.all()
        )

        if self.action in ['list', 'retrieve']:
            return background_tasks.prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
            )

        return background_tasks


class DiagramBackgroundTaskViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet[BackgroundTask],
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiagramBackgroundTaskSerializer

    def get_queryset(self) -> QuerySet[BackgroundTask]:
        background_tasks: QuerySet[BackgroundTask] = (
            self.telegram_bot.background_tasks.all()
        )

        if self.action in ['list', 'retrieve']:
            return background_tasks.prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
            )

        return background_tasks
