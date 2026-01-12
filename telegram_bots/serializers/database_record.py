from django.conf import settings
from django.utils.translation import gettext as _

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

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if (
            not self.instance
            and self.telegram_bot.database_records.count() + 1
            > settings.TELEGRAM_BOT_MAX_DATABASE_RECORDS
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s записей в базу данных.')
                % {'max': settings.TELEGRAM_BOT_MAX_DATABASE_RECORDS},
                code='max_limit',
            )

        return data

    def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
        return self.telegram_bot.database_records.create(**validated_data)

    def update(
        self, database_record: DatabaseRecord, validated_data: dict[str, Any]
    ) -> DatabaseRecord:
        database_record.data = validated_data.get('data', database_record.data)
        database_record.save(update_fields=['data'])

        return database_record
