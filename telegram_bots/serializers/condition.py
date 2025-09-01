from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..models import Condition, ConditionPart
from .base import DiagramSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from typing import Any


class ConditionPartSerializer(serializers.ModelSerializer[ConditionPart]):
    class Meta:
        model = ConditionPart
        fields = [
            'id',
            'type',
            'first_value',
            'operator',
            'second_value',
            'next_part_operator',
        ]


class ConditionSerializer(TelegramBotMixin, serializers.ModelSerializer[Condition]):
    parts = ConditionPartSerializer(many=True)

    class Meta:
        model = Condition
        fields = ['id', 'name', 'parts']

    def validate_parts(self, parts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.partial and not parts:
            raise serializers.ValidationError(
                _('Условие должно содержать хотя бы одну часть.')
            )

        return parts

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if (
            not self.instance
            and self.telegram_bot.conditions.count() + 1
            > settings.TELEGRAM_BOT_MAX_CONDITIONS
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s условий.')
                % {'max': settings.TELEGRAM_BOT_MAX_CONDITIONS},
                code='max_limit',
            )

        return data

    def create(self, validated_data: dict[str, Any]) -> Condition:
        parts_data: list[dict[str, Any]] = validated_data.pop('parts')

        condition: Condition = self.telegram_bot.conditions.create(**validated_data)

        ConditionPart.objects.bulk_create(
            ConditionPart(condition=condition, **part_data) for part_data in parts_data
        )

        return condition

    def update(self, condition: Condition, validated_data: dict[str, Any]) -> Condition:
        condition.name = validated_data.get('name', condition.name)
        condition.save(update_fields=['name'])

        create_parts: list[ConditionPart] = []
        update_parts: list[ConditionPart] = []

        for part_data in validated_data.get('parts', []):
            try:
                part: ConditionPart = condition.parts.get(id=part_data['id'])
                part.type = part_data.get('type', part.type)
                part.first_value = part_data.get('first_value', part.first_value)
                part.operator = part_data.get('operator', part.operator)
                part.second_value = part_data.get('second_value', part.second_value)
                part.next_part_operator = part_data.get(
                    'next_part_operator', part.next_part_operator
                )

                update_parts.append(part)
            except (KeyError, ConditionPart.DoesNotExist):
                create_parts.append(ConditionPart(condition=condition, **part_data))

        new_parts: list[ConditionPart] = ConditionPart.objects.bulk_create(create_parts)
        ConditionPart.objects.bulk_update(
            update_parts,
            fields=[
                'type',
                'first_value',
                'operator',
                'second_value',
                'next_part_operator',
            ],
        )

        if not self.partial:
            condition.parts.exclude(
                id__in=[part.id for part in new_parts + update_parts]
            ).delete()

        return condition


class DiagramConditionSerializer(DiagramSerializer[Condition]):
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Condition
        fields = [
            'id',
            'name',
            'source_connections',
            'target_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name']
