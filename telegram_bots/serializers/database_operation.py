from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import DatabaseCreateOperation, DatabaseOperation, DatabaseUpdateOperation
from .base import DiagramSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from contextlib import suppress
from typing import Any


class DatabaseCreateOperationSerializer(
    serializers.ModelSerializer[DatabaseCreateOperation]
):
    class Meta:
        model = DatabaseCreateOperation
        fields = ['data']


class DatabaseUpdateOperationSerializer(
    serializers.ModelSerializer[DatabaseUpdateOperation]
):
    class Meta:
        model = DatabaseUpdateOperation
        fields = [
            'overwrite',
            'lookup_field_name',
            'lookup_field_value',
            'create_if_not_found',
            'new_data',
        ]


class DatabaseOperationSerializer(
    TelegramBotMixin, serializers.ModelSerializer[DatabaseOperation]
):
    create_operation = DatabaseCreateOperationSerializer(
        required=False, allow_null=True
    )
    update_operation = DatabaseUpdateOperationSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = DatabaseOperation
        fields = ['id', 'name', 'create_operation', 'update_operation']

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if bool(data.get('create_operation')) is bool(data.get('update_operation')):
            raise serializers.ValidationError(
                _(
                    "Необходимо указать только одно из полей: 'create_operation' "
                    "или 'update_operation'."
                )
            )

        return data

    def create_create_operation(
        self, operation: DatabaseOperation, data: dict[str, Any]
    ) -> DatabaseCreateOperation:
        return DatabaseCreateOperation.objects.create(operation=operation, **data)

    def create_update_operation(
        self, operation: DatabaseOperation, data: dict[str, Any]
    ) -> DatabaseUpdateOperation:
        return DatabaseUpdateOperation.objects.create(operation=operation, **data)

    def create(self, validated_data: dict[str, Any]) -> DatabaseOperation:
        create_operation_data: dict[str, Any] | None = validated_data.pop(
            'create_operation', None
        )
        update_operation_data: dict[str, Any] | None = validated_data.pop(
            'update_operation', None
        )

        operation: DatabaseOperation = self.telegram_bot.database_operations.create(
            **validated_data
        )

        if create_operation_data:
            self.create_create_operation(operation, create_operation_data)
        elif update_operation_data:
            self.create_update_operation(operation, update_operation_data)

        return operation

    def update_create_operation(
        self, operation: DatabaseOperation, data: dict[str, Any] | None
    ) -> DatabaseCreateOperation | None:
        if not data:
            if not self.partial:
                with suppress(DatabaseCreateOperation.DoesNotExist):
                    operation.create_operation.delete()
            return None

        try:
            create_operation: DatabaseCreateOperation = operation.create_operation
            create_operation.data = data.get('data', create_operation.data)
            create_operation.save(update_fields=['data'])
            return create_operation
        except DatabaseCreateOperation.DoesNotExist:
            return self.create_create_operation(operation, data)

    def update_update_operation(
        self, operation: DatabaseOperation, data: dict[str, Any] | None
    ) -> DatabaseUpdateOperation | None:
        if not data:
            if not self.partial:
                with suppress(DatabaseUpdateOperation.DoesNotExist):
                    operation.update_operation.delete()
            return None

        try:
            update_operation: DatabaseUpdateOperation = operation.update_operation
            update_operation.overwrite = data.get(
                'overwrite', update_operation.overwrite
            )
            update_operation.lookup_field_name = data.get(
                'lookup_field_name', update_operation.lookup_field_name
            )
            update_operation.lookup_field_value = data.get(
                'lookup_field_value', update_operation.lookup_field_value
            )
            update_operation.create_if_not_found = data.get(
                'create_if_not_found', update_operation.create_if_not_found
            )
            update_operation.new_data = data.get('new_data', update_operation.new_data)
            update_operation.save(
                update_fields=[
                    'overwrite',
                    'lookup_field_name',
                    'lookup_field_value',
                    'create_if_not_found',
                    'new_data',
                ]
            )
            return update_operation
        except DatabaseUpdateOperation.DoesNotExist:
            return self.create_update_operation(operation, data)

    def update(
        self, operation: DatabaseOperation, validated_data: dict[str, Any]
    ) -> DatabaseOperation:
        operation.name = validated_data.get('name', operation.name)
        operation.save(update_fields=['name'])

        self.update_create_operation(operation, validated_data.get('create_operation'))
        self.update_update_operation(operation, validated_data.get('update_operation'))

        operation.refresh_from_db()

        return operation


class DiagramDatabaseOperationSerializer(DiagramSerializer[DatabaseOperation]):
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = DatabaseOperation
        fields = [
            'id',
            'name',
            'source_connections',
            'target_connections',
            *DiagramSerializer.Meta.fields,
        ]
        read_only_fields = ['name']
