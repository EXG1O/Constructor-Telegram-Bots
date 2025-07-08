from rest_framework import serializers

from ..mixins import TelegramBotContextMixin
from ..models import BackgroundTask, BackgroundTaskAPIRequest
from .base import DiagramSerializer
from .connection import ConnectionSerializer

from contextlib import suppress
from typing import Any


class BackgroundTaskAPIRequestSerializer(
    serializers.ModelSerializer[BackgroundTaskAPIRequest]
):
    class Meta:
        model = BackgroundTaskAPIRequest
        fields = ['url', 'method', 'headers', 'body']


class BackgroundTaskSerializer(
    TelegramBotContextMixin, serializers.ModelSerializer[BackgroundTask]
):
    api_request = BackgroundTaskAPIRequestSerializer(required=False, allow_null=True)

    class Meta:
        model = BackgroundTask
        fields = ['id', 'name', 'interval', 'api_request']

    def create(self, validated_data: dict[str, Any]) -> BackgroundTask:
        api_request: dict[str, Any] | None = validated_data.pop('api_request', None)

        background_task: BackgroundTask = self.telegram_bot.background_tasks.create(
            **validated_data
        )

        if api_request:
            BackgroundTaskAPIRequest.objects.create(
                background_task=background_task, **api_request
            )

        return background_task

    def update(
        self, background_task: BackgroundTask, validated_data: dict[str, Any]
    ) -> BackgroundTask:
        api_request: dict[str, Any] | None = validated_data.get('api_request')

        background_task.name = validated_data.get('name', background_task.name)
        background_task.interval = validated_data.get(
            'interval', background_task.interval
        )
        background_task.save(update_fields=['name', 'interval'])

        if api_request:
            try:
                background_task.api_request.url = api_request.get(
                    'url', background_task.api_request.url
                )
                background_task.api_request.method = api_request.get(
                    'method', background_task.api_request.method
                )
                background_task.api_request.headers = api_request.get(
                    'headers', background_task.api_request.headers
                )
                background_task.api_request.body = api_request.get(
                    'body', background_task.api_request.body
                )
                background_task.api_request.save(
                    update_fields=['url', 'method', 'headers', 'body']
                )
            except BackgroundTaskAPIRequest.DoesNotExist:
                BackgroundTaskAPIRequest.objects.create(
                    background_task=background_task, **api_request
                )
        elif not self.partial:
            with suppress(BackgroundTaskAPIRequest.DoesNotExist):
                background_task.api_request.delete()

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
