from rest_framework import serializers

from ..models import User

from typing import Any


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = [
            'id',
            'telegram_id',
            'first_name',
            'last_name',
            'is_allowed',
            'is_blocked',
            'activated_date',
        ]
        read_only_fields = ['telegram_id', 'first_name', 'last_name', 'activated_date']

    def update(self, user: User, validated_data: dict[str, Any]) -> User:
        user.is_allowed = validated_data.get('is_allowed', user.is_allowed)
        user.is_blocked = validated_data.get('is_blocked', user.is_blocked)
        user.save(update_fields=['is_allowed', 'is_blocked'])

        return user
