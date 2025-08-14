from rest_framework import serializers

from ...models import Condition, ConditionPart
from .connection import ConnectionSerializer


class ConditionPartSerializer(serializers.ModelSerializer[ConditionPart]):
    class Meta:
        model = ConditionPart
        fields = [
            'id',
            'type',
            'first_value',
            'operator',
            'second_value',
            'next_part_operator',
        ]


class ConditionSerializer(serializers.ModelSerializer[Condition]):
    parts = ConditionPartSerializer(many=True)
    source_connections = ConnectionSerializer(many=True)
    target_connections = ConnectionSerializer(many=True)

    class Meta:
        model = Condition
        fields = ['id', 'name', 'parts', 'source_connections', 'target_connections']
