from django.template import defaultfilters as filters
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from user.models import User
from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandCommand,
	TelegramBotCommandMessageText,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotCommandApiRequest,
	TelegramBotUser,
)

from .functions import is_valid_telegram_bot_api_token

from typing import Any
import re


class TelegramBotModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBot
		fields = ['id', 'username', 'api_token', 'is_private', 'is_running', 'is_stopped']

	def to_representation(self, instance: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = f'{filters.date(instance.added_date)} {filters.time(instance.added_date)}'

		return representation

class TelegramBotCommandCommandModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandCommand
		fields = ['text', 'description']

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

class CreateTelegramBotSerializer(serializers.Serializer):
	api_token = serializers.CharField(max_length=50, error_messages={
		'blank': _('Введите API-токен Telegram бота!'),
		'max_length': _('API-токен Telegram бота должен содержать не более 50 символов!'),
	})
	is_private = serializers.BooleanField()

	def validate_api_token(self, api_token: str) -> str:
		user: User = self.context['user']

		if user.telegram_bots.filter(api_token=api_token).exists():
			raise serializers.ValidationError(_('Вы уже используете этот API-токен Telegram бота на сайте!'))
		elif TelegramBot.objects.filter(api_token=api_token).exists():
			raise serializers.ValidationError(_('Этот API-токен Telegram бота уже использует другой пользователь сайта!'))

		if not is_valid_telegram_bot_api_token(api_token):
			raise serializers.ValidationError(_('Ваш API-токен Telegram бота является недействительным!'))

		return api_token

class UpdateTelegramBotSerializer(CreateTelegramBotSerializer):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		for field in ['api_token', 'is_private']:
			self.fields[field].required = False
			self.fields[field].default = None

	def validate_api_token(self, api_token: str | None) -> str | None:
		if api_token is not None:
			return super().validate_api_token(api_token)

		return api_token

class TelegramBotCommandCommandSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=32, error_messages={
		'blank': _('Введите команду!'),
		'max_length': _('Команда должна содержать не более 32 символов!'),
	})
	is_show_in_menu = serializers.BooleanField()
	description = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите описание для команды!'),
		'max_length': _('Описание команды должно содержать не более 255 символов!'),
	}, default=None)

class TelegramBotCommandMessageTextSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=4096, error_messages={
		'blank': _('Введите текст сообщения!'),
		'max_length': _('Текст сообщения должен содержать не более 4096 символов!'),
	})

	def validate_text(self, text: str) -> str:
		return re.sub(r'<[/]?p>', '', text).replace('<br>', '\n')

class TelegramBotCommandKeyboardButtonSerializer(serializers.Serializer):
	id = serializers.IntegerField(default=None)
	row = serializers.IntegerField(default=None)
	text = serializers.CharField(max_length=4096, error_messages={
		'blank': _('Введите название кнопки клавиатуры!'),
		'max_length': _('Название кнопки клавиатуры должно содержать не более 4096 символов!'),
	})
	url = serializers.URLField(max_length=2048, error_messages={
		'blank': _('Введите URL-адрес для кнопки клавиатуры!'),
		'invalid': _('Введите правильный URL-адрес для кнопки клавиатуры!'),
		'max_length': _('URL-адрес кнопки клавиатуры должен содержать не более 2048 символов!'),
	}, default=None)

class TelegramBotCommandKeyboardSerializer(serializers.Serializer):
	mode =  serializers.ChoiceField(choices=['default', 'inline', 'payment'])
	buttons = TelegramBotCommandKeyboardButtonSerializer(many=True)

class TelegramBotCommandApiRequestSerializer(serializers.Serializer):
	url = serializers.URLField(max_length=2048, error_messages={
		'blank': _('Введите URL-адрес для API-запроса!'),
		'invalid': _('Введите правильный URL-адрес для API-запроса!'),
		'max_length': _('URL-адрес API-запроса должен содержать не более 2048 символов!'),
	})
	method = serializers.ChoiceField(choices=['get', 'post', 'put', 'patch', 'delete'])
	headers = serializers.JSONField(default=None)
	data = serializers.JSONField(default=None)

class CreateTelegramBotCommandSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите название команде!'),
		'max_length': _('Название команды должно содержать не более 255 символов!'),
	})
	command = TelegramBotCommandCommandSerializer(default=None)
	message_text = TelegramBotCommandMessageTextSerializer()
	keyboard = TelegramBotCommandKeyboardSerializer(default=None)
	api_request = TelegramBotCommandApiRequestSerializer(default=None)
	database_record = serializers.JSONField(default=None)

class UpdateTelegramBotCommandSerializer(CreateTelegramBotCommandSerializer):
	pass

class UpdateTelegramBotCommandPositionSerializer(serializers.Serializer):
	x = serializers.IntegerField()
	y = serializers.IntegerField()

class UpdateTelegramBotCommandKeyboardButtonTelegramBotCommandSerializer(serializers.Serializer):
	telegram_bot_command_id = serializers.IntegerField()
	start_diagram_connector = serializers.CharField()
	end_diagram_connector = serializers.CharField()

	def validate_telegram_bot_command_id(self, telegram_bot_command_id: int) -> int:
		telegram_bot: TelegramBot = self.context['telegram_bot']

		if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			raise serializers.ValidationError(_('Команда Telegram бота не найдена!'))

		return telegram_bot_command_id