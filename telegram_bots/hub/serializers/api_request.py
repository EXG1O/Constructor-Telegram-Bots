from rest_framework import serializers

from ...models import APIRequest
from .connection import ConnectionSerializer


class APIRequestSerializer(serializers.ModelSerializer[APIRequest]):
    source_connections = ConnectionSerializer(many=True)
    target_connections = ConnectionSerializer(many=True)

    class Meta:
        model = APIRequest
        fields = [
            'id',
            'name',
            'url',
            'method',
            'headers',
            'body',
            'source_connections',
            'target_connections',
        ]
