from django.db.models import QuerySet

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from constructor_telegram_bots.mixins import IDLookupMixin
from users.authentication import JWTCookieAuthentication

from ..models import DatabaseOperation
from ..serializers import (
    DatabaseOperationSerializer,
    DiagramDatabaseOperationSerializer,
)
from .mixins import TelegramBotMixin


class DatabaseOperationViewSet(
    IDLookupMixin, TelegramBotMixin, ModelViewSet[DatabaseOperation]
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DatabaseOperationSerializer

    def get_queryset(self) -> QuerySet[DatabaseOperation]:
        operations: QuerySet[DatabaseOperation] = (
            self.telegram_bot.database_operations.all()
        )

        if self.action in ['list', 'retrieve']:
            return operations.select_related(
                'create_operation', 'update_operation'
            ).prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return operations


class DiagramDatabaseOperationViewSet(
    IDLookupMixin,
    TelegramBotMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet[DatabaseOperation],
):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DiagramDatabaseOperationSerializer

    def get_queryset(self) -> QuerySet[DatabaseOperation]:
        operations: QuerySet[DatabaseOperation] = (
            self.telegram_bot.database_operations.all()
        )

        if self.action in ['list', 'retrieve']:
            return operations.prefetch_related(
                'source_connections__source_object',
                'source_connections__target_object',
                'target_connections__source_object',
                'target_connections__target_object',
            )

        return operations
