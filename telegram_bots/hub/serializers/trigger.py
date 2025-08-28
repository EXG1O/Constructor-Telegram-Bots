from rest_framework import serializers

from ...models import Trigger, TriggerCommand, TriggerMessage
from .connection import ConnectionSerializer


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
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = Trigger
        fields = ['id', 'command', 'message', 'source_connections']
