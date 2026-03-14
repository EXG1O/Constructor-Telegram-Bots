from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import TemporaryVariable
from .base import DiagramSerializer
from .mixins import TelegramBotMixin

from typing import Any


class TemporaryVariableSerializer(
    TelegramBotMixin, serializers.ModelSerializer[TemporaryVariable]
):
    class Meta:
        model = TemporaryVariable
        fields = ['id', 'name', 'value']

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if (
            not self.instance
            and self.telegram_bot.temporary_variables.count() + 1
            > settings.TELEGRAM_BOT_MAX_TEMPORARY_VARIABLES
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s временных переменных.')
                % {'max': settings.TELEGRAM_BOT_MAX_TEMPORARY_VARIABLES},
                code='max_limit',
            )

        return data

    def create(self, validated_data: dict[str, Any]) -> TemporaryVariable:
        return self.telegram_bot.temporary_variables.create(**validated_data)

    def update(
        self, temporary_variable: TemporaryVariable, validated_data: dict[str, Any]
    ) -> TemporaryVariable:
        temporary_variable.name = validated_data.get('name', temporary_variable.name)
        temporary_variable.value = validated_data.get('value', temporary_variable.value)
        temporary_variable.save(update_fields=['name', 'value'])

        return temporary_variable


class DiagramTemporaryVariableSerializer(DiagramSerializer[TemporaryVariable]):
    class Meta(DiagramSerializer.Meta):
        model = TemporaryVariable
        fields = DiagramSerializer.Meta.fields + ['value']
        read_only_fields = DiagramSerializer.Meta.read_only_fields + ['value']
