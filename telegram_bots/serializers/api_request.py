from rest_framework import serializers

from ..mixins import TelegramBotContextMixin
from ..models import APIRequest
from .base import DiagramSerializer
from .connection import ConnectionSerializer

from typing import Any


class APIRequestSerializer(
    TelegramBotContextMixin, serializers.ModelSerializer[APIRequest]
):
    class Meta:
        model = APIRequest
        fields = ['id', 'name', 'url', 'method', 'headers', 'body']

    def create(self, validated_data: dict[str, Any]) -> APIRequest:
        return self.telegram_bot.api_requests.create(**validated_data)

    def update(
        self, api_request: APIRequest, validated_data: dict[str, Any]
    ) -> APIRequest:
        api_request.name = validated_data.get('name', api_request.name)
        api_request.url = validated_data.get('url', api_request.url)
        api_request.method = validated_data.get('method', api_request.method)
        api_request.headers = validated_data.get('headers', api_request.headers)
        api_request.body = validated_data.get('body', api_request.body)
        api_request.save(update_fields=['name', 'url', 'method', 'headers', 'body'])

        return api_request


class DiagramAPIRequestSerializer(DiagramSerializer[APIRequest]):
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = APIRequest
        fields = [
            'id',
            'name',
            'url',
            'method',
            'source_connections',
            'target_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name', 'url', 'method']
