from django.template import defaultfilters as filters

from rest_framework import serializers

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandCommand,
	TelegramBotCommandMessageText,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotCommandApiRequest,
	TelegramBotUser,
)

from typing import Any


class TelegramBotModelSerializer(serializers.ModelSerializer):
	commands_count = serializers.IntegerField(source='commands.count')
	users_count = serializers.IntegerField(source='users.count')

	class Meta:
		model = TelegramBot
		fields = ['id', 'username', 'api_token', 'is_private', 'is_running', 'is_stopped', 'commands_count', 'users_count']

	def to_representation(self, instance: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = f'{filters.date(instance.added_date)} {filters.time(instance.added_date)}'

		return representation

class TelegramBotCommandCommandModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandCommand
		fields = ['text', 'is_show_in_menu', 'description']

class TelegramBotCommandMessageTextModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandMessageText
		fields = ['text']

	def to_representation(self, instance: TelegramBotCommandMessageText) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['text'] = representation['text'].replace('\n', '<br>')

		return representation

class TelegramBotCommandKeyboardButtonModelSerializer(serializers.ModelSerializer):
	telegram_bot_command_id = serializers.IntegerField(source='telegram_bot_command.id', allow_null=True)

	class Meta:
		model = TelegramBotCommandKeyboardButton
		fields = ['id', 'row', 'text', 'url', 'telegram_bot_command_id', 'start_diagram_connector', 'end_diagram_connector']

	def to_representation(self, instance: TelegramBotCommandKeyboardButton) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)

		if self.context.get('escape', False):
			representation['text'] = filters.escape(representation['text'])

		return representation

class TelegramBotCommandKeyboardModelSerializer(serializers.ModelSerializer):
	buttons = TelegramBotCommandKeyboardButtonModelSerializer(many=True)

	class Meta:
		model = TelegramBotCommandKeyboard
		fields = ['mode', 'buttons']

class TelegramBotCommandApiRequestModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandApiRequest
		fields = ['url', 'method', 'headers', 'data']

class TelegramBotCommandModelSerializer(serializers.ModelSerializer):
	command = TelegramBotCommandCommandModelSerializer(allow_null=True)
	message_text = TelegramBotCommandMessageTextModelSerializer(allow_null=True)
	keyboard = TelegramBotCommandKeyboardModelSerializer(allow_null=True)
	api_request = TelegramBotCommandApiRequestModelSerializer(allow_null=True)

	class Meta:
		model = TelegramBotCommand
		fields = ['id', 'name', 'command', 'image', 'message_text', 'keyboard', 'api_request', 'database_record', 'x', 'y']

	def to_representation(self, instance: TelegramBotCommand):
		representation: dict[str, Any] = super().to_representation(instance)

		if self.context.get('escape', False):
			representation['name'] = filters.escape(representation['name'])

		return representation

class TelegramBotUserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotUser
		fields = ['id', 'user_id', 'full_name', 'is_allowed']

	def to_representation(self, instance: TelegramBotUser) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['activated_date'] = f'{filters.date(instance.activated_date)} {filters.time(instance.activated_date)}'

		return representation
