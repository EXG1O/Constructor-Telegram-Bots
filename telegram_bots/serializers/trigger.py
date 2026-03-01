from django.conf import settings
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import Trigger, TriggerCommand, TriggerMessage
from .base import DiagramSerializer
from .mixins import TelegramBotMixin

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


class TriggerSerializer(TelegramBotMixin, serializers.ModelSerializer[Trigger]):
    command = TriggerCommandSerializer(required=False, allow_null=True)
    message = TriggerMessageSerializer(required=False, allow_null=True)

    class Meta:
        model = Trigger
        fields = ['id', 'name', 'command', 'message']

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        has_command: bool = bool(data.get('command'))
        has_message: bool = bool(data.get('message'))

        if self.instance and self.partial:
            if not has_command:
                with suppress(TriggerCommand.DoesNotExist):
                    has_command = bool(self.instance.command)
            if not has_message:
                with suppress(TriggerMessage.DoesNotExist):
                    has_message = bool(self.instance.message)

        if has_command is has_message:
            raise serializers.ValidationError(
                _(
                    'Триггер должен иметь значение только для одного из полей: '
                    "'command' или 'message'."
                ),
            )

        if (
            not self.instance
            and self.telegram_bot.triggers.count() + 1
            > settings.TELEGRAM_BOT_MAX_TRIGGERS
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s триггеров.')
                % {'max': settings.TELEGRAM_BOT_MAX_TRIGGERS},
                code='max_limit',
            )

        return data

    def create_command(self, trigger: Trigger, data: dict[str, Any]) -> TriggerCommand:
        return TriggerCommand.objects.create(trigger=trigger, **data)

    def create_message(self, trigger: Trigger, data: dict[str, Any]) -> TriggerMessage:
        return TriggerMessage.objects.create(trigger=trigger, **data)

    def create(self, validated_data: dict[str, Any]) -> Trigger:
        command_data: dict[str, Any] | None = validated_data.pop('command', None)
        message_data: dict[str, Any] | None = validated_data.pop('message', None)

        trigger: Trigger = self.telegram_bot.triggers.create(**validated_data)

        if command_data:
            self.create_command(trigger, command_data)
        if message_data:
            self.create_message(trigger, message_data)

        return trigger

    def update_command(
        self, trigger: Trigger, data: dict[str, Any] | None
    ) -> TriggerCommand | None:
        if not data:
            if not self.partial:
                with suppress(TriggerCommand.DoesNotExist):
                    trigger.command.delete()
                    del trigger._state.fields_cache['command']
            return None

        try:
            command: TriggerCommand = trigger.command
            command.command = data.get('command', command.command)
            command.payload = data.get('payload', command.payload)
            command.description = data.get('description', command.description)
            command.save(update_fields=['command', 'payload', 'description'])
            return command
        except TriggerCommand.DoesNotExist:
            return self.create_command(trigger, data)

    def update_message(
        self, trigger: Trigger, data: dict[str, Any] | None
    ) -> TriggerMessage | None:
        if not data:
            if not self.partial:
                with suppress(TriggerMessage.DoesNotExist):
                    trigger.message.delete()
                    del trigger._state.fields_cache['message']
            return None

        try:
            message: TriggerMessage = trigger.message
            message.text = data.get('text', message.text)
            message.save(update_fields=['text'])
            return message
        except TriggerMessage.DoesNotExist:
            return self.create_message(trigger, data)

    def update(self, trigger: Trigger, validated_data: dict[str, Any]) -> Trigger:
        command_data: dict[str, Any] | None = validated_data.get('command')
        message_data: dict[str, Any] | None = validated_data.get('message')

        trigger.name = validated_data.get('name', trigger.name)
        trigger.save(update_fields=['name'])

        self.update_command(trigger, command_data)
        self.update_message(trigger, message_data)

        return trigger


class DiagramTriggerSerializer(DiagramSerializer[Trigger]):
    class Meta(DiagramSerializer.Meta):
        model = Trigger
