from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import APIRequest
from .base import DiagramSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from typing import Any


class APIRequestSerializer(TelegramBotMixin, serializers.ModelSerializer[APIRequest]):
    class Meta:
        model = APIRequest
        fields = ['id', 'name', 'url', 'method', 'headers', 'body']

    def validate_headers(self, headers: list[Any] | dict[str, Any]) -> dict[str, str]:
        if not isinstance(headers, dict):
            raise serializers.ValidationError(_('Заголовки должны быть словарем.'))

        for key, value in headers.items():
            if not isinstance(value, str):
                raise serializers.ValidationError(
                    _("Значение для заголовка '%(key)s' должно быть строкой.")
                    % {'key': key}
                )

        return headers

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if (
            not self.instance
            and self.telegram_bot.api_requests.count() + 1
            > settings.TELEGRAM_BOT_MAX_API_REQUESTS
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s API-запросов.')
                % {'max': settings.TELEGRAM_BOT_MAX_API_REQUESTS},
                code='max_limit',
            )

        return data

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

    class Meta:
        model = APIRequest
        fields = [
            'id',
            'name',
            'url',
            'method',
            'source_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name', 'url', 'method']
