from rest_framework import serializers

from ...models import (
    DatabaseCreateOperation,
    DatabaseOperation,
    DatabaseUpdateOperation,
)
from .connection import ConnectionSerializer


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


class DatabaseOperationSerializer(serializers.ModelSerializer[DatabaseOperation]):
    create_operation = DatabaseCreateOperationSerializer()
    update_operation = DatabaseUpdateOperationSerializer()
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = DatabaseOperation
        fields = ['id', 'create_operation', 'update_operation', 'source_connections']
