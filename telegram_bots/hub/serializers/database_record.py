from rest_framework import serializers

from ...models import DatabaseRecord
from ...serializers.mixins import TelegramBotMixin

from typing import Any


class DatabaseRecordSerializer(
    TelegramBotMixin, serializers.ModelSerializer[DatabaseRecord]
):
    class Meta:
        model = DatabaseRecord
        fields = ['id', 'data']

    def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
        return self.telegram_bot.database_records.create(**validated_data)
