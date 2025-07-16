from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..enums import ConnectionObjectType
from ..models import (
    BackgroundTask,
    Command,
    CommandKeyboardButton,
    Condition,
    Connection,
    Trigger,
)
from .mixins import TelegramBotMixin

from typing import Any


class ConnectionSerializer(TelegramBotMixin, serializers.ModelSerializer[Connection]):
    source_object_type = serializers.ChoiceField(
        choices=ConnectionObjectType.source_choices(), write_only=True
    )
    target_object_type = serializers.ChoiceField(
        choices=ConnectionObjectType.target_choices(), write_only=True
    )

    class Meta:
        model = Connection
        fields = [
            'id',
            'source_object_type',
            'source_object_id',
            'source_handle_position',
            'target_object_type',
            'target_object_id',
            'target_handle_position',
        ]

    _object_type_map: dict[ConnectionObjectType, Any] = {
        ConnectionObjectType.TRIGGER: {
            'model': Trigger,
            'queryset': lambda self: self.telegram_bot.triggers,
        },
        ConnectionObjectType.COMMAND: {
            'model': Command,
            'queryset': lambda self: self.telegram_bot.commands,
        },
        ConnectionObjectType.COMMAND_KEYBOARD_BUTTON: {
            'model': CommandKeyboardButton,
            'queryset': lambda self: CommandKeyboardButton.objects.filter(
                keyboard__command__telegram_bot=self.telegram_bot
            ),
        },
        ConnectionObjectType.CONDITION: {
            'model': Condition,
            'queryset': lambda self: self.telegram_bot.conditions,
        },
        ConnectionObjectType.BACKGROUND_TASK: {
            'model': BackgroundTask,
            'queryset': lambda self: self.telegram_bot.background_tasks,
        },
    }

    def get_object(self, object_type: str, object_id: int) -> Model:
        object_type = ConnectionObjectType(object_type)
        config: dict[str, Any] | None = self._object_type_map.get(object_type)

        if not config:
            raise ValueError('Unknown object type.')

        try:
            return config['queryset'](self).get(id=object_id)
        except config['model'].DoesNotExist as error:
            raise serializers.ValidationError(
                _('%(object)s не найден.') % {'object': object_type.label}
            ) from error

    def get_object_type(self, object: Model) -> str:
        for object_type, config in self._object_type_map.items():
            if isinstance(object, config['model']):
                return object_type

        raise ValueError('Unknown object.')

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        source_object_type: str = data.pop('source_object_type')
        target_object_type: str = data.pop('target_object_type')

        allowed_source_object_types: dict[str, str] = dict(
            ConnectionObjectType.source_choices()
        )
        allowed_target_object_types: dict[str, str] = dict(
            ConnectionObjectType.target_choices()
        )

        if source_object_type not in allowed_source_object_types:
            raise serializers.ValidationError(
                _('%(source_object)s не может быть стартовой позиции коннектора.')
                % {'source_object': allowed_source_object_types[source_object_type]}
            )

        if target_object_type not in allowed_target_object_types:
            raise serializers.ValidationError(
                _('%(target_object)s не может быть окончательной позиции коннектора.')
                % {'target_object': allowed_target_object_types[target_object_type]}
            )

        data['source_object'] = self.get_object(
            source_object_type, data.pop('source_object_id')
        )
        data['target_object'] = self.get_object(
            target_object_type, data.pop('target_object_id')
        )

        return data

    def create(self, validated_data: dict[str, Any]) -> Connection:
        return self.telegram_bot.connections.create(**validated_data)

    def to_representation(self, instance: Connection) -> dict[str, Any]:
        representation: dict[str, Any] = super().to_representation(instance)
        representation['source_object_type'] = self.get_object_type(
            instance.source_object  # type: ignore [arg-type]
        )
        representation['target_object_type'] = self.get_object_type(
            instance.target_object  # type: ignore [arg-type]
        )

        return representation
