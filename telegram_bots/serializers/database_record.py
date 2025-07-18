from rest_framework import serializers

from ..models import DatabaseRecord
from .mixins import TelegramBotMixin

from typing import Any


class DatabaseRecordSerializer(
    TelegramBotMixin, serializers.ModelSerializer[DatabaseRecord]
):
    class Meta:
        model = DatabaseRecord
        fields = ['id', 'data']

    def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
        return self.telegram_bot.database_records.create(**validated_data)

    def update(
        self, database_record: DatabaseRecord, validated_data: dict[str, Any]
    ) -> DatabaseRecord:
        database_record.data = validated_data.get('data', database_record.data)
        database_record.save(update_fields=['data'])

        return database_record
