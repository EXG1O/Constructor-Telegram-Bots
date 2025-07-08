from rest_framework import serializers
from rest_framework.request import Request

from users.models import User as SiteUser

from ..models import TelegramBot

from typing import Any


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
    class Meta:
        model = TelegramBot
        fields = [
            'id',
            'username',
            'api_token',
            'storage_size',
            'used_storage_size',
            'remaining_storage_size',
            'is_private',
            'is_enabled',
            'is_loading',
            'added_date',
        ]
        read_only_fields = [
            'id',
            'username',
            'storage_size',
            'used_storage_size',
            'remaining_storage_size',
            'is_enabled',
            'is_loading',
            'added_date',
        ]

    @property
    def site_user(self) -> SiteUser:
        request: Any = self.context.get('request')

        if not isinstance(request, Request):
            raise TypeError(
                'You not passed a rest_framework.request.Request instance '
                'as request to the serializer context.'
            )
        elif not isinstance(request.user, SiteUser):
            raise TypeError(
                'The request.user instance is not an users.models.User instance.'
            )

        return request.user

    def create(self, validated_data: dict[str, Any]) -> TelegramBot:
        return self.site_user.telegram_bots.create(**validated_data)

    def update(
        self, telegram_bot: TelegramBot, validated_data: dict[str, Any]
    ) -> TelegramBot:
        telegram_bot.api_token = validated_data.get('api_token', telegram_bot.api_token)
        telegram_bot.is_private = validated_data.get(
            'is_private', telegram_bot.is_private
        )
        telegram_bot.save(update_fields=['api_token', 'is_private'])

        return telegram_bot
