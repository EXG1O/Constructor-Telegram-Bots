from django.utils import timezone

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

        user, created = self.telegram_bot.users.get_or_create(
            telegram_id=telegram_id, defaults=validated_data
        )

        if not created:
            user.full_name = validated_data.get('full_name', user.full_name)
            user.last_activity_date = timezone.now()
            user.save(update_fields=['full_name', 'last_activity_date'])

        return user
