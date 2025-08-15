from django.db.models import Model

from rest_framework import serializers

from ...enums import ConnectionObjectType
from ...models import (
    APIRequest,
    BackgroundTask,
    Command,
    CommandKeyboardButton,
    Condition,
    Connection,
    DatabaseOperation,
    Trigger,
)

from typing import Any


class ConnectionSerializer(serializers.ModelSerializer[Connection]):
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
            'target_object_type',
            'target_object_id',
        ]

    _object_type_map: dict[ConnectionObjectType, type[Model]] = {
        ConnectionObjectType.TRIGGER: Trigger,
        ConnectionObjectType.COMMAND: Command,
        ConnectionObjectType.COMMAND_KEYBOARD_BUTTON: CommandKeyboardButton,
        ConnectionObjectType.CONDITION: Condition,
        ConnectionObjectType.BACKGROUND_TASK: BackgroundTask,
        ConnectionObjectType.API_REQUEST: APIRequest,
        ConnectionObjectType.DATABASE_OPERATION: DatabaseOperation,
    }

    def get_object_type(self, object: Model) -> str:
        for object_type, model_class in self._object_type_map.items():
            if isinstance(object, model_class):
                return object_type

        raise ValueError('Unknown object.')

    def to_representation(self, instance: Connection) -> dict[str, Any]:
        representation: dict[str, Any] = super().to_representation(instance)
        representation['source_object_type'] = self.get_object_type(
            instance.source_object  # type: ignore [arg-type]
        )
        representation['target_object_type'] = self.get_object_type(
            instance.target_object  # type: ignore [arg-type]
        )

        return representation
