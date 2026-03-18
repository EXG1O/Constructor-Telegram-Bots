from rest_framework import serializers

from ...models import TemporaryVariable
from .connection import ConnectionSerializer


class TemporaryVariableSerializer(serializers.ModelSerializer[TemporaryVariable]):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = TemporaryVariable
        fields = ['id', 'name', 'value', 'source_connections']
