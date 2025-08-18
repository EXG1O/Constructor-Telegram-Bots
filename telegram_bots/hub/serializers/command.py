from rest_framework import serializers

from ...models import (
    Command,
    CommandDocument,
    CommandImage,
    CommandKeyboard,
    CommandKeyboardButton,
    CommandMessage,
    CommandSettings,
)
from ...serializers.base import CommandMediaSerializer
from .connection import ConnectionSerializer


class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
    class Meta:
        model = CommandSettings
        fields = ['reply_to_user_message', 'delete_user_message', 'send_as_new_message']


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


class CommandSerializer(serializers.ModelSerializer[Command]):
    settings = CommandSettingsSerializer()
    images = CommandImageSerializer(many=True)
    documents = CommandDocumentSerializer(many=True)
    message = CommandMessageSerializer()
    keyboard = CommandKeyboardSerializer()
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
            'target_connections',
        ]
