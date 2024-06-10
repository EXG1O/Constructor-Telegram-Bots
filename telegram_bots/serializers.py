from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model, QuerySet
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.request import Request

from users.models import User as SiteUser
from utils.formats import date_time_format

from .base_models import AbstractCommandMedia
from .base_serializers import CommandMediaSerializer, DiagramSerializer
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
import os


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
		extra_kwargs = {'id': {'read_only': False, 'required': False}}


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


class CommandSerializer(serializers.ModelSerializer[Command], TelegramBotContextMixin):
	settings = CommandSettingsSerializer()
	trigger = CommandTriggerSerializer(required=False, allow_null=True)
	images = CommandImageSerializer(many=True, required=False, allow_null=True)
	files = CommandFileSerializer(many=True, required=False, allow_null=True)
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

	def _validate_media(
		self, media: list[dict[str, Any]], file_key: str
	) -> list[dict[str, Any]]:
		for data in media:
			if 'id' not in data and (file_key in data) is ('from_url' in data):
				raise serializers.ValidationError(
					_(
						'Необходимо указать только одно из полей '
						"'%(key)s' или 'from_url'."
					)
					% {'key': file_key},
					code='media',
				)

		return media

	def validate_images(self, images: list[dict[str, Any]]) -> list[dict[str, Any]]:
		return self._validate_media(images, 'image')

	def validate_files(self, files: list[dict[str, Any]]) -> list[dict[str, Any]]:
		return self._validate_media(files, 'file')

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		images_data: list[dict[str, Any]] = data.get('images', [])
		files_data: list[dict[str, Any]] = data.get('files', [])

		if images_data or files_data:
			extra_size: int = 0

			for image_data in images_data:
				image: Any | None = image_data.get('image')

				if isinstance(image, UploadedFile):
					extra_size += image.size or 0

			for file_data in files_data:
				file: Any | None = file_data.get('file')

				if isinstance(file, UploadedFile):
					extra_size += file.size or 0

			if self.telegram_bot.remaining_storage_size - extra_size < 0:
				raise serializers.ValidationError(
					_('Превышен лимит хранилища.'), code='storage_size'
				)

		return data

	def create_settings(self, command: Command, settings_data: dict[str, Any]) -> None:
		CommandSettings.objects.create(command=command, **settings_data)

	def create_trigger(
		self, command: Command, trigger_data: dict[str, Any] | None
	) -> None:
		if not trigger_data:
			return

		CommandTrigger.objects.create(command=command, **trigger_data)

	def create_images(
		self, command: Command, images_data: list[dict[str, Any]] | None
	) -> None:
		if not images_data:
			return

		CommandImage.objects.bulk_create(
			CommandImage(command=command, **image_data) for image_data in images_data
		)

	def create_files(
		self, command: Command, files_data: list[dict[str, Any]] | None
	) -> None:
		if not files_data:
			return

		CommandFile.objects.bulk_create(
			CommandFile(command=command, **file_data) for file_data in files_data
		)

	def create_message(self, command: Command, message_data: dict[str, Any]) -> None:
		CommandMessage.objects.create(command=command, **message_data)

	def create_keyboard(
		self, command: Command, keyboard_data: dict[str, Any] | None
	) -> None:
		if not keyboard_data or 'buttons' not in keyboard_data:
			return

		buttons_data: list[dict[str, Any]] = keyboard_data.pop('buttons')

		keyboard: CommandKeyboard = CommandKeyboard.objects.create(
			command=command, **keyboard_data
		)

		CommandKeyboardButton.objects.bulk_create(
			CommandKeyboardButton(keyboard=keyboard, **button_data)
			for button_data in buttons_data
		)

	def create_api_request(
		self, command: Command, api_request_data: dict[str, Any] | None
	) -> None:
		if not api_request_data:
			return

		CommandAPIRequest.objects.create(command=command, **api_request_data)

	def create_database_record(
		self, command: Command, database_record_data: dict[str, Any] | None
	) -> None:
		if not database_record_data:
			return

		CommandDatabaseRecord.objects.create(command=command, **database_record_data)

	def create(self, validated_data: dict[str, Any]) -> Command:
		settings: dict[str, Any] = validated_data.pop('settings')
		trigger: dict[str, Any] | None = validated_data.pop('trigger', None)
		images: list[dict[str, Any]] | None = validated_data.pop('images', None)
		files: list[dict[str, Any]] | None = validated_data.pop('files', None)
		message: dict[str, Any] = validated_data.pop('message')
		keyboard: dict[str, Any] | None = validated_data.pop('keyboard', None)
		api_request: dict[str, Any] | None = validated_data.pop('api_request', None)
		database_record: dict[str, Any] | None = validated_data.pop(
			'database_record', None
		)

		command: Command = self.telegram_bot.commands.create(**validated_data)

		self.create_settings(command, settings)
		self.create_trigger(command, trigger)
		self.create_images(command, images)
		self.create_files(command, files)
		self.create_message(command, message)
		self.create_keyboard(command, keyboard)
		self.create_api_request(command, api_request)
		self.create_database_record(command, database_record)

		return command

	def update_settings(
		self, command: Command, settings_data: dict[str, Any] | None
	) -> None:
		if not settings_data:
			return

		command.settings.is_reply_to_user_message = settings_data.get(
			'is_reply_to_user_message', command.settings.is_reply_to_user_message
		)
		command.settings.is_delete_user_message = settings_data.get(
			'is_delete_user_message', command.settings.is_delete_user_message
		)
		command.settings.is_send_as_new_message = settings_data.get(
			'is_send_as_new_message', command.settings.is_send_as_new_message
		)
		command.settings.save(
			update_fields=[
				'is_reply_to_user_message',
				'is_delete_user_message',
				'is_send_as_new_message',
			]
		)

	def update_trigger(
		self, command: Command, trigger_data: dict[str, Any] | None
	) -> None:
		if trigger_data:
			try:
				command.trigger.text = trigger_data.get('text', command.trigger.text)
				command.trigger.description = trigger_data.get(
					'description', command.trigger.description
				)
				command.trigger.save(update_fields=['text', 'description'])
			except CommandTrigger.DoesNotExist:
				self.create_trigger(command, trigger_data)
		elif not self.partial:
			try:
				command.trigger.delete()
			except CommandTrigger.DoesNotExist:
				pass

	def _delete_media_files(
		self,
		queryset: QuerySet[AbstractCommandMedia],
		media_class: type[AbstractCommandMedia],
	) -> None:
		file_field_name: str = media_class.file_field_name

		for file_path in queryset.exclude(**{file_field_name: None}).values_list(
			file_field_name, flat=True
		):
			try:
				os.remove(settings.MEDIA_ROOT / file_path)
			except OSError:
				pass

	def update_media(
		self,
		command: Command,
		media_class: type[AbstractCommandMedia],
		media_data: list[dict[str, Any]] | None,
	) -> None:
		file_field_name: str = media_class.file_field_name
		queryset: QuerySet[AbstractCommandMedia] = getattr(
			command, media_class.related_name
		)

		if media_data:
			create_media: list[AbstractCommandMedia] = []
			update_media: list[AbstractCommandMedia] = []

			for data in media_data:
				file: UploadedFile | None = data.get(file_field_name)
				from_url: str | None = data.get('from_url')

				try:
					media: AbstractCommandMedia = queryset.get(id=data['id'])
					media.position = data.get('position', media.position)

					if file or from_url:
						if media.file_field:
							media.file_field.delete()

						media.file_field = file
						media.from_url = from_url

					update_media.append(media)
				except (KeyError, media_class.DoesNotExist):
					create_media.append(media_class(command=command, **data))  # type: ignore [misc]

			new_media: list[AbstractCommandMedia] = media_class.objects.bulk_create(  # type: ignore [attr-defined]
				create_media
			)
			media_class.objects.bulk_update(  # type: ignore [attr-defined]
				update_media, fields=['position', file_field_name, 'from_url']
			)

			if not self.partial:
				new_queryset: QuerySet[AbstractCommandMedia] = queryset.exclude(
					id__in=[media.id for media in new_media + update_media]  # type: ignore [attr-defined]
				)

				self._delete_media_files(new_queryset, media_class)

				new_queryset.delete()
		elif not self.partial:
			self._delete_media_files(queryset, media_class)

			queryset.all().delete()

	def update_images(
		self, command: Command, images_data: list[dict[str, Any]] | None
	) -> None:
		self.update_media(command, CommandImage, images_data)

	def update_files(
		self, command: Command, files_data: list[dict[str, Any]] | None
	) -> None:
		self.update_media(command, CommandFile, files_data)

	def update_message(
		self, command: Command, message_data: dict[str, Any] | None
	) -> None:
		if not message_data:
			return

		command.message.text = message_data.get('text', command.message.text)
		command.message.save(update_fields=['text'])

	def update_keyboard(
		self, command: Command, keyboard_data: dict[str, Any] | None
	) -> None:
		if keyboard_data:
			try:
				command.keyboard.type = keyboard_data.get('type', command.keyboard.type)
				command.keyboard.save(update_fields=['type'])

				create_buttons: list[CommandKeyboardButton] = []
				update_buttons: list[CommandKeyboardButton] = []

				for button_data in keyboard_data.get('buttons', []):
					try:
						button: CommandKeyboardButton = command.keyboard.buttons.get(
							id=button_data['id']
						)
						button.row = button_data.get('row', button.row)
						button.position = button_data.get('position', button.position)
						button.text = button_data.get('text', button.text)
						button.url = button_data.get('url', button.url)

						update_buttons.append(button)
					except (KeyError, CommandKeyboardButton.DoesNotExist):
						create_buttons.append(
							CommandKeyboardButton(
								keyboard=command.keyboard, **button_data
							)
						)

				new_buttons: list[CommandKeyboardButton] = (
					CommandKeyboardButton.objects.bulk_create(create_buttons)
				)
				CommandKeyboardButton.objects.bulk_update(
					update_buttons, fields=['row', 'text', 'url']
				)

				if not self.partial:
					command.keyboard.buttons.exclude(
						id__in=[button.id for button in new_buttons + update_buttons]
					).delete()
			except CommandKeyboard.DoesNotExist:
				self.create_keyboard(command, keyboard_data)
		elif not self.partial:
			try:
				command.keyboard.delete()
			except CommandKeyboard.DoesNotExist:
				pass

	def update_api_request(
		self, command: Command, api_request_data: dict[str, Any] | None
	) -> None:
		if api_request_data:
			try:
				command.api_request.url = api_request_data.get(
					'url', command.api_request.url
				)
				command.api_request.method = api_request_data.get(
					'method', command.api_request.method
				)
				command.api_request.headers = api_request_data.get(
					'headers', command.api_request.headers
				)
				command.api_request.body = api_request_data.get(
					'body', command.api_request.body
				)
				command.api_request.save(
					update_fields=['url', 'method', 'headers', 'body']
				)
			except CommandAPIRequest.DoesNotExist:
				self.create_api_request(command, api_request_data)
		elif not self.partial:
			try:
				command.api_request.delete()
			except CommandAPIRequest.DoesNotExist:
				pass

	def update_database_record(
		self, command: Command, database_record_data: dict[str, Any] | None
	) -> None:
		if database_record_data:
			try:
				command.database_record.data = database_record_data.get(
					'data', command.database_record.data
				)
				command.database_record.save(update_fields=['data'])
			except CommandDatabaseRecord.DoesNotExist:
				self.create_database_record(command, database_record_data)
		elif not self.partial:
			try:
				command.database_record.delete()
			except CommandDatabaseRecord.DoesNotExist:
				pass

	def update(self, command: Command, validated_data: dict[str, Any]) -> Command:
		command.name = validated_data.get('name', command.name)
		command.save(update_fields=['name'])

		self.update_settings(command, validated_data.get('settings'))
		self.update_trigger(command, validated_data.get('trigger'))
		self.update_images(command, validated_data.get('images'))
		self.update_files(command, validated_data.get('files'))
		self.update_message(command, validated_data.get('message'))
		self.update_keyboard(command, validated_data.get('keyboard'))
		self.update_api_request(command, validated_data.get('api_request'))
		self.update_database_record(command, validated_data.get('database_record'))

		command.refresh_from_db(
			fields=['trigger', 'keyboard', 'api_request', 'database_record']
		)

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
		parts_data: list[dict[str, Any]] = validated_data.pop('parts')

		condition: Condition = self.telegram_bot.conditions.create(**validated_data)

		ConditionPart.objects.bulk_create(
			ConditionPart(condition=condition, **part_data) for part_data in parts_data
		)

		return condition

	def update(self, condition: Condition, validated_data: dict[str, Any]) -> Condition:
		condition.name = validated_data.get('name', condition.name)
		condition.save(update_fields=['name'])

		create_parts: list[ConditionPart] = []
		update_parts: list[ConditionPart] = []

		for part_data in validated_data.get('parts', []):
			try:
				part: ConditionPart = condition.parts.get(id=part_data['id'])
				part.type = part_data.get('type', part.type)
				part.first_value = part_data.get('first_value', part.first_value)
				part.operator = part_data.get('operator', part.operator)
				part.second_value = part_data.get('second_value', part.second_value)
				part.next_part_operator = part_data.get(
					'next_part_operator', part.next_part_operator
				)

				update_parts.append(part)
			except (KeyError, ConditionPart.DoesNotExist):
				create_parts.append(ConditionPart(condition=condition, **part_data))

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
				id__in=[part.id for part in new_parts + update_parts]
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
		fields = ['id', 'row', 'position', 'text', 'url', 'source_connections']


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
