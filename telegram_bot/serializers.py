from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from utils import filters

from user.models import User

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandCommand,
	TelegramBotCommandImage,
	TelegramBotCommandFile,
	TelegramBotCommandMessageText,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotCommandApiRequest,
	TelegramBotCommandDatabaseRecord,
	TelegramBotUser,
)
from .functions import is_valid_telegram_bot_api_token

from typing import Any
import re


class TelegramBotSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBot
		fields = ('id', 'username', 'api_token', 'is_private', 'is_running', 'is_stopped')

	def to_representation(self, instance: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = filters.datetime(instance.added_date)

		return representation

class TelegramBotCommandCommandSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandCommand
		fields = ('text', 'description')

class TelegramBotCommandImageSerializer(serializers.ModelSerializer):
	image = serializers.CharField(source='image.url')

	class Meta:
		model = TelegramBotCommandImage
		fields = ('image',)

class TelegramBotCommandFileSerializer(serializers.ModelSerializer):
	file = serializers.CharField(source='file.url')

	class Meta:
		model = TelegramBotCommandFile
		fields = ('file',)

class TelegramBotCommandMessageTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandMessageText
		fields = ('text',)

class TelegramBotCommandKeyboardButtonSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandKeyboardButton
		fields = ('id', 'row', 'text', 'url')

class TelegramBotCommandKeyboardSerializer(serializers.ModelSerializer):
	buttons = TelegramBotCommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = TelegramBotCommandKeyboard
		fields = ('type', 'buttons')

class TelegramBotCommandApiRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandApiRequest
		fields = ('url', 'method', 'headers', 'body')

class TelegramBotCommandDatabaseRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandDatabaseRecord
		fields = ('data',)

class TelegramBotCommandModelSerializer(serializers.ModelSerializer):
	command = TelegramBotCommandCommandSerializer(allow_null=True)
	images = TelegramBotCommandImageSerializer(many=True, allow_null=True)
	files = TelegramBotCommandFileSerializer(many=True, allow_null=True)
	message_text = TelegramBotCommandMessageTextSerializer(allow_null=True)
	keyboard = TelegramBotCommandKeyboardSerializer(allow_null=True)
	api_request = TelegramBotCommandApiRequestSerializer(allow_null=True)
	database_record = TelegramBotCommandDatabaseRecordSerializer(allow_null=True)

	class Meta:
		model = TelegramBotCommand
		fields = ('id', 'name', 'command', 'images', 'files', 'message_text', 'keyboard', 'api_request', 'database_record')

class TelegramBotCommandKeyboardButtonDiagramSerializer(serializers.ModelSerializer):
	telegram_bot_command_id = serializers.IntegerField(source='telegram_bot_command.id', allow_null=True)

	class Meta:
		model = TelegramBotCommandKeyboardButton
		fields = ('id', 'row', 'text', 'url', 'telegram_bot_command_id', 'start_diagram_connector', 'end_diagram_connector')

class TelegramBotCommandKeyboardDiagramSerializer(serializers.ModelSerializer):
	buttons = TelegramBotCommandKeyboardButtonDiagramSerializer(many=True)

	class Meta:
		model = TelegramBotCommandKeyboard
		fields = ('type', 'buttons')

class TelegramBotCommandDiagramSerializer(serializers.ModelSerializer):
	message_text = TelegramBotCommandMessageTextSerializer()
	keyboard = TelegramBotCommandKeyboardDiagramSerializer(allow_null=True)

	class Meta:
		model = TelegramBotCommand
		fields = ('id', 'name', 'image', 'message_text', 'keyboard', 'x', 'y')

class TelegramBotUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotUser
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')

	def to_representation(self, instance: TelegramBotUser) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['activated_date'] = filters.datetime(instance.activated_date)

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

	def validate_api_token(self, api_token: str | None) -> str | None: # type: ignore[override]
		if api_token is not None:
			return super().validate_api_token(api_token)

		return api_token

class CreateTelegramBotCommandCommandSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=32, error_messages={
		'blank': _('Введите команду!'),
		'max_length': _('Команда должна содержать не более 32 символов!'),
	})
	description = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите описание для команды!'),
		'max_length': _('Описание команды должно содержать не более 255 символов!'),
	}, default=None)

class CreateTelegramBotCommandMessageTextSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=4096, error_messages={
		'blank': _('Введите текст сообщения!'),
		'max_length': _('Текст сообщения должен содержать не более 4096 символов!'),
	})

	def validate_text(self, text: str) -> str:
		return re.sub(r'<[/]?p>', '', text).replace('<br>', '\n')

class CreateTelegramBotCommandKeyboardButtonSerializer(serializers.Serializer):
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

class CreateTelegramBotCommandKeyboardSerializer(serializers.Serializer):
	type =  serializers.ChoiceField(choices=['default', 'inline', 'payment'])
	buttons = CreateTelegramBotCommandKeyboardButtonSerializer(many=True)

class CreateTelegramBotCommandApiRequestSerializer(serializers.Serializer):
	url = serializers.URLField(max_length=2048, error_messages={
		'blank': _('Введите URL-адрес для API-запроса!'),
		'invalid': _('Введите правильный URL-адрес для API-запроса!'),
		'max_length': _('URL-адрес API-запроса должен содержать не более 2048 символов!'),
	})
	method = serializers.ChoiceField(choices=['get', 'post', 'put', 'patch', 'delete'])
	headers = serializers.JSONField(default=None)
	body = serializers.JSONField(default=None)

class CreateTelegramBotCommandSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите название команде!'),
		'max_length': _('Название команды должно содержать не более 255 символов!'),
	})
	command = CreateTelegramBotCommandCommandSerializer(default=None)
	message_text = CreateTelegramBotCommandMessageTextSerializer()
	keyboard = CreateTelegramBotCommandKeyboardSerializer(default=None)
	api_request = CreateTelegramBotCommandApiRequestSerializer(default=None)

class UpdateTelegramBotCommandSerializer(CreateTelegramBotCommandSerializer):
	pass

class ConnectTelegramBotCommandDiagramKeyboardButtonSerializer(serializers.Serializer):
	telegram_bot_command_keyboard_button_id = serializers.IntegerField()
	telegram_bot_command_id = serializers.IntegerField()
	start_diagram_connector = serializers.CharField()
	end_diagram_connector = serializers.CharField()

	def validate_telegram_bot_command_id(self, telegram_bot_command_id: int) -> int:
		telegram_bot: TelegramBot = self.context['telegram_bot']

		if not telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			raise serializers.ValidationError(_('Команда Telegram бота не найдена!'))

		return telegram_bot_command_id

	def validate_telegram_bot_command_keyboard_button_id(self, telegram_bot_command_keyboard_button_id: int) -> int:
		telegram_bot_command: TelegramBotCommand = self.context['telegram_bot_command']

		if not telegram_bot_command.keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists():
			raise serializers.ValidationError(_('Кнопка клавиатуры команды Telegram бота не найдена!'))

		return telegram_bot_command_keyboard_button_id

class DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer(serializers.Serializer):
	telegram_bot_command_keyboard_button_id = serializers.IntegerField()

	def validate_telegram_bot_command_keyboard_button_id(self, telegram_bot_command_keyboard_button_id: int) -> int:
		telegram_bot_command: TelegramBotCommand = self.context['telegram_bot_command']

		if not telegram_bot_command.keyboard.buttons.filter(id=telegram_bot_command_keyboard_button_id).exists():
			raise serializers.ValidationError(_('Кнопка клавиатуры команды Telegram бота не найдена!'))

		return telegram_bot_command_keyboard_button_id

class UpdateTelegramBotCommandDiagramPositionSerializer(serializers.Serializer):
	x = serializers.FloatField()
	y = serializers.FloatField()