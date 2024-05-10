from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.request import Request

from users.models import User as SiteUser
from utils.formats import date_time_format

from .base_serializers import DiagramSerializer
from .models import (
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

from typing import Any


class TelegramBotContextMixin:
	_telegram_bot: TelegramBot | None = None

	@property
	def telegram_bot(self) -> TelegramBot:
		if self._telegram_bot is None:
			telegram_bot: Any = self.context.get('telegram_bot')  # type: ignore [attr-defined]

			if not isinstance(telegram_bot, TelegramBot):
				raise TypeError(
					'You not passed a TelegramBot instance as '
					'telegram_bot to the serializer context.'
				)

			self._telegram_bot = telegram_bot

		return self._telegram_bot


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
	class Meta:
		model = TelegramBot
		fields = [
			'id',
			'username',
			'api_token',
			'storage_size',
			'used_storage_size',
			'remaining_storage_size',
			'is_private',
			'is_enabled',
			'is_loading',
		]
		read_only_fields = [
			'id',
			'username',
			'storage_size',
			'used_storage_size',
			'remaining_storage_size',
			'is_enabled',
			'is_loading',
		]

	@property
	def site_user(self) -> SiteUser:
		request: Any = self.context.get('request')

		if not isinstance(request, Request):
			raise TypeError(
				'You not passed a rest_framework.request.Request instance '
				'as request to the serializer context.'
			)
		elif not isinstance(request.user, SiteUser):
			raise TypeError(
				'The request.user instance is not an users.models.User instance.'
			)

		return request.user

	def create(self, validated_data: dict[str, Any]) -> TelegramBot:
		return self.site_user.telegram_bots.create(**validated_data)

	def update(
		self, telegram_bot: TelegramBot, validated_data: dict[str, Any]
	) -> TelegramBot:
		telegram_bot.api_token = validated_data.get('api_token', telegram_bot.api_token)
		telegram_bot.is_private = validated_data.get(
			'is_private', telegram_bot.is_private
		)
		telegram_bot.save(update_fields=['api_token', 'is_private'])

		return telegram_bot

	def to_representation(self, telegram_bot: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(telegram_bot)
		representation['added_date'] = date_time_format(telegram_bot.added_date)

		return representation


class ConnectionSerializer(
	TelegramBotContextMixin, serializers.ModelSerializer[Connection]
):
	source_object_type = serializers.ChoiceField(
		choices=['command', 'command_keyboard_button', 'condition', 'background_task'],
		write_only=True,
	)
	target_object_type = serializers.ChoiceField(
		choices=['command', 'condition'],
		write_only=True,
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

	def get_object(self, object_type: str, object_id: int) -> Model:
		if object_type == 'command':
			try:
				return self.telegram_bot.commands.get(id=object_id)
			except Command.DoesNotExist:
				raise serializers.ValidationError(_('Команда не найдена!'))
		elif object_type == 'command_keyboard_button':
			try:
				return CommandKeyboardButton.objects.get(
					keyboard__command__telegram_bot=self.telegram_bot, id=object_id
				)
			except CommandKeyboardButton.DoesNotExist:
				raise serializers.ValidationError(
					_('Кнопка клавиатуры команды не найдена!')
				)
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

	def get_object_type(self, object: Model) -> str:
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
		source_object_type: str = data.pop('source_object_type')
		target_object_type: str = data.pop('target_object_type')

		if source_object_type == 'command' and target_object_type == 'command':
			raise serializers.ValidationError(
				_('Нельзя подключить команду к другой команде!')
			)

		data['source_object'] = self.get_object(
			source_object_type, data.pop('source_object_id')
		)
		data['target_object'] = self.get_object(
			target_object_type, data.pop('target_object_id')
		)

		return data

	def create(self, validated_data: dict[str, Any]) -> Connection:
		return self.telegram_bot.connections.create(**validated_data)

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


class CommandImageSerializer(serializers.ModelSerializer[CommandImage]):
	name = serializers.CharField(source='image.name')
	size = serializers.IntegerField(source='image.size')
	url = serializers.CharField(source='image.url')

	class Meta:
		model = CommandImage
		fields = ['id', 'name', 'size', 'url']

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
		fields = ['id', 'name', 'size', 'url']

	def to_representation(self, instance: CommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('files/')[-1]

		return representation


class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
	class Meta:
		model = CommandMessage
		fields = ['text']


class CommandKeyboardButtonSerializer(
	serializers.ModelSerializer[CommandKeyboardButton]
):
	class Meta:
		model = CommandKeyboardButton
		fields = ['id', 'row', 'text', 'url']


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
	trigger = CommandTriggerSerializer(required=False, allow_null=True)
	images = CommandImageSerializer(many=True)
	files = CommandFileSerializer(many=True)
	message = CommandMessageSerializer()
	keyboard = CommandKeyboardSerializer(required=False, allow_null=True)
	api_request = CommandAPIRequestSerializer(required=False, allow_null=True)
	database_record = CommandDatabaseRecordSerializer(required=False, allow_null=True)

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


class BaseOperationCommandSerialization(CommandSerializer, TelegramBotContextMixin):
	images = serializers.ListField(  # type: ignore [assignment]
		child=serializers.ImageField(), required=False, allow_null=True
	)
	files = serializers.ListField(  # type: ignore [assignment]
		child=serializers.FileField(), required=False, allow_null=True
	)

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		images: list[InMemoryUploadedFile] = data.get('images', [])
		files: list[InMemoryUploadedFile] = data.get('files', [])

		if images or files:
			extra_size: int = sum(image.size or 0 for image in images) + sum(
				file.size or 0 for file in files
			)

			if self.telegram_bot.remaining_storage_size - extra_size < 0:
				raise serializers.ValidationError(
					_('Превышен лимит хранилища.'), code='storage_size'
				)

		return data

	def to_representation(self, command: Command) -> dict[str, Any]:
		return CommandSerializer(command).data


class CreateCommandSerializer(BaseOperationCommandSerialization):
	# TODO: In the future, it can be split into separate methods.
	def create(self, validated_data: dict[str, Any]) -> Command:
		settings: dict[str, Any] = validated_data.pop('settings')
		trigger: dict[str, Any] | None = validated_data.pop('trigger', None)
		images: list[InMemoryUploadedFile] | None = validated_data.pop('images', None)
		files: list[InMemoryUploadedFile] | None = validated_data.pop('files', None)
		message: dict[str, Any] = validated_data.pop('message')
		keyboard: dict[str, Any] | None = validated_data.pop('keyboard', None)
		api_request: dict[str, Any] | None = validated_data.pop('api_request', None)
		database_record: dict[str, Any] | None = validated_data.pop(
			'database_record', None
		)

		command: Command = self.telegram_bot.commands.create(**validated_data)

		kwargs: dict[str, Any] = {'command': command}

		CommandSettings.objects.create(**kwargs, **settings)

		if trigger:
			CommandTrigger.objects.create(**kwargs, **trigger)

		if images:
			CommandImage.objects.bulk_create(
				CommandImage(**kwargs, image=image) for image in images
			)

		if files:
			CommandFile.objects.bulk_create(
				CommandFile(**kwargs, file=file) for file in files
			)

		CommandMessage.objects.create(**kwargs, **message)

		if keyboard:
			buttons: list[dict[str, Any]] = keyboard.pop('buttons', [])

			if buttons:
				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
					**kwargs, **keyboard
				)

				CommandKeyboardButton.objects.bulk_create(
					CommandKeyboardButton(keyboard=_keyboard, **button)
					for button in buttons
				)

		if api_request:
			CommandAPIRequest.objects.create(**kwargs, **api_request)

		if database_record:
			CommandDatabaseRecord.objects.create(**kwargs, **database_record)

		return command


class UpdateCommandSerializer(BaseOperationCommandSerialization):
	images_id = serializers.ListField(child=serializers.IntegerField(), default=[])
	files_id = serializers.ListField(child=serializers.IntegerField(), default=[])

	class Meta(BaseOperationCommandSerialization.Meta):
		fields = BaseOperationCommandSerialization.Meta.fields + [
			'images_id',
			'files_id',
		]

	# TODO: In the future, it can be split into separate methods.
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
		command.save(update_fields=['name'])

		if settings:
			command.settings.is_reply_to_user_message = settings.get(
				'is_reply_to_user_message', command.settings.is_reply_to_user_message
			)
			command.settings.is_delete_user_message = settings.get(
				'is_delete_user_message', command.settings.is_delete_user_message
			)
			command.settings.is_send_as_new_message = settings.get(
				'is_send_as_new_message', command.settings.is_send_as_new_message
			)
			command.settings.save(
				update_fields=[
					'is_reply_to_user_message',
					'is_delete_user_message',
					'is_send_as_new_message',
				]
			)

		if trigger:
			try:
				command.trigger.text = trigger.get('text', command.trigger.text)
				command.trigger.description = trigger.get(
					'description', command.trigger.description
				)
				command.trigger.save(update_fields=['text', 'description'])
			except CommandTrigger.DoesNotExist:
				CommandTrigger.objects.create(command=command, **trigger)
		elif not self.partial:
			try:
				command.trigger.delete()
			except CommandTrigger.DoesNotExist:
				pass

		if not self.partial:
			if images_id:
				command.images.exclude(id__in=images_id).delete()

			if files_id:
				command.files.exclude(id__in=files_id).delete()

		if images:
			CommandImage.objects.bulk_create(
				CommandImage(command=command, image=image) for image in images
			)

		if files:
			CommandFile.objects.bulk_create(
				CommandFile(command=command, file=file) for file in files
			)

		if message:
			command.message.text = message.get('text', command.message.text)
			command.message.save(update_fields=['text'])

		if keyboard:
			try:
				command.keyboard.type = keyboard.get('type', command.keyboard.type)
				command.keyboard.save(update_fields=['type'])

				create_buttons: list[CommandKeyboardButton] = []
				update_buttons: list[CommandKeyboardButton] = []

				for button in keyboard.get('buttons', []):
					try:
						_button: CommandKeyboardButton = command.keyboard.buttons.get(
							id=button['id']
						)
						_button.row = button.get('row', _button.row)
						_button.text = button.get('text', _button.text)
						_button.url = button.get('url', _button.url)

						update_buttons.append(_button)
					except (KeyError, CommandKeyboardButton.DoesNotExist):
						create_buttons.append(
							CommandKeyboardButton(keyboard=command.keyboard, **button)
						)

				new_buttons: list[CommandKeyboardButton] = (
					CommandKeyboardButton.objects.bulk_create(create_buttons)
				)
				CommandKeyboardButton.objects.bulk_update(
					update_buttons, fields=['row', 'text', 'url']
				)

				if not self.partial:
					command.keyboard.buttons.exclude(
						id__in=[new_button.id for new_button in new_buttons]
						+ [update_button.id for update_button in update_buttons]
					).delete()
			except CommandKeyboard.DoesNotExist:
				buttons: list[dict[str, Any]] = keyboard.pop('buttons')

				_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
					command=command, **keyboard
				)

				CommandKeyboardButton.objects.bulk_create(
					CommandKeyboardButton(keyboard=_keyboard, **button)
					for button in buttons
				)
		elif not self.partial:
			try:
				command.keyboard.delete()
			except CommandKeyboard.DoesNotExist:
				pass

		if api_request:
			try:
				command.api_request.url = api_request.get(
					'url', command.api_request.url
				)
				command.api_request.method = api_request.get(
					'method', command.api_request.method
				)
				command.api_request.headers = api_request.get(
					'headers', command.api_request.headers
				)
				command.api_request.body = api_request.get(
					'body', command.api_request.body
				)
				command.api_request.save(
					update_fields=['url', 'method', 'headers', 'body']
				)
			except CommandAPIRequest.DoesNotExist:
				CommandAPIRequest.objects.create(command=command, **api_request)
		elif not self.partial:
			try:
				command.api_request.delete()
			except CommandAPIRequest.DoesNotExist:
				pass

		if database_record:
			try:
				command.database_record.data = database_record.get(
					'data', command.database_record.data
				)
				command.database_record.save(update_fields=['data'])
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
		fields = [
			'id',
			'type',
			'first_value',
			'operator',
			'second_value',
			'next_part_operator',
		]


class ConditionSerializer(
	TelegramBotContextMixin, serializers.ModelSerializer[Condition]
):
	parts = ConditionPartSerializer(many=True)

	class Meta:
		model = Condition
		fields = ['id', 'name', 'parts']

	def validate_parts(self, parts: list[dict[str, Any]]) -> list[dict[str, Any]]:
		if not self.partial and not parts:
			raise serializers.ValidationError(
				_('Условие должно содержать хотя бы одну часть.')
			)

		return parts

	def create(self, validated_data: dict[str, Any]) -> Condition:
		parts: list[dict[str, Any]] = validated_data.pop('parts')

		condition: Condition = self.telegram_bot.conditions.create(**validated_data)

		ConditionPart.objects.bulk_create(
			ConditionPart(condition=condition, **part) for part in parts
		)

		return condition

	def update(self, condition: Condition, validated_data: dict[str, Any]) -> Condition:
		condition.name = validated_data.get('name', condition.name)
		condition.save(update_fields=['name'])

		create_parts: list[ConditionPart] = []
		update_parts: list[ConditionPart] = []

		for part in validated_data.get('parts', []):
			try:
				_part: ConditionPart = condition.parts.get(id=part['id'])
				_part.type = part.get('type', _part.type)
				_part.first_value = part.get('first_value', _part.first_value)
				_part.operator = part.get('operator', _part.operator)
				_part.second_value = part.get('second_value', _part.second_value)
				_part.next_part_operator = part.get(
					'next_part_operator', _part.next_part_operator
				)

				update_parts.append(_part)
			except (KeyError, ConditionPart.DoesNotExist):
				create_parts.append(ConditionPart(condition=condition, **part))

		new_parts: list[ConditionPart] = ConditionPart.objects.bulk_create(create_parts)
		ConditionPart.objects.bulk_update(
			update_parts,
			fields=[
				'type',
				'first_value',
				'operator',
				'second_value',
				'next_part_operator',
			],
		)

		if not self.partial:
			condition.parts.exclude(
				id__in=[new_part.id for new_part in new_parts]
				+ [update_part.id for update_part in update_parts]
			).delete()

		return condition


class BackgroundTaskAPIRequestSerializer(
	serializers.ModelSerializer[BackgroundTaskAPIRequest]
):
	class Meta:
		model = BackgroundTaskAPIRequest
		fields = ['url', 'method', 'headers', 'body']


class BackgroundTaskSerializer(
	TelegramBotContextMixin, serializers.ModelSerializer[BackgroundTask]
):
	api_request = BackgroundTaskAPIRequestSerializer(required=False)

	class Meta:
		model = BackgroundTask
		fields = ['id', 'name', 'interval', 'api_request']

	def create(self, validated_data: dict[str, Any]) -> BackgroundTask:
		api_request: dict[str, Any] | None = validated_data.pop('api_request', None)

		background_task: BackgroundTask = self.telegram_bot.background_tasks.create(
			**validated_data
		)

		if api_request:
			BackgroundTaskAPIRequest.objects.create(
				background_task=background_task, **api_request
			)

		return background_task

	def update(
		self, background_task: BackgroundTask, validated_data: dict[str, Any]
	) -> BackgroundTask:
		api_request: dict[str, Any] | None = validated_data.get('api_request')

		background_task.name = validated_data.get('name', background_task.name)
		background_task.interval = validated_data.get(
			'interval', background_task.interval
		)
		background_task.save(update_fields=['name', 'interval'])

		if api_request:
			try:
				background_task.api_request.url = api_request.get(
					'url', background_task.api_request.url
				)
				background_task.api_request.method = api_request.get(
					'method', background_task.api_request.method
				)
				background_task.api_request.headers = api_request.get(
					'headers', background_task.api_request.headers
				)
				background_task.api_request.body = api_request.get(
					'body', background_task.api_request.body
				)
				background_task.api_request.save(
					update_fields=['url', 'method', 'headers', 'body']
				)
			except BackgroundTaskAPIRequest.DoesNotExist:
				BackgroundTaskAPIRequest.objects.create(
					background_task=background_task, **api_request
				)
		elif not self.partial:
			try:
				background_task.api_request.delete()
			except BackgroundTaskAPIRequest.DoesNotExist:
				pass

		return background_task


class DiagramCommandKeyboardButtonSerializer(
	serializers.ModelSerializer[CommandKeyboardButton]
):
	source_connections = ConnectionSerializer(many=True)

	class Meta:
		model = CommandKeyboardButton
		fields = ['id', 'row', 'text', 'url', 'source_connections']


class DiagramCommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
	buttons = DiagramCommandKeyboardButtonSerializer(many=True)

	class Meta:
		model = CommandKeyboard
		fields = ['type', 'buttons']


class DiagramCommandSerializer(DiagramSerializer[Command]):
	images = CommandImageSerializer(many=True, read_only=True)
	files = CommandFileSerializer(many=True, read_only=True)
	message = CommandMessageSerializer(read_only=True)
	keyboard = DiagramCommandKeyboardSerializer(allow_null=True, read_only=True)
	source_connections = ConnectionSerializer(many=True, read_only=True)
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = Command
		fields = [
			'id',
			'name',
			'images',
			'files',
			'message',
			'keyboard',
			'source_connections',
			'target_connections',
		] + DiagramSerializer.Meta.fields
		read_only_fields = ['name']


class DiagramConditionSerializer(DiagramSerializer[Condition]):
	source_connections = ConnectionSerializer(many=True, read_only=True)
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = Condition
		fields = [
			'id',
			'name',
			'source_connections',
			'target_connections',
		] + DiagramSerializer.Meta.fields
		read_only_fields = ['name']


class DiagramBackgroundTaskSerializer(DiagramSerializer[BackgroundTask]):
	target_connections = ConnectionSerializer(many=True, read_only=True)

	class Meta:
		model = BackgroundTask
		fields = [
			'id',
			'name',
			'interval',
			'target_connections',
		] + DiagramSerializer.Meta.fields
		read_only_fields = ['name', 'interval']


class VariableSerializer(
	TelegramBotContextMixin, serializers.ModelSerializer[Variable]
):
	class Meta:
		model = Variable
		fields = ['id', 'name', 'value', 'description']

	def create(self, validated_data: dict[str, Any]) -> Variable:
		return self.telegram_bot.variables.create(**validated_data)

	def update(self, variable: Variable, validated_data: dict[str, Any]) -> Variable:
		variable.name = validated_data.get('name', variable.name)
		variable.value = validated_data.get('value', variable.value)
		variable.description = validated_data.get('description', variable.description)
		variable.save(update_fields=['name', 'value', 'description'])

		return variable


class UserSerializer(serializers.ModelSerializer[User]):
	class Meta:
		model = User
		fields = ['id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked']
		read_only_fields = ['telegram_id', 'full_name']

	def update(self, user: User, validated_data: dict[str, Any]) -> User:
		user.is_allowed = validated_data.get('is_allowed', user.is_allowed)
		user.is_blocked = validated_data.get('is_blocked', user.is_blocked)
		user.save(update_fields=['is_allowed', 'is_blocked'])

		return user

	def to_representation(self, user: User) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(user)
		representation['activated_date'] = date_time_format(user.activated_date)

		return representation


class DatabaseRecordSerializer(
	TelegramBotContextMixin, serializers.ModelSerializer[DatabaseRecord]
):
	class Meta:
		model = DatabaseRecord
		fields = ['id', 'data']

	def create(self, validated_data: dict[str, Any]) -> DatabaseRecord:
		return self.telegram_bot.database_records.create(**validated_data)

	def update(
		self, database_record: DatabaseRecord, validated_data: dict[str, Any]
	) -> DatabaseRecord:
		database_record.data = validated_data.get('data', database_record.data)
		database_record.save(update_fields=['data'])

		return database_record
