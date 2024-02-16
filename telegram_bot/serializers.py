from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from utils import filters

from user.models import User

from .models import (
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


class TelegramBotSerializer(serializers.ModelSerializer):
	def __init__(self, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)

		if self.instance:
			for field in ('api_token', 'is_private'):
				self.fields[field].required = False
				self.fields[field].default = None

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
	def user(self) -> User:
		user: User | None = self.context.get('user')

		if not isinstance(user, User):
			raise TypeError('You not passed a User instance to the serializer context!')

		return user

	def create(self, validated_data: dict[str, Any]) -> TelegramBot:
		return TelegramBot.objects.create(owner=self.user, **validated_data)

	def update(self, instance: TelegramBot, validated_data: dict[str, Any]) -> TelegramBot:
		api_token: str | None = validated_data.get('api_token')
		is_private: bool | None = validated_data.get('is_private')

		if api_token:
			instance.api_token = api_token
			instance.is_enabled = False
			instance.is_loading = False
			instance.update_username(save=False)

		if is_private is not None:
			instance.is_private = is_private

		if api_token and is_private is not None:
			instance.save()

		return instance

	def to_representation(self, instance: TelegramBot) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = filters.datetime(instance.added_date)

		return representation

class TelegramBotCommandSettingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandSettings
		fields = ('is_reply_to_user_message', 'is_delete_user_message', 'is_send_as_new_message')

class TelegramBotCommandCommandSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandCommand
		fields = ('text', 'description')

class TelegramBotCommandImageSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source='image.name')
	size = serializers.IntegerField(source='image.size')
	url = serializers.CharField(source='image.url')

	class Meta:
		model = TelegramBotCommandImage
		fields = ('id', 'name', 'size', 'url')

	def to_representation(self, instance: TelegramBotCommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('images/')[-1]

		return representation

class TelegramBotCommandFileSerializer(serializers.ModelSerializer):
	name = serializers.CharField(source='file.name')
	size = serializers.IntegerField(source='file.size')
	url = serializers.CharField(source='file.url')

	class Meta:
		model = TelegramBotCommandFile
		fields = ('id', 'name', 'size', 'url')

	def to_representation(self, instance: TelegramBotCommandImage) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['name'] = representation['name'].split('files/')[-1]

		return representation

class TelegramBotCommandMessageTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommandMessageText
		fields = ('text',)

	def to_representation(self, instance: TelegramBotCommandMessageText) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['text'] = representation['text'].replace('\n', '<br>')

		return representation

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
	settings = TelegramBotCommandSettingsSerializer()
	command = TelegramBotCommandCommandSerializer(default=None)
	images = TelegramBotCommandImageSerializer(many=True)
	files = TelegramBotCommandFileSerializer(many=True)
	message_text = TelegramBotCommandMessageTextSerializer()
	keyboard = TelegramBotCommandKeyboardSerializer(default=None)
	api_request = TelegramBotCommandApiRequestSerializer(default=None)
	database_record = TelegramBotCommandDatabaseRecordSerializer(default=None)

	class Meta:
		model = TelegramBotCommand
		fields = ('id', 'name', 'settings', 'command', 'images', 'files', 'message_text', 'keyboard', 'api_request', 'database_record')

class CreateTelegramBotCommandSerializer(TelegramBotCommandModelSerializer):
	images = serializers.ListField(child=serializers.ImageField(), default=[]) # type: ignore [assignment]
	files = serializers.ListField(child=serializers.FileField(), default=[]) # type: ignore [assignment]

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: TelegramBot | None = self.context.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('You not passed a TelegramBot instance to the serializer context!')

		return telegram_bot

	def validate(self, data: dict[str, Any]) -> dict[str, Any]:
		size: int = sum(image.size for image in data['images']) + sum(file.size for file in data['files'])

		if self.telegram_bot.remaining_storage_size - size < 0:
			raise serializers.ValidationError(_('Вы превысили лимит памяти!'))

		return data

	def create(self, validated_data: dict[str, Any]) -> TelegramBotCommand:
		settings: dict[str, Any] = validated_data.pop('settings')
		command: dict[str, Any] | None = validated_data.pop('command')
		images: list[InMemoryUploadedFile] = validated_data.pop('images')
		files: list[InMemoryUploadedFile] = validated_data.pop('files')
		message_text: dict[str, Any] = validated_data.pop('message_text')
		keyboard: dict[str, Any] | None = validated_data.pop('keyboard')
		api_request: dict[str, Any] | None = validated_data.pop('api_request')
		database_record: dict[str, Any] | None = validated_data.pop('database_record')

		telegram_bot_command: TelegramBotCommand = TelegramBotCommand.objects.create(telegram_bot=self.telegram_bot, **validated_data)

		kwargs: dict[str, TelegramBotCommand] = {'telegram_bot_command': telegram_bot_command}

		TelegramBotCommandSettings.objects.create(**kwargs, **settings)

		if command:
			TelegramBotCommandCommand.objects.create(**kwargs, **command)

		for image in images:
			TelegramBotCommandImage.objects.create(**kwargs, image=image)

		for file in files:
			TelegramBotCommandFile.objects.create(**kwargs, file=file)

		TelegramBotCommandMessageText.objects.create(**kwargs, **message_text)

		if keyboard:
			buttons: list[dict[str, Any]] = keyboard.pop('buttons')

			_keyboard: TelegramBotCommandKeyboard = TelegramBotCommandKeyboard.objects.create(**kwargs, **keyboard)

			for button in buttons:
				TelegramBotCommandKeyboardButton.objects.create(telegram_bot_command_keyboard=_keyboard, **button)

		if api_request:
			TelegramBotCommandApiRequest.objects.create(**kwargs, **api_request)

		if database_record:
			TelegramBotCommandDatabaseRecord.objects.create(**kwargs, **database_record)

		return telegram_bot_command

	def to_representation(self, instance: TelegramBotCommand) -> dict[str, Any]:
		return TelegramBotCommandModelSerializer(instance).data

class UpdateTelegramBotCommandSerializer(CreateTelegramBotCommandSerializer):
	images_id = serializers.ListField(child=serializers.IntegerField(), default=[])
	files_id = serializers.ListField(child=serializers.IntegerField(), default=[])

	class Meta(CreateTelegramBotCommandSerializer.Meta):
		fields = (*CreateTelegramBotCommandSerializer.Meta.fields, 'images_id', 'files_id') # type: ignore [assignment]

	def update(self, instance: TelegramBotCommand, validated_data: dict[str, Any]) -> TelegramBotCommand:
		settings: dict[str, Any] | None = validated_data.get('settings')
		command: dict[str, Any] | None = validated_data['command']
		images: list[InMemoryUploadedFile] = validated_data['images']
		images_id: list[int] = validated_data['images_id']
		files: list[InMemoryUploadedFile] = validated_data['files']
		files_id: list[int] = validated_data['files_id']
		message_text: dict[str, Any] | None = validated_data.get('message_text')
		keyboard: dict[str, Any] | None = validated_data['keyboard']
		api_request: dict[str, Any] | None = validated_data['api_request']
		database_record: dict[str, Any] | None = validated_data['database_record']

		instance.name = validated_data.get('name', instance.name)
		instance.save()

		if settings:
			try:
				instance.settings.is_reply_to_user_message = settings.get('is_reply_to_user_message', instance.settings.is_reply_to_user_message)
				instance.settings.is_delete_user_message = settings.get('is_delete_user_message', instance.settings.is_delete_user_message)
				instance.settings.is_send_as_new_message = settings.get('is_send_as_new_message', instance.settings.is_send_as_new_message)
				instance.settings.save()
			except TelegramBotCommandSettings.DoesNotExist:
				TelegramBotCommandSettings.objects.create(telegram_bot_command=instance, **settings)

		if command:
			try:
				instance.command.text = command.get('text', instance.command.text)
				instance.command.description = command.get('description', instance.command.description)
				instance.command.save()
			except TelegramBotCommandCommand.DoesNotExist:
				TelegramBotCommandCommand.objects.create(telegram_bot_command=instance, **command)
		else:
			try:
				instance.command.delete()
			except TelegramBotCommandCommand.DoesNotExist:
				pass

		for image in instance.images.all():
			if image.id not in images_id:
				image.delete()

		for image in images: # type: ignore [assignment]
			TelegramBotCommandImage.objects.create(telegram_bot_command=instance, image=image)

		for file in instance.files.all():
			if file.id not in files_id:
				file.delete()

		for file in files: # type: ignore [assignment]
			TelegramBotCommandFile.objects.create(telegram_bot_command=instance, file=file)

		if message_text:
			instance.message_text.text = message_text.get('text', instance.message_text.text)
			instance.message_text.save()

		if keyboard:
			try:
				instance.keyboard.type = keyboard.get('type', instance.keyboard.type)
				instance.keyboard.save()

				buttons_id: list[int] = []

				for button in keyboard['buttons']:
					try:
						button_: TelegramBotCommandKeyboardButton = instance.keyboard.buttons.get(id=button.get('id', 0))
						button_.row = button.get('row')
						button_.text = button.get('text', button_.text)
						button_.url = button.get('url')
						button_.save()
					except TelegramBotCommandKeyboardButton.DoesNotExist:
						button_: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create( # type: ignore [no-redef]
							telegram_bot_command_keyboard=instance.keyboard,
							**button
						)

					buttons_id.append(button_.id)

				for button in instance.keyboard.buttons.all():
					if button.id not in buttons_id:
						button.delete()
			except TelegramBotCommandKeyboard.DoesNotExist:
				buttons: list[dict[str, Any]] = keyboard.pop('buttons')

				_keyboard: TelegramBotCommandKeyboard = TelegramBotCommandKeyboard.objects.create(telegram_bot_command=instance, **keyboard)

				for button in buttons:
					TelegramBotCommandKeyboardButton.objects.create(telegram_bot_command_keyboard=_keyboard, **button)
		else:
			try:
				instance.keyboard.delete()
			except TelegramBotCommandKeyboard.DoesNotExist:
				pass

		if api_request:
			try:
				instance.api_request.url = api_request.get('url', instance.api_request.url)
				instance.api_request.method = api_request.get('method', instance.api_request.method)
				instance.api_request.headers = api_request.get('headers')
				instance.api_request.body = api_request.get('body')
				instance.api_request.save()
			except TelegramBotCommandApiRequest.DoesNotExist:
				TelegramBotCommandApiRequest.objects.create(telegram_bot_command=instance, **api_request)
		else:
			try:
				instance.api_request.delete()
			except TelegramBotCommandApiRequest.DoesNotExist:
				pass

		if database_record:
			try:
				instance.database_record.data = database_record.get('data', instance.database_record.data)
			except TelegramBotCommandDatabaseRecord.DoesNotExist:
				TelegramBotCommandDatabaseRecord.objects.create(telegram_bot_command=instance, **database_record)
		else:
			try:
				instance.database_record.delete()
			except TelegramBotCommandDatabaseRecord.DoesNotExist:
				pass

		return instance

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
	images = TelegramBotCommandImageSerializer(many=True)
	files = TelegramBotCommandFileSerializer(many=True)
	message_text = TelegramBotCommandMessageTextSerializer()
	keyboard = TelegramBotCommandKeyboardDiagramSerializer(allow_null=True)

	class Meta:
		model = TelegramBotCommand
		fields = ('id', 'name', 'images', 'files', 'message_text', 'keyboard', 'x', 'y')

class ConnectTelegramBotCommandDiagramKeyboardButtonSerializer(serializers.Serializer):
	telegram_bot_command_keyboard_button_id = serializers.IntegerField()
	telegram_bot_command_id = serializers.IntegerField()
	start_diagram_connector = serializers.CharField()
	end_diagram_connector = serializers.CharField()

	class Meta:
		fields = ('telegram_bot_command_keyboard_button_id', 'telegram_bot_command_id', 'start_diagram_connector', 'end_diagram_connector')

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: TelegramBot | None = self.context.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('You not passed a TelegramBot instance to the serializer context!')

		return telegram_bot

	def validate_telegram_bot_command_id(self, telegram_bot_command_id: int) -> int:
		if not self.telegram_bot.commands.filter(id=telegram_bot_command_id).exists():
			raise serializers.ValidationError(_('Команда Telegram бота не найдена!'))

		return telegram_bot_command_id

	def validate_telegram_bot_command_keyboard_button_id(self, telegram_bot_command_keyboard_button_id: int) -> int:
		try:
			self.instance.keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id) # type: ignore [union-attr]
		except TelegramBotCommandKeyboard.DoesNotExist:
			raise serializers.ValidationError(_('У команды Telegram бота нет клавиатуры!'))
		except TelegramBotCommandKeyboardButton.DoesNotExist:
			raise serializers.ValidationError(_('Кнопка клавиатуры команды Telegram бота не найдена!'))

		return telegram_bot_command_keyboard_button_id

	def update(self, instance: TelegramBotCommand, validated_data: dict[str, Any]) -> TelegramBotCommand:
		keyboard_button: TelegramBotCommandKeyboardButton = instance.keyboard.buttons.get(id=validated_data['telegram_bot_command_keyboard_button_id'])
		keyboard_button.telegram_bot_command = self.telegram_bot.commands.get(id=validated_data['telegram_bot_command_id'])
		keyboard_button.start_diagram_connector = validated_data['start_diagram_connector']
		keyboard_button.end_diagram_connector = validated_data['end_diagram_connector']
		keyboard_button.save()

		return instance

class DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer(serializers.Serializer):
	telegram_bot_command_keyboard_button_id = serializers.IntegerField()

	def validate_telegram_bot_command_keyboard_button_id(self, telegram_bot_command_keyboard_button_id: int) -> int:
		try:
			self.instance.keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id) # type: ignore [union-attr]
		except TelegramBotCommandKeyboard.DoesNotExist:
			raise serializers.ValidationError(_('У команды Telegram бота нет клавиатуры!'))
		except TelegramBotCommandKeyboardButton.DoesNotExist:
			raise serializers.ValidationError(_('Кнопка клавиатуры команды Telegram бота не найдена!'))

		return telegram_bot_command_keyboard_button_id

	def update(self, instance: TelegramBotCommand, validated_data: dict[str, Any]) -> TelegramBotCommand:
		keyboard_button: TelegramBotCommandKeyboardButton = instance.keyboard.buttons.get(id=validated_data['telegram_bot_command_keyboard_button_id'])
		keyboard_button.telegram_bot_command = None
		keyboard_button.start_diagram_connector = None
		keyboard_button.end_diagram_connector = None
		keyboard_button.save()

		return instance

class UpdateTelegramBotCommandDiagramPositionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotCommand
		fields = ('x', 'y')
		extra_kwargs = {
			'x': {'required': True},
			'y': {'required': True},
		}

	def update(self, instance: TelegramBotCommand, validated_data: dict[str, Any]) -> TelegramBotCommand:
		instance.x = validated_data['x']
		instance.y = validated_data['y']
		instance.save()

		return instance

class TelegramBotVariableSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotVariable
		fields = ('id', 'name', 'value', 'description')

	@property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: TelegramBot | None = self.context.get('telegram_bot')

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError('You not passed a TelegramBot instance to the serializer context!')

		return telegram_bot

	def create(self, validated_data: dict[str, Any]) -> TelegramBotVariable:
		return TelegramBotVariable.objects.create(telegram_bot=self.telegram_bot, **validated_data)

	def update(self, instance: TelegramBotVariable, validated_data: dict[str, Any]) -> TelegramBotVariable:
		instance.name = validated_data['name']
		instance.value = validated_data['value']
		instance.description = validated_data['description']
		instance.save()

		return instance

class TelegramBotUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = TelegramBotUser
		fields = ('id', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked')

	def to_representation(self, instance: TelegramBotUser) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['activated_date'] = filters.datetime(instance.activated_date)

		return representation