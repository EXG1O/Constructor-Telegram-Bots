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
	CommandFile,
	CommandImage,
	CommandKeyboard,
	CommandKeyboardButton,
	CommandMessage,
	CommandSettings,
	CommandTrigger,
	Condition,
	ConditionPart,
	Connection,
	DatabaseRecord,
	TelegramBot,
	User,
	Variable,
)
from .mixins import TelegramBotContextMixin

from typing import Any


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
	class Meta:
		model = TelegramBot
		fields = ['id', 'api_token', 'is_private', 'must_be_enabled', 'is_enabled']


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
			'source_handle_position',
			'target_object_type',
			'target_object_id',
			'target_handle_position',
		]

	def get_object_type(self, object: Model) -> str:
		if isinstance(object, Command):
			return ConnectionObjectType.COMMAND
		elif isinstance(object, CommandKeyboardButton):
			return ConnectionObjectType.COMMAND_KEYBOARD_BUTTON
		elif isinstance(object, Condition):
			return ConnectionObjectType.CONDITION
		elif isinstance(object, BackgroundTask):
			return ConnectionObjectType.BACKGROUND_TASK

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


class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
	class Meta:
		model = CommandSettings
		fields = [
			'is_reply_to_user_message',
			'is_delete_user_message',
			'is_send_as_new_message',
		]


class CommandTriggerSerializer(serializers.ModelSerializer[CommandTrigger]):
	class Meta:
		model = CommandTrigger
		fields = ['text', 'description']


class CommandImageSerializer(CommandMediaSerializer[CommandImage]):
	file_field_name = 'image'

	class Meta:
		model = CommandImage


class CommandFileSerializer(CommandMediaSerializer[CommandFile]):
	file_field_name = 'file'

	class Meta:
		model = CommandFile


class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
	class Meta:
		model = CommandMessage
		fields = ['text']


class CommandKeyboardButtonSerializer(
	serializers.ModelSerializer[CommandKeyboardButton]
):
	class Meta:
		model = CommandKeyboardButton
		fields = ['id', 'row', 'position', 'text', 'url']


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
	trigger = CommandTriggerSerializer()
	images = CommandImageSerializer(many=True)
	files = CommandFileSerializer(many=True)
	message = CommandMessageSerializer()
	keyboard = CommandKeyboardSerializer()
	api_request = CommandAPIRequestSerializer()
	database_record = CommandDatabaseRecordSerializer()

	class Meta:
		model = Command
		fields = [
			'id',
			'name',
			'settings',
			'trigger',
			'images',
			'files',
			'message',
			'keyboard',
			'api_request',
			'database_record',
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

	class Meta:
		model = Condition
		fields = ['id', 'name', 'parts']


class BackgroundTaskAPIRequestSerializer(
	serializers.ModelSerializer[BackgroundTaskAPIRequest]
):
	class Meta:
		model = BackgroundTaskAPIRequest
		fields = ['url', 'method', 'headers', 'body']


class BackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask]):
	api_request = BackgroundTaskAPIRequestSerializer()

	class Meta:
		model = BackgroundTask
		fields = ['id', 'name', 'interval', 'api_request']


class VariableSerializer(serializers.ModelSerializer[Variable]):
	class Meta:
		model = Variable
		fields = ['id', 'name', 'value', 'description']


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


class DatabaseRecordSerializer(serializers.ModelSerializer[DatabaseRecord]):
	class Meta:
		model = DatabaseRecord
		fields = ['id', 'data']
