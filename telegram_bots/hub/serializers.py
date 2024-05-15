from rest_framework import serializers

from ..models import (
	Command,
	CommandAPIRequest,
	CommandDatabaseRecord,
	CommandFile,
	CommandImage,
	CommandKeyboard,
	CommandKeyboardButton,
	CommandMessage,
	CommandSettings,
	CommandTrigger,
	TelegramBot,
	User,
	Variable,
)

from typing import Any


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
	class Meta:
		model = TelegramBot
		fields = ('id', 'is_private', 'is_enabled', 'is_loading')
		read_only_fields = ('id', 'is_private')

	def update(
		self, instance: TelegramBot, validated_data: dict[str, Any]
	) -> TelegramBot:
		instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
		instance.is_loading = validated_data.get('is_loading', instance.is_loading)
		instance.save()

		return instance


class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
	class Meta:
		model = CommandSettings
		fields = (
			'is_reply_to_user_message',
			'is_delete_user_message',
			'is_send_as_new_message',
		)


class CommandTriggerSerializer(serializers.ModelSerializer[CommandTrigger]):
	class Meta:
		model = CommandTrigger
		fields = ('text', 'description')


class CommandImageSerializer(serializers.ModelSerializer[CommandImage]):
	name = serializers.CharField(source='image.name')
	url = serializers.CharField(source='image.url')

	class Meta:
		model = CommandImage
		fields = ('name', 'url')

	def to_representation(self, instance: CommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('images/')[-1]

		return representation


class CommandFileSerializer(serializers.ModelSerializer[CommandFile]):
	name = serializers.CharField(source='file.name')
	url = serializers.CharField(source='file.url')

	class Meta:
		model = CommandFile
		fields = ('name', 'url')

	def to_representation(self, instance: CommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('files/')[-1]

		return representation


class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
	class Meta:
		model = CommandMessage
		fields = ('text',)


class CommandKeyboardButtonSerializer(
	serializers.ModelSerializer[CommandKeyboardButton]
):
	telegram_bot_command_id = serializers.IntegerField(source='telegram_bot_command.id')

	class Meta:
		model = CommandKeyboardButton
		fields = ('id', 'row', 'text', 'url', 'telegram_bot_command_id')


class CommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
	buttons = CommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = CommandKeyboard
		fields = ('type', 'buttons')


class CommandAPIRequestSerializer(serializers.ModelSerializer[CommandAPIRequest]):
	class Meta:
		model = CommandAPIRequest
		fields = ('url', 'method', 'headers', 'body')


class CommandDatabaseRecordSerializer(
	serializers.ModelSerializer[CommandDatabaseRecord]
):
	class Meta:
		model = CommandDatabaseRecord
		fields = ('data',)


class CommandSerializer(serializers.ModelSerializer[Command]):
	settings = CommandSettingsSerializer()
	trigger = CommandTriggerSerializer(default=None)
	images = CommandImageSerializer(many=True)
	files = CommandFileSerializer(many=True)
	message = CommandMessageSerializer()
	keyboard = CommandKeyboardSerializer(default=None)
	api_request = CommandAPIRequestSerializer(default=None)
	database_record = CommandDatabaseRecordSerializer(default=None)

	class Meta:
		model = Command
		fields = (
			'id',
			'name',
			'settings',
			'command',
			'images',
			'files',
			'message_text',
			'keyboard',
			'api_request',
			'database_record',
		)


class VariableSerializer(serializers.ModelSerializer[Variable]):
	class Meta:
		model = Variable
		fields = ('id', 'name', 'value')


class UserSerializer(serializers.ModelSerializer[User]):
	class Meta:
		model = User
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')
		read_only_fields = ('id', 'is_allowed', 'is_blocked')

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: TelegramBot | None = self.context.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError(
				'You not passed a TelegramBot instance to the serializer context!'
			)

		return telegram_bot

	def create(self, validated_data: dict[str, Any]) -> User:
		return User.objects.get_or_create(
			telegram_bot=self.telegram_bot,
			telegram_id=validated_data.pop('telegram_id'),
			defaults=validated_data,
		)[0]
