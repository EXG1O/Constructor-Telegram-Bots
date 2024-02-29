from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from utils import filters

from users.models import User as SiteUser

from .models import (
	TelegramBot,
	Connection,
	CommandSettings,
	CommandTrigger,
	CommandImage,
	CommandFile,
	CommandMessage,
	CommandKeyboardButton,
	CommandKeyboard,
	CommandAPIRequest,
	CommandDatabaseRecord,
	Command,
	Condition,
	BackgroundTask,
	Variable,
	User,
)

from typing import  Any


class TelegramBotContextMixin:
	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: Any = self.context.get('telegram_bot') # type: ignore [attr-defined]

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('You not passed a TelegramBot instance to the serializer context!')

		return telegram_bot


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)

		if self.instance:
			self.fields['api_token'].required = False

	class Meta:
		model = TelegramBot
		fields = (
			'id',
			'username',
			'api_token',
			'storage_size',
			'used_storage_size',
			'remaining_storage_size',
			'is_private',
			'is_enabled',
			'is_loading',
		)
		read_only_fields = (
			'id',
			'username',
			'storage_size',
			'used_storage_size',
			'remaining_storage_size',
			'is_enabled',
			'is_loading',
		)

	@property
	def site_user(self) -> SiteUser:
		site_user: SiteUser | None = self.context.get('site_user')

		if not isinstance(site_user, SiteUser):
			raise TypeError('You not passed a users.models.User instance as site_user to the serializer context!')

		return site_user

	def create(self, validated_data: dict[str, Any]) -> TelegramBot:
		return TelegramBot.objects.create(owner=self.site_user, **validated_data)

	def update(self, instance: TelegramBot, validated_data: dict[str, Any]) -> TelegramBot:
		instance.api_token = validated_data.get('api_token', instance.api_token)
		instance.is_private = validated_data.get('is_private', instance.is_private)
		instance.save()

		return instance

	def to_representation(self, instance: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = filters.datetime(instance.added_date)

		return representation

class TelegramBotActionSerializer(serializers.Serializer):
	action = serializers.ChoiceField(choices=('start', 'restart', 'stop'))

class ConnectionSerializer(serializers.ModelSerializer[Connection], TelegramBotContextMixin):
	source_object_type = serializers.ChoiceField(
		choices=('command', 'command_keyboard_button', 'condition', 'background_task'),
		write_only=True,
	)
	target_object_type = serializers.ChoiceField(
		choices=('command', 'condition'),
		write_only=True,
	)

	class Meta:
		model = Connection
		fields = (
			'id',
			'source_object_type',
			'source_object_id',
			'source_handle_position',
			'target_object_type',
			'target_object_id',
			'target_handle_position',
		)

	def get_object(self, object_type: str, object_id: int) -> models.Model:
		if object_type == 'command':
			try:
				return self.telegram_bot.commands.get(id=object_id)
			except Command.DoesNotExist:
				raise serializers.ValidationError(_('Команда не найдена!'))
		elif object_type == 'command_keyboard_button':
			try:
				return CommandKeyboardButton.objects.get(
					keyboard__command__telegram_bot=self.telegram_bot,
					id=object_id,
				)
			except CommandKeyboardButton.DoesNotExist:
				raise serializers.ValidationError(_('Кнопка клавиатуры команды не найдена!'))
		elif object_type == 'condition':
			try:
				return self.telegram_bot.conditions.get(id=object_id)
			except Condition.DoesNotExist:
				raise serializers.ValidationError(_('Условие не найдено!'))
		elif object_type == 'background_task':
			try:
				return self.telegram_bot.background_tasks.get(id=object_id)
			except BackgroundTask.DoesNotExist:
				raise serializers.ValidationError(_('Фоновая задача не найдена!'))
		else:
			raise ValueError('Unknown object type!')

	def get_object_type(self, object: models.Model) -> str:
		if isinstance(object, Command):
			return 'command'
		elif isinstance(object, CommandKeyboardButton):
			return 'command_keyboard_button'
		elif isinstance(object, Condition):
			return 'condition'
		elif isinstance(object, BackgroundTask):
			return 'background_task'
		else:
			raise ValueError('Unknown object!')

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		source_object_type: str = data['source_object_type']
		target_object_type: str = data['target_object_type']

		if source_object_type == 'command' and target_object_type == 'command':
			raise serializers.ValidationError(_('Нельзя подключить команду к другой команде!'))

		self.source_object = self.get_object(source_object_type, data['source_object_id'])
		self.target_object = self.get_object(target_object_type, data['target_object_id'])

		return data

	def create(self, validated_data: dict[str, Any]) -> Connection:
		del validated_data['source_object_type']
		del validated_data['source_object_id']
		del validated_data['target_object_type']
		del validated_data['target_object_id']

		return Connection.objects.create(
			telegram_bot=self.telegram_bot,
			source_object=self.source_object,
			target_object=self.target_object,
			**validated_data,
		)

	def to_representation(self, instance: Connection) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['source_object_type'] = self.get_object_type(instance.source_object) # type: ignore [arg-type]
		representation['target_object_type'] = self.get_object_type(instance.target_object) # type: ignore [arg-type]

		return representation

class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
	class Meta:
		model = CommandSettings
		fields = (
			'is_reply_to_user_message',
			'is_delete_user_message',
			'is_send_as_new_message',
		)

class CommandCommandSerializer(serializers.ModelSerializer[CommandTrigger]):
	class Meta:
		model = CommandTrigger
		fields = ('text', 'description')

class CommandImageSerializer(serializers.ModelSerializer[CommandImage]):
	name = serializers.CharField(source='image.name')
	size = serializers.IntegerField(source='image.size')
	url = serializers.CharField(source='image.url')

	class Meta:
		model = CommandImage
		fields = ('id', 'name', 'size', 'url')

	def to_representation(self, instance: CommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('images/')[-1]

		return representation

class CommandFileSerializer(serializers.ModelSerializer[CommandFile]):
	name = serializers.CharField(source='file.name')
	size = serializers.IntegerField(source='file.size')
	url = serializers.CharField(source='file.url')

	class Meta:
		model = CommandFile
		fields = ('id', 'name', 'size', 'url')

	def to_representation(self, instance: CommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('files/')[-1]

		return representation

class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
	class Meta:
		model = CommandMessage
		fields = ('text',)

class CommandKeyboardButtonSerializer(serializers.ModelSerializer[CommandKeyboardButton]):
	class Meta:
		model = CommandKeyboardButton
		fields = ('id', 'row', 'text', 'url')

class CommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
	buttons = CommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = CommandKeyboard
		fields = ('type', 'buttons')

class CommandAPIRequestSerializer(serializers.ModelSerializer[CommandAPIRequest]):
	class Meta:
		model = CommandAPIRequest
		fields = ('url', 'method', 'headers', 'body')

class CommandDatabaseRecordSerializer(serializers.ModelSerializer[CommandDatabaseRecord]):
	class Meta:
		model = CommandDatabaseRecord
		fields = ('data',)

class CommandSerializer(serializers.ModelSerializer):
	settings = CommandSettingsSerializer()
	trigger = CommandCommandSerializer(required=False)
	images = CommandImageSerializer(many=True)
	files = CommandFileSerializer(many=True)
	message = CommandMessageSerializer()
	keyboard = CommandKeyboardSerializer(required=False)
	api_request = CommandAPIRequestSerializer(required=False)
	database_record = CommandDatabaseRecordSerializer(required=False)

	class Meta:
		model = Command
		fields = (
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
		)

class CreateCommandSerializer(CommandSerializer, TelegramBotContextMixin):
	images = serializers.ListField(child=serializers.ImageField(), default=[]) # type: ignore [assignment]
	files = serializers.ListField(child=serializers.FileField(), default=[]) # type: ignore [assignment]

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		size: int = sum(image.size for image in data['images']) + sum(file.size for file in data['files'])

		if self.telegram_bot.remaining_storage_size - size < 0:
			raise serializers.ValidationError(_('Вы превысили лимит хранилища!'))

		return data

	def create(self, validated_data: dict[str, Any]) -> Command:
		settings: dict[str, Any] = validated_data.pop('settings')
		trigger: dict[str, Any] | None = validated_data.pop('trigger', None)
		images: list[InMemoryUploadedFile] = validated_data.pop('images')
		files: list[InMemoryUploadedFile] = validated_data.pop('files')
		message: dict[str, Any] = validated_data.pop('message')
		keyboard: dict[str, Any] | None = validated_data.pop('keyboard', None)
		api_request: dict[str, Any] | None = validated_data.pop('api_request', None)
		database_record: dict[str, Any] | None = validated_data.pop('database_record', None)

		command: Command = Command.objects.create(telegram_bot=self.telegram_bot, **validated_data)

		kwargs: dict[str, Command] = {'command': command}

		CommandSettings.objects.create(**kwargs, **settings)

		if trigger:
			CommandTrigger.objects.create(**kwargs, **trigger)

		for image in images:
			CommandImage.objects.create(**kwargs, image=image)

		for file in files:
			CommandFile.objects.create(**kwargs, file=file)

		CommandMessage.objects.create(**kwargs, **message)

		if keyboard:
			buttons: list[dict[str, Any]] = keyboard.pop('buttons', [])

			if buttons:
				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(**kwargs, **keyboard)

				for button in buttons:
					CommandKeyboardButton.objects.create(keyboard=_keyboard, **button)

		if api_request:
			CommandAPIRequest.objects.create(**kwargs, **api_request)

		if database_record:
			CommandDatabaseRecord.objects.create(**kwargs, **database_record)

		return command

	def to_representation(self, instance: Command) -> dict[str, Any]:
		return CommandSerializer(instance).data

class UpdateCommandSerializer(CreateCommandSerializer):
	images_id = serializers.ListField(child=serializers.IntegerField(), default=[])
	files_id = serializers.ListField(child=serializers.IntegerField(), default=[])

	class Meta(CreateCommandSerializer.Meta):
		fields = (*CreateCommandSerializer.Meta.fields, 'images_id', 'files_id') # type: ignore [assignment]

	def update(self, command: Command, validated_data: dict[str, Any]) -> Command:
		settings: dict[str, Any] = validated_data['settings']
		trigger: dict[str, Any] | None = validated_data.get('trigger')
		images: list[InMemoryUploadedFile] = validated_data['images']
		images_id: list[int] = validated_data['images_id']
		files: list[InMemoryUploadedFile] = validated_data['files']
		files_id: list[int] = validated_data['files_id']
		message: dict[str, Any] = validated_data['message']
		keyboard: dict[str, Any] | None = validated_data.get('keyboard')
		api_request: dict[str, Any] | None = validated_data.get('api_request')
		database_record: dict[str, Any] | None = validated_data.get('database_record')

		command.name = validated_data.get('name', command.name)
		command.save()

		try:
			command.settings.is_reply_to_user_message = settings.get(
				'is_reply_to_user_message',
				command.settings.is_reply_to_user_message,
			)
			command.settings.is_delete_user_message = settings.get(
				'is_delete_user_message',
				command.settings.is_delete_user_message,
			)
			command.settings.is_send_as_new_message = settings.get(
				'is_send_as_new_message',
				command.settings.is_send_as_new_message,
			)
			command.settings.save()
		except CommandSettings.DoesNotExist:
			CommandSettings.objects.create(command=command, **settings)

		if trigger:
			try:
				command.trigger.text = trigger.get('text', command.trigger.text)
				command.trigger.description = trigger.get('description')
				command.trigger.save()
			except CommandTrigger.DoesNotExist:
				CommandTrigger.objects.create(command=command, **trigger)
		else:
			try:
				command.trigger.delete()
			except CommandTrigger.DoesNotExist:
				pass

		for image in images:
			CommandImage.objects.create(command=command, image=image)

		for file in files:
			CommandFile.objects.create(command=command, file=file)

		command.images.exclude(id__in=images_id).delete()
		command.files.exclude(id__in=files_id).delete()

		command.message.text = message.get('text', command.message.text)
		command.message.save()

		if keyboard:
			try:
				command.keyboard.type = keyboard.get('type', command.keyboard.type)
				command.keyboard.save()

				buttons_id: list[int] = []

				for button in keyboard.get('buttons', []):
					try:
						_button: CommandKeyboardButton = command.keyboard.buttons.get(id=button.get('id', 0))
						_button.row = button.get('row')
						_button.text = button.get('text', _button.text)
						_button.url = button.get('url')
						_button.save()
					except CommandKeyboardButton.DoesNotExist:
						_button: CommandKeyboardButton = CommandKeyboardButton.objects.create( # type: ignore [no-redef]
							keyboard=command.keyboard,
							**button,
						)

					buttons_id.append(_button.id)

				command.keyboard.buttons.exclude(id__in=buttons_id).delete()
			except CommandKeyboard.DoesNotExist:
				buttons: list[dict[str, Any]] = keyboard.pop('buttons')

				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(command=command, **keyboard)

				for button in buttons:
					CommandKeyboardButton.objects.create(keyboard=_keyboard, **button)
		else:
			try:
				command.keyboard.delete()
			except CommandKeyboard.DoesNotExist:
				pass

		if api_request:
			try:
				command.api_request.url = api_request.get('url', command.api_request.url)
				command.api_request.method = api_request.get('method', command.api_request.method)
				command.api_request.headers = api_request.get('headers')
				command.api_request.body = api_request.get('body')
				command.api_request.save()
			except CommandAPIRequest.DoesNotExist:
				CommandAPIRequest.objects.create(command=command, **api_request)
		else:
			try:
				command.api_request.delete()
			except CommandAPIRequest.DoesNotExist:
				pass

		if database_record:
			try:
				command.database_record.data = database_record.get('data', command.database_record.data)
			except CommandDatabaseRecord.DoesNotExist:
				CommandDatabaseRecord.objects.create(command=command, **database_record)
		else:
			try:
				command.database_record.delete()
			except CommandDatabaseRecord.DoesNotExist:
				pass

		return command

class DiagramCommandKeyboardButtonSerializer(serializers.ModelSerializer[CommandKeyboardButton]):
	source_connections = ConnectionSerializer(many=True)

	class Meta:
		model = CommandKeyboardButton
		fields = ('id', 'row', 'text', 'url', 'source_connections')

class DiagramCommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
	buttons = DiagramCommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = CommandKeyboard
		fields = ('type', 'buttons')

class DiagramCommandSerializer(serializers.ModelSerializer[Command]):
	images = CommandImageSerializer(many=True, read_only=True)
	files = CommandFileSerializer(many=True, read_only=True)
	message = CommandMessageSerializer(read_only=True)
	keyboard = DiagramCommandKeyboardSerializer(allow_null=True, read_only=True)
	source_connections = ConnectionSerializer(many=True, read_only=True)
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = Command
		fields = (
			'id',
			'name',
			'images',
			'files',
			'message',
			'keyboard',
			'x',
			'y',
			'source_connections',
			'target_connections',
		)
		read_only_fields = ('name',)

	def update(self, instance: Command, validated_data: dict[str, Any]) -> Command:
		instance.x = validated_data.get('x', instance.x)
		instance.y = validated_data.get('y', instance.y)
		instance.save()

		return instance

class VariableSerializer(serializers.ModelSerializer[Variable], TelegramBotContextMixin):
	class Meta:
		model = Variable
		fields = ('id', 'name', 'value', 'description')

	def create(self, validated_data: dict[str, Any]) -> Variable:
		return Variable.objects.create(telegram_bot=self.telegram_bot, **validated_data)

	def update(self, instance: Variable, validated_data: dict[str, Any]) -> Variable:
		instance.name = validated_data['name']
		instance.value = validated_data['value']
		instance.description = validated_data['description']
		instance.save()

		return instance

class UserSerializer(serializers.ModelSerializer[User]):
	class Meta:
		model = User
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')

	def to_representation(self, instance: User) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['activated_date'] = filters.datetime(instance.activated_date)

		return representation

class UserActionSerializer(serializers.Serializer):
	action = serializers.ChoiceField(choices=('allow', 'unallow', 'block', 'unblock'))