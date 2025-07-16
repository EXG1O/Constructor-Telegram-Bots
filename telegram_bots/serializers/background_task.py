from rest_framework import serializers

from ..models import BackgroundTask
from .base import DiagramSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from typing import Any


class BackgroundTaskSerializer(
    TelegramBotMixin, serializers.ModelSerializer[BackgroundTask]
):
    class Meta:
        model = BackgroundTask
        fields = ['id', 'name', 'interval']

    def create(self, validated_data: dict[str, Any]) -> BackgroundTask:
        return self.telegram_bot.background_tasks.create(**validated_data)

    def update(
        self, background_task: BackgroundTask, validated_data: dict[str, Any]
    ) -> BackgroundTask:
        background_task.name = validated_data.get('name', background_task.name)
        background_task.interval = validated_data.get(
            'interval', background_task.interval
        )
        background_task.save(update_fields=['name', 'interval'])

        return background_task


class DiagramBackgroundTaskSerializer(DiagramSerializer[BackgroundTask]):
    source_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = BackgroundTask
        fields = [
            'id',
            'name',
            'interval',
            'source_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name', 'interval']
