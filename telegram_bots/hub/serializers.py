from django.db.models import Model

from rest_framework import serializers

from ..base_serializers import CommandMediaSerializer
from ..enums import ConnectionObjectType
from ..models import (
    BackgroundTask,
    BackgroundTaskAPIRequest,
    Command,
    CommandAPIRequest,
    CommandDatabaseRecord,
    CommandDocument,
    CommandImage,
    CommandKeyboard,
    CommandKeyboardButton,
    CommandMessage,
    CommandSettings,
    Condition,
    ConditionPart,
    Connection,
    DatabaseRecord,
    TelegramBot,
    Trigger,
    TriggerCommand,
    TriggerMessage,
    User,
    Variable,
)
from .mixins import TelegramBotContextMixin

from typing import Any


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
    class Meta:
        model = TelegramBot
        fields = ['id', 'is_private']


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


class TriggerCommandSerializer(serializers.ModelSerializer[TriggerCommand]):
    class Meta:
        model = TriggerCommand
        fields = ['command', 'payload', 'description']


class TriggerMessageSerializer(serializers.ModelSerializer[TriggerMessage]):
    class Meta:
        model = TriggerMessage
        fields = ['text']


class TriggerSerializer(serializers.ModelSerializer[Trigger]):
    command = TriggerCommandSerializer()
    message = TriggerMessageSerializer()

    class Meta:
        model = Trigger
        fields = ['id', 'name', 'command', 'message']


class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
    class Meta:
        model = CommandSettings
        fields = [
            'is_reply_to_user_message',
            'is_delete_user_message',
            'is_send_as_new_message',
        ]


class CommandImageSerializer(CommandMediaSerializer[CommandImage]):
    class Meta:
        model = CommandImage


class CommandDocumentSerializer(CommandMediaSerializer[CommandDocument]):
    class Meta:
        model = CommandDocument


class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
    class Meta:
        model = CommandMessage
        fields = ['text']


class CommandKeyboardButtonSerializer(
    serializers.ModelSerializer[CommandKeyboardButton]
):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = CommandKeyboardButton
        fields = ['id', 'row', 'position', 'text', 'url', 'source_connections']


class CommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
    buttons = CommandKeyboardButtonSerializer(many=True)

    class Meta:
        model = CommandKeyboard
        fields = ['type', 'buttons']


class CommandAPIRequestSerializer(serializers.ModelSerializer[CommandAPIRequest]):
    class Meta:
        model = CommandAPIRequest
        fields = ['url', 'method', 'headers', 'body']


class CommandDatabaseRecordSerializer(
    serializers.ModelSerializer[CommandDatabaseRecord]
):
    class Meta:
        model = CommandDatabaseRecord
        fields = ['data']


class CommandSerializer(serializers.ModelSerializer[Command]):
    settings = CommandSettingsSerializer()
    images = CommandImageSerializer(many=True)
    documents = CommandDocumentSerializer(many=True)
    message = CommandMessageSerializer()
    keyboard = CommandKeyboardSerializer()
    api_request = CommandAPIRequestSerializer()
    database_record = CommandDatabaseRecordSerializer()
    target_connections = ConnectionSerializer(many=True)

    class Meta:
        model = Command
        fields = [
            'id',
            'name',
            'settings',
            'images',
            'documents',
            'message',
            'keyboard',
            'api_request',
            'database_record',
            'target_connections',
        ]


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


class ConditionSerializer(serializers.ModelSerializer[Condition]):
    parts = ConditionPartSerializer(many=True)
    source_connections = ConnectionSerializer(many=True)
    target_connections = ConnectionSerializer(many=True)

    class Meta:
        model = Condition
        fields = ['id', 'name', 'parts', 'source_connections', 'target_connections']


class BackgroundTaskAPIRequestSerializer(
    serializers.ModelSerializer[BackgroundTaskAPIRequest]
):
    class Meta:
        model = BackgroundTaskAPIRequest
        fields = ['url', 'method', 'headers', 'body']


class BackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask]):
    api_request = BackgroundTaskAPIRequestSerializer()
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = BackgroundTask
        fields = ['id', 'name', 'interval', 'api_request', 'source_connections']


class VariableSerializer(serializers.ModelSerializer[Variable]):
    class Meta:
        model = Variable
        fields = ['id', 'name', 'value']


class UserSerializer(TelegramBotContextMixin, serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked']
        read_only_fields = ['is_allowed', 'is_blocked']

    def create(self, validated_data: dict[str, Any]) -> User:
        telegram_id: int = validated_data.pop('telegram_id')

        return self.telegram_bot.users.get_or_create(
            telegram_id=telegram_id, defaults=validated_data
        )[0]


class DatabaseRecordSerializer(
    TelegramBotContextMixin, serializers.ModelSerializer[DatabaseRecord]
):
    class Meta:
        model = DatabaseRecord
        fields = ['id', 'data']

    def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
        return self.telegram_bot.database_records.create(**validated_data)
