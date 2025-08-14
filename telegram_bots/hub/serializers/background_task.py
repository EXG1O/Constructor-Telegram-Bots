from rest_framework import serializers

from ...models import BackgroundTask
from .connection import ConnectionSerializer


class BackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask]):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = BackgroundTask
        fields = ['id', 'name', 'interval', 'source_connections']
