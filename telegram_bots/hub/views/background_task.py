from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin

from ...models import BackgroundTask
from ..authentication import TokenAuthentication
from ..serializers import BackgroundTaskSerializer
from .mixins import TelegramBotMixin


class BackgroundTaskViewSet(
    IDLookupMixin, TelegramBotMixin, ReadOnlyModelViewSet[BackgroundTask]
):
    authentication_classes = [TokenAuthentication]
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
