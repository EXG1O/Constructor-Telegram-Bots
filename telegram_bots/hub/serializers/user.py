from rest_framework import serializers

from ...models import User
from ...serializers.mixins import TelegramBotMixin

from typing import Any


class UserSerializer(TelegramBotMixin, serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked']
        read_only_fields = ['is_allowed', 'is_blocked']

    def create(self, validated_data: dict[str, Any]) -> User:
        telegram_id: int = validated_data.pop('telegram_id')

        return self.telegram_bot.users.get_or_create(
            telegram_id=telegram_id, defaults=validated_data
        )[0]
