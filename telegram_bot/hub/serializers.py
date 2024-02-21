from rest_framework import serializers

from ..models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandSettings,
	TelegramBotCommandCommand,
	TelegramBotCommandImage,
	TelegramBotCommandFile,
	TelegramBotCommandMessageText,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotCommandApiRequest,
	TelegramBotCommandDatabaseRecord,
	TelegramBotVariable,
	TelegramBotUser,
)

from typing import Any


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
	class Meta:
		model = TelegramBot
		fields = ('id', 'is_private', 'is_enabled', 'is_loading')
		read_only_fields = ('id', 'is_private')

	def update(self, instance: TelegramBot, validated_data: dict[str, Any]) -> TelegramBot:
		instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
		instance.is_loading = validated_data.get('is_loading', instance.is_loading)
		instance.save()

		return instance

class TelegramBotCommandSettingsSerializer(serializers.ModelSerializer[TelegramBotCommandSettings]):
	class Meta:
		model = TelegramBotCommandSettings
		fields = ('is_reply_to_user_message', 'is_delete_user_message', 'is_send_as_new_message')

class TelegramBotCommandCommandSerializer(serializers.ModelSerializer[TelegramBotCommandCommand]):
	class Meta:
		model = TelegramBotCommandCommand
		fields = ('text', 'description')

class TelegramBotCommandImageSerializer(serializers.ModelSerializer[TelegramBotCommandImage]):
	name = serializers.CharField(source='image.name')
	url = serializers.CharField(source='image.url')

	class Meta:
		model = TelegramBotCommandImage
		fields = ('name', 'url')

	def to_representation(self, instance: TelegramBotCommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('images/')[-1]

		return representation

class TelegramBotCommandFileSerializer(serializers.ModelSerializer[TelegramBotCommandFile]):
	name = serializers.CharField(source='file.name')
	url = serializers.CharField(source='file.url')

	class Meta:
		model = TelegramBotCommandFile
		fields = ('name', 'url')

	def to_representation(self, instance: TelegramBotCommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('files/')[-1]

		return representation

class TelegramBotCommandMessageTextSerializer(serializers.ModelSerializer[TelegramBotCommandMessageText]):
	class Meta:
		model = TelegramBotCommandMessageText
		fields = ('text',)

class TelegramBotCommandKeyboardButtonSerializer(serializers.ModelSerializer[TelegramBotCommandKeyboardButton]):
	telegram_bot_command_id = serializers.IntegerField(source='telegram_bot_command.id')

	class Meta:
		model = TelegramBotCommandKeyboardButton
		fields = ('id', 'row', 'text', 'url', 'telegram_bot_command_id')

class TelegramBotCommandKeyboardSerializer(serializers.ModelSerializer[TelegramBotCommandKeyboard]):
	buttons = TelegramBotCommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = TelegramBotCommandKeyboard
		fields = ('type', 'buttons')

class TelegramBotCommandApiRequestSerializer(serializers.ModelSerializer[TelegramBotCommandApiRequest]):
	class Meta:
		model = TelegramBotCommandApiRequest
		fields = ('url', 'method', 'headers', 'body')

class TelegramBotCommandDatabaseRecordSerializer(serializers.ModelSerializer[TelegramBotCommandDatabaseRecord]):
	class Meta:
		model = TelegramBotCommandDatabaseRecord
		fields = ('data',)

class TelegramBotCommandSerializer(serializers.ModelSerializer[TelegramBotCommand]):
	settings = TelegramBotCommandSettingsSerializer()
	command = TelegramBotCommandCommandSerializer(default=None) # type: ignore [arg-type]
	images = TelegramBotCommandImageSerializer(many=True)
	files = TelegramBotCommandFileSerializer(many=True)
	message_text = TelegramBotCommandMessageTextSerializer()
	keyboard = TelegramBotCommandKeyboardSerializer(default=None) # type: ignore [arg-type]
	api_request = TelegramBotCommandApiRequestSerializer(default=None) # type: ignore [arg-type]
	database_record = TelegramBotCommandDatabaseRecordSerializer(default=None) # type: ignore [arg-type]

	class Meta:
		model = TelegramBotCommand
		fields = ('id', 'name', 'settings', 'command', 'images', 'files', 'message_text', 'keyboard', 'api_request', 'database_record')

class TelegramBotVariableSerializer(serializers.ModelSerializer[TelegramBotVariable]):
	class Meta:
		model = TelegramBotVariable
		fields = ('id', 'name', 'value')

class TelegramBotUserSerializer(serializers.ModelSerializer[TelegramBotUser]):
	class Meta:
		model = TelegramBotUser
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')
		read_only_fields = ('id', 'is_allowed', 'is_blocked')

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: TelegramBot | None = self.context.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('You not passed a TelegramBot instance to the serializer context!')

		return telegram_bot

	def create(self, validated_data: dict[str, Any]) -> TelegramBotUser:
		return TelegramBotUser.objects.get_or_create(
			telegram_bot=self.telegram_bot,
			telegram_id=validated_data.pop('telegram_id'),
			defaults=validated_data,
		)[0]