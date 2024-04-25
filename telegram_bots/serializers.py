from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

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
	ConditionPart,
	Condition,
	BackgroundTaskAPIRequest,
	BackgroundTask,
	Variable,
	User,
	DatabaseRecord,
)

from typing import Any


class TelegramBotContextMixin:
	@property
	def view(self) -> GenericAPIView:
		view: Any = self.context.get('view')  # type: ignore [attr-defined]

		if not isinstance(view, GenericAPIView):
			raise TypeError(
				'You not passed a rest_framework.generics.GenericAPIView instance as view to the serializer context!'
			)

		return view

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: Any = self.view.kwargs.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('The telegram_bot in view.kwargs is not an TelegramBot instance!')

		return telegram_bot


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
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
		request: Any = self.context.get('request')

		if not isinstance(request, Request):
			raise TypeError(
				'You not passed a rest_framework.request.Request instance as request to the serializer context!'
			)
		elif not isinstance(request.user, SiteUser):
			raise TypeError('The request.user instance is not an users.models.User instance!')

		return request.user

	def create(self, validated_data: dict[str, Any]) -> TelegramBot:
		return self.site_user.telegram_bots.create(**validated_data)

	def update(self, telegram_bot: TelegramBot, validated_data: dict[str, Any]) -> TelegramBot:
		telegram_bot.api_token = validated_data.get('api_token', telegram_bot.api_token)
		telegram_bot.is_private = validated_data.get('is_private', telegram_bot.is_private)
		telegram_bot.save()

		return telegram_bot

	def to_representation(self, telegram_bot: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(telegram_bot)
		representation['added_date'] = filters.datetime(telegram_bot.added_date)

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
		representation['source_object_type'] = self.get_object_type(instance.source_object)  # type: ignore [arg-type]
		representation['target_object_type'] = self.get_object_type(instance.target_object)  # type: ignore [arg-type]

		return representation


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
	trigger = CommandTriggerSerializer(required=False, allow_null=True)
	images = CommandImageSerializer(many=True)
	files = CommandFileSerializer(many=True)
	message = CommandMessageSerializer()
	keyboard = CommandKeyboardSerializer(required=False, allow_null=True)
	api_request = CommandAPIRequestSerializer(required=False, allow_null=True)
	database_record = CommandDatabaseRecordSerializer(required=False, allow_null=True)

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
	images = serializers.ListField(child=serializers.ImageField(), default=[])  # type: ignore [assignment]
	files = serializers.ListField(child=serializers.FileField(), default=[])  # type: ignore [assignment]

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		images: list[InMemoryUploadedFile] = data.get('images', [])
		files: list[InMemoryUploadedFile] = data.get('files', [])

		size: int = sum(image.size for image in images) + sum(file.size for file in files)  # type: ignore [misc]

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

		command: Command = self.telegram_bot.commands.create(**validated_data)

		CommandSettings.objects.create(command=command, **settings)

		if trigger:
			CommandTrigger.objects.create(command=command, **trigger)

		for image in images:
			command.images.create(image=image)

		for file in files:
			command.files.create(file=file)

		CommandMessage.objects.create(command=command, **message)

		if keyboard:
			buttons: list[dict[str, Any]] = keyboard.pop('buttons', [])

			if buttons:
				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(command=command, **keyboard)

				for button in buttons:
					_keyboard.buttons.create(**button)

		if api_request:
			CommandAPIRequest.objects.create(command=command, **api_request)

		if database_record:
			CommandDatabaseRecord.objects.create(command=command, **database_record)

		return command

	def to_representation(self, instance: Command) -> dict[str, Any]:
		return CommandSerializer(instance).data


class UpdateCommandSerializer(CreateCommandSerializer):
	images_id = serializers.ListField(child=serializers.IntegerField(), default=[])
	files_id = serializers.ListField(child=serializers.IntegerField(), default=[])

	class Meta(CreateCommandSerializer.Meta):
		fields = (*CreateCommandSerializer.Meta.fields, 'images_id', 'files_id')  # type: ignore [assignment]

	def update(self, command: Command, validated_data: dict[str, Any]) -> Command:
		settings: dict[str, Any] | None = validated_data.get('settings')
		trigger: dict[str, Any] | None = validated_data.get('trigger')
		images: list[InMemoryUploadedFile] = validated_data.get('images', [])
		images_id: list[int] = validated_data.get('images_id', [])
		files: list[InMemoryUploadedFile] = validated_data.get('files', [])
		files_id: list[int] = validated_data.get('files_id', [])
		message: dict[str, Any] | None = validated_data.get('message')
		keyboard: dict[str, Any] | None = validated_data.get('keyboard')
		api_request: dict[str, Any] | None = validated_data.get('api_request')
		database_record: dict[str, Any] | None = validated_data.get('database_record')

		command.name = validated_data.get('name', command.name)
		command.save()

		if settings:
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

		if trigger:
			try:
				command.trigger.text = trigger.get('text', command.trigger.text)
				command.trigger.description = trigger.get('description', command.trigger.description)
				command.trigger.save()
			except CommandTrigger.DoesNotExist:
				CommandTrigger.objects.create(command=command, **trigger)
		elif not self.partial:
			try:
				command.trigger.delete()
			except CommandTrigger.DoesNotExist:
				pass

		if not self.partial:
			command.images.exclude(id__in=images_id).delete()
			command.files.exclude(id__in=files_id).delete()

		for image in images:
			command.images.create(image=image)

		for file in files:
			command.files.create(file=file)

		if message:
			command.message.text = message.get('text', command.message.text)
			command.message.save()

		if keyboard:
			try:
				command.keyboard.type = keyboard.get('type', command.keyboard.type)
				command.keyboard.save()

				buttons_id: list[int] = []

				for button in keyboard.get('buttons', []):
					_button: CommandKeyboardButton

					try:
						_button = command.keyboard.buttons.get(id=button.get('id', 0))
						_button.row = button.get('row', _button.row)
						_button.text = button.get('text', _button.text)
						_button.url = button.get('url', _button.url)
						_button.save()
					except CommandKeyboardButton.DoesNotExist:
						_button = command.keyboard.buttons.create(**button)

					buttons_id.append(_button.id)

				if not self.partial:
					command.keyboard.buttons.exclude(id__in=buttons_id).delete()
			except CommandKeyboard.DoesNotExist:
				buttons: list[dict[str, Any]] = keyboard.pop('buttons')

				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(command=command, **keyboard)

				for button in buttons:
					_keyboard.buttons.create(**button)
		elif not self.partial:
			try:
				command.keyboard.delete()
			except CommandKeyboard.DoesNotExist:
				pass

		if api_request:
			try:
				command.api_request.url = api_request.get('url', command.api_request.url)
				command.api_request.method = api_request.get('method', command.api_request.method)
				command.api_request.headers = api_request.get('headers', command.api_request.headers)
				command.api_request.body = api_request.get('body', command.api_request.body)
				command.api_request.save()
			except CommandAPIRequest.DoesNotExist:
				CommandAPIRequest.objects.create(command=command, **api_request)
		elif not self.partial:
			try:
				command.api_request.delete()
			except CommandAPIRequest.DoesNotExist:
				pass

		if database_record:
			try:
				command.database_record.data = database_record.get('data', command.database_record.data)
			except CommandDatabaseRecord.DoesNotExist:
				CommandDatabaseRecord.objects.create(command=command, **database_record)
		elif not self.partial:
			try:
				command.database_record.delete()
			except CommandDatabaseRecord.DoesNotExist:
				pass

		return command


class ConditionPartSerializer(serializers.ModelSerializer[ConditionPart]):
	class Meta:
		model = ConditionPart
		fields = ('id', 'type', 'first_value', 'operator', 'second_value', 'next_part_operator')


class ConditionSerializer(serializers.ModelSerializer[Condition], TelegramBotContextMixin):
	parts = ConditionPartSerializer(many=True)

	class Meta:
		model = Condition
		fields = ('id', 'name', 'parts')

	def validate_parts(self, parts: list[dict[str, Any]]) -> list[dict[str, Any]]:
		if not self.partial and not len(parts):
			raise serializers.ValidationError(_('Условие должно содержать хотя бы одну часть.'))

		return parts

	def create(self, validated_data: dict[str, Any]) -> Condition:
		parts: list[dict[str, Any]] = validated_data.pop('parts')

		condition: Condition = self.telegram_bot.conditions.create(**validated_data)

		for part in parts:
			condition.parts.create(**part)

		return condition

	def update(self, condition: Condition, validated_data: dict[str, Any]) -> Condition:
		condition.name = validated_data.get('name', condition.name)
		condition.save()

		parts_id: list[int] = []

		for part in validated_data.get('parts', []):
			_part: ConditionPart

			try:
				_part = condition.parts.get(id=part.get('id', 0))
				_part.type = part.get('type', _part.type)
				_part.first_value = part.get('first_value', _part.first_value)
				_part.operator = part.get('operator', _part.operator)
				_part.second_value = part.get('second_value', _part.second_value)
				_part.next_part_operator = part.get('next_part_operator', _part.next_part_operator)
				_part.save()
			except ConditionPart.DoesNotExist:
				_part = condition.parts.create(**part)

			parts_id.append(_part.id)

		if not self.partial:
			condition.parts.exclude(id__in=parts_id).delete()

		return condition


class BackgroundTaskAPIRequestSerializer(serializers.ModelSerializer[BackgroundTaskAPIRequest]):
	class Meta:
		model = BackgroundTaskAPIRequest
		fields = ('url', 'method', 'headers', 'body')


class BackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask], TelegramBotContextMixin):
	api_request = BackgroundTaskAPIRequestSerializer(required=False)

	class Meta:
		model = BackgroundTask
		fields = ('id', 'name', 'interval', 'api_request')

	def create(self, validated_data: dict[str, Any]) -> BackgroundTask:
		api_request: dict[str, Any] | None = validated_data.pop('api_request', None)

		background_task: BackgroundTask = self.telegram_bot.background_tasks.create(**validated_data)

		if api_request:
			BackgroundTaskAPIRequest.objects.create(background_task=background_task, **api_request)

		return background_task

	def update(self, background_task: BackgroundTask, validated_data: dict[str, Any]) -> BackgroundTask:
		api_request: dict[str, Any] | None = validated_data.get('api_request')

		background_task.name = validated_data.get('name', background_task.name)
		background_task.interval = validated_data.get('interval', background_task.interval)
		background_task.save()

		if api_request:
			try:
				background_task.api_request.url = api_request.get('url', background_task.api_request.url)
				background_task.api_request.method = api_request.get('method', background_task.api_request.method)
				background_task.api_request.headers = api_request.get('headers', background_task.api_request.headers)
				background_task.api_request.body = api_request.get('body', background_task.api_request.body)
				background_task.api_request.save()
			except BackgroundTaskAPIRequest.DoesNotExist:
				BackgroundTaskAPIRequest.objects.create(background_task=background_task, **api_request)
		elif not self.partial:
			try:
				background_task.api_request.delete()
			except BackgroundTaskAPIRequest.DoesNotExist:
				pass

		return background_task


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

	def update(self, command: Command, validated_data: dict[str, Any]) -> Command:
		command.x = validated_data.get('x', command.x)
		command.y = validated_data.get('y', command.y)
		command.save()

		return command


class DiagramConditionSerializer(serializers.ModelSerializer[Condition]):
	source_connections = ConnectionSerializer(many=True, read_only=True)
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = Condition
		fields = ('id', 'name', 'x', 'y', 'source_connections', 'target_connections')
		read_only_fields = ('name',)

	def update(self, condition: Condition, validated_data: dict[str, Any]) -> Condition:
		condition.x = validated_data.get('x', condition.x)
		condition.y = validated_data.get('y', condition.y)
		condition.save()

		return condition


class DiagramBackgroundTaskSerializer(serializers.ModelSerializer[BackgroundTask]):
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = BackgroundTask
		fields = ('id', 'name', 'interval', 'x', 'y', 'target_connections')
		read_only_fields = ('name', 'interval')

	def update(self, background_task: BackgroundTask, validated_data: dict[str, Any]) -> BackgroundTask:
		background_task.x = validated_data.get('x', background_task.x)
		background_task.y = validated_data.get('y', background_task.y)
		background_task.save()

		return background_task


class VariableSerializer(serializers.ModelSerializer[Variable], TelegramBotContextMixin):
	class Meta:
		model = Variable
		fields = ('id', 'name', 'value', 'description')

	def create(self, validated_data: dict[str, Any]) -> Variable:
		return self.telegram_bot.variables.create(**validated_data)

	def update(self, variable: Variable, validated_data: dict[str, Any]) -> Variable:
		variable.name = validated_data.get('name', variable.name)
		variable.value = validated_data.get('value', variable.value)
		variable.description = validated_data.get('description', variable.description)
		variable.save()

		return variable


class UserSerializer(serializers.ModelSerializer[User]):
	class Meta:
		model = User
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')
		read_only_fields = ('telegram_id', 'full_name')

	def update(self, user: User, validated_data: dict[str, Any]) -> User:
		user.is_allowed = validated_data.get('is_allowed', user.is_allowed)
		user.is_blocked = validated_data.get('is_blocked', user.is_blocked)
		user.save()

		return user

	def to_representation(self, user: User) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(user)
		representation['activated_date'] = filters.datetime(user.activated_date)

		return representation


class DatabaseRecordSerializer(serializers.ModelSerializer[DatabaseRecord], TelegramBotContextMixin):
	class Meta:
		model = DatabaseRecord
		fields = ('id', 'data')

	def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
		return self.telegram_bot.database_records.create(**validated_data)

	def update(self, database_record: DatabaseRecord, validated_data: dict[str, Any]) -> DatabaseRecord:
		database_record.data = validated_data.get('data', database_record.data)
		database_record.save()

		return database_record
