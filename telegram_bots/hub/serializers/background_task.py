from rest_framework import serializers

from ...models import BackgroundTask
from .connection import ConnectionSerializer


class BackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask]):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = BackgroundTask
        fields = ['id', 'interval', 'source_connections']
