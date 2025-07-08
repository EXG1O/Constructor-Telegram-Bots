from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from ..mixins import TelegramBotContextMixin
from ..models import Trigger, TriggerCommand, TriggerMessage
from .base import DiagramSerializer
from .connection import ConnectionSerializer

from contextlib import suppress
from typing import Any


class TriggerCommandSerializer(serializers.ModelSerializer[TriggerCommand]):
    class Meta:
        model = TriggerCommand
        fields = ['command', 'payload', 'description']


class TriggerMessageSerializer(serializers.ModelSerializer[TriggerMessage]):
    class Meta:
        model = TriggerMessage
        fields = ['text']


class TriggerSerializer(serializers.ModelSerializer[Trigger], TelegramBotContextMixin):
    command = TriggerCommandSerializer(required=False, allow_null=True)
    message = TriggerMessageSerializer(required=False, allow_null=True)

    class Meta:
        model = Trigger
        fields = ['id', 'name', 'command', 'message']

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if bool(data.get('command')) is bool(data.get('message')):
            raise serializers.ValidationError(
                _("Необходимо указать только одно из полей: 'command' или 'message'.")
            )

        return data

    def create(self, validated_data: dict[str, Any]) -> Trigger:
        command_data: dict[str, Any] | None = validated_data.pop('command', None)
        message_data: dict[str, Any] | None = validated_data.pop('message', None)

        trigger: Trigger = self.telegram_bot.triggers.create(**validated_data)

        if command_data:
            TriggerCommand.objects.create(trigger=trigger, **command_data)

        if message_data:
            TriggerMessage.objects.create(trigger=trigger, **message_data)

        return trigger

    def update(self, trigger: Trigger, validated_data: dict[str, Any]) -> Trigger:
        command_data: dict[str, Any] | None = validated_data.get('command')
        message_data: dict[str, Any] | None = validated_data.get('message')

        trigger.name = validated_data.get('name', trigger.name)
        trigger.save(update_fields=['name'])

        if command_data:
            try:
                trigger.command.command = command_data.get(
                    'command', trigger.command.command
                )
                trigger.command.payload = command_data.get(
                    'payload', trigger.command.payload
                )
                trigger.command.description = command_data.get(
                    'description', trigger.command.description
                )
                trigger.command.save(
                    update_fields=['command', 'payload', 'description']
                )
            except TriggerCommand.DoesNotExist:
                TriggerCommand.objects.create(trigger=trigger, **command_data)
        elif not self.partial:
            with suppress(TriggerCommand.DoesNotExist):
                trigger.command.delete()

        if message_data:
            try:
                trigger.message.text = message_data.get('text', trigger.message.text)
                trigger.message.save(update_fields=['text'])
            except TriggerMessage.DoesNotExist:
                TriggerMessage.objects.create(trigger=trigger, **message_data)
        elif not self.partial:
            with suppress(TriggerMessage.DoesNotExist):
                trigger.message.delete()

        return trigger


class DiagramTriggerSerializer(DiagramSerializer[Trigger]):
    source_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Trigger
        fields = ['id', 'name', 'source_connections'] + DiagramSerializer.Meta.fields
        read_only_fields = ['name']
