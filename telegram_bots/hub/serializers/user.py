from django.utils import timezone

from rest_framework import serializers

from ...models import User
from ...serializers.mixins import TelegramBotMixin

from typing import Any


class UserSerializer(TelegramBotMixin, serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            'id',
            'telegram_id',
            'username',
            'first_name',
            'last_name',
            'is_bot',
            'is_premium',
            'is_allowed',
            'is_blocked',
        ]
        read_only_fields = ['is_allowed', 'is_blocked']

    def create(self, validated_data: dict[str, Any]) -> User:
        telegram_id: int = validated_data.pop('telegram_id')

        user, created = self.telegram_bot.users.get_or_create(
            telegram_id=telegram_id, defaults=validated_data
        )

        if not created:
            user.username = validated_data.get('username', user.username)
            user.first_name = validated_data.get('first_name', user.first_name)
            user.last_name = validated_data.get('last_name', user.last_name)
            user.is_bot = validated_data.get('is_bot', user.is_bot)
            user.is_premium = validated_data.get('is_premium', user.is_premium)
            user.last_activity_date = timezone.now()
            user.save(
                update_fields=[
                    'username',
                    'first_name',
                    'last_name',
                    'is_bot',
                    'is_premium',
                    'last_activity_date',
                ]
            )

        return user
