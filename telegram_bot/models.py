from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

import requests
from requests import Response

from typing import Any


class TelegramBot(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telegram_bots', verbose_name=_('Владелец'))
	username = models.CharField('@username', max_length=32, null=True)
	api_token = models.CharField(_('API-токен'), max_length=50, unique=True)
	is_private = models.BooleanField(_('Приватный'), default=False)
	is_running = models.BooleanField(_('Включён'), default=False)
	is_stopped = models.BooleanField(_('Выключен'), default=True)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot'

		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	# TODO: Надо реализовать метод start для запуска Telegram бота, но проблема в том, что происходит циклический импорт.

	def stop(self) -> None:
		self.is_running = False
		self.save()

	def update_username(self, save: bool = True) -> None:
		if settings.TEST:
			self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
		else:
			responce: Response = requests.get(f'https://api.telegram.org/bot{self.api_token}/getMe')

			if responce.status_code == 200:
				self.username = responce.json()['result']['username']

		if save:
			self.save()

	def __str__(self) -> str:
		return f'@{self.username}'

class TelegramBotCommandManager(models.Manager):
	def create( # type: ignore [override]
		self,
		telegram_bot: TelegramBot,
		name: str,
		settings: dict[str, Any],
		message_text: dict[str, Any],
		images: list[InMemoryUploadedFile] = [],
		files: list[InMemoryUploadedFile] = [],
		command: dict[str, Any] | None = None,
		keyboard: dict[str, Any] | None = None,
		api_request: dict[str, Any] | None = None,
		database_record: dict[str, Any] | None = None,
	) -> 'TelegramBotCommand':
		telegram_bot_command: TelegramBotCommand = super().create(telegram_bot=telegram_bot, name=name) # type: ignore [assignment]

		kwargs: dict[str, TelegramBotCommand] = {'telegram_bot_command': telegram_bot_command}

		TelegramBotCommandSettings.objects.create(**kwargs, **settings)
		TelegramBotCommandMessageText.objects.create(**kwargs, **message_text)

		if command:
			TelegramBotCommandCommand.objects.create(**kwargs, **command)

		if keyboard:
			TelegramBotCommandKeyboard.objects.create(**kwargs, **keyboard) # type: ignore [misc, arg-type]

		if api_request:
			TelegramBotCommandApiRequest.objects.create(**kwargs, **api_request)

		if database_record:
			TelegramBotCommandDatabaseRecord.objects.create(**kwargs, **database_record)

		for image in images:
			TelegramBotCommandImage.objects.create(**kwargs, image=image)

		for file in files:
			TelegramBotCommandFile.objects.create(**kwargs, file=file)

		return telegram_bot_command

class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)

	x =	models.IntegerField(_('Координата X'), default=0)
	y = models.IntegerField(_('Координата Y'), default=0)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

	def update(
		self,
		name: str,
		settings: dict[str, Any],
		message_text: dict[str, Any],
		images: list[InMemoryUploadedFile] = [],
		images_id: list[int] = [],
		files: list[InMemoryUploadedFile] = [],
		files_id: list[int] = [],
		command: dict[str, Any] | None = None,
		keyboard: dict[str, Any] | None = None,
		api_request: dict[str, Any] | None = None,
		database_record: dict[str, Any] | None = None,
	):
		self.name = name
		self.save()

		self.message_text.text = message_text['text']
		self.message_text.save()

		try:
			self.settings.is_reply_to_user_message = settings['is_reply_to_user_message']
			self.settings.is_delete_user_message = settings['is_delete_user_message']
			self.settings.is_send_as_new_message = settings['is_send_as_new_message']
			self.settings.save()
		except TelegramBotCommandSettings.DoesNotExist:
			TelegramBotCommandSettings.objects.create(telegram_bot_command=self, **settings)

		if command:
			try:
				self.command.text = command['text']
				self.command.description = command['description']
				self.command.save()
			except TelegramBotCommandCommand.DoesNotExist:
				TelegramBotCommandCommand.objects.create(telegram_bot_command=self, **command)
		else:
			try:
				self.command.delete()
			except TelegramBotCommandCommand.DoesNotExist:
				pass

		if keyboard:
			try:
				self.keyboard.type = keyboard['type']
				self.keyboard.save()

				buttons_id: list[int] = []

				for button in keyboard['buttons']:
					try:
						button_: TelegramBotCommandKeyboardButton = self.keyboard.buttons.get(id=button['id'])
						button_.row = button['row']
						button_.text = button['text']
						button_.url = button['url']
						button_.save()
					except TelegramBotCommandKeyboardButton.DoesNotExist:
						button_: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create( # type: ignore [no-redef]
							telegram_bot_command_keyboard=self.keyboard,
							**button
						)

					buttons_id.append(button_.id)

				for button in self.keyboard.buttons.all():
					if button.id not in buttons_id:
						button.delete()
			except TelegramBotCommandKeyboard.DoesNotExist:
				TelegramBotCommandKeyboard.objects.create(telegram_bot_command=self, **keyboard)
		else:
			try:
				self.keyboard.delete()
			except TelegramBotCommandKeyboard.DoesNotExist:
				pass

		if api_request:
			try:
				self.api_request.url = api_request['url']
				self.api_request.method = api_request['method']
				self.api_request.headers = api_request['headers']
				self.api_request.body = api_request['body']
				self.api_request.save()
			except TelegramBotCommandApiRequest.DoesNotExist:
				TelegramBotCommandApiRequest.objects.create(telegram_bot_command=self, **api_request)
		else:
			try:
				self.api_request.delete()
			except TelegramBotCommandApiRequest.DoesNotExist:
				pass

		if database_record:
			try:
				self.database_record.data = database_record['data']
			except TelegramBotCommandDatabaseRecord.DoesNotExist:
				TelegramBotCommandDatabaseRecord.objects.create(telegram_bot_command=self, **database_record)
		else:
			try:
				self.database_record.delete()
			except TelegramBotCommandDatabaseRecord.DoesNotExist:
				pass

		for image in self.images.all():
			if image.id not in images_id:
				image.delete()

		for image in images: # type: ignore [assignment]
			TelegramBotCommandImage.objects.create(telegram_bot_command=self, image=image)

		for file in self.files.all():
			if file.id not in files_id:
				file.delete()

		for file in files: # type: ignore [assignment]
			TelegramBotCommandFile.objects.create(telegram_bot_command=self, file=file)

	def __str__(self) -> str:
		return self.name

class TelegramBotCommandSettings(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='settings')
	is_reply_to_user_message = models.BooleanField(_('Ответить на сообщение пользователя'), default=False)
	is_delete_user_message = models.BooleanField(_('Удалить сообщение пользователя'), default=False)
	is_send_as_new_message = models.BooleanField(_('Отправить сообщение как новое'), default=False)

	class Meta:
		db_table = 'telegram_bot_command_settings'

class TelegramBotCommandCommand(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='command')
	text = models.CharField(_('Команда'), max_length=32)
	description = models.CharField(_('Описание'), max_length=255, blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_command'

def upload_telegram_bot_command_image_path(instance: 'TelegramBotCommandImage', file_name: str) -> str:
	return f'telegram_bots/{instance.telegram_bot_command.telegram_bot.id}/commands/{instance.telegram_bot_command.id}/images/{file_name}'

def upload_telegram_bot_command_file_path(instance: 'TelegramBotCommandFile', file_name: str) -> str:
	return f'telegram_bots/{instance.telegram_bot_command.telegram_bot.id}/commands/{instance.telegram_bot_command.id}/files/{file_name}'

class TelegramBotCommandImage(models.Model):
	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(_('Изображение'), upload_to=upload_telegram_bot_command_image_path)

	class Meta:
		db_table = 'telegram_bot_command_image'

class TelegramBotCommandFile(models.Model):
	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.CASCADE, related_name='files')
	file = models.ImageField(_('Файл'), upload_to=upload_telegram_bot_command_file_path)

	class Meta:
		db_table = 'telegram_bot_command_file'

class TelegramBotCommandMessageText(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='message_text')
	text = models.TextField(_('Текст'), max_length=4096)

	class Meta:
		db_table = 'telegram_bot_command_message_text'

class TelegramBotCommandKeyboardManager(models.Manager):
	def create( # type: ignore [override]
		self,
		telegram_bot_command: 'TelegramBotCommand',
		type: str,
		buttons: list[dict[str, Any]]
	) -> 'TelegramBotCommandKeyboard':
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = super().create(telegram_bot_command=telegram_bot_command, type=type) # type: ignore [assignment]

		for button in buttons:
			TelegramBotCommandKeyboardButton.objects.create(
				telegram_bot_command_keyboard=telegram_bot_command_keyboard,
				row=button['row'],
				text=button['text'],
				url=button['url'],
			)

		return telegram_bot_command_keyboard

class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='keyboard')
	type = models.CharField(_('Режим'), max_length=7, choices=(
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
	), default='default')

	objects = TelegramBotCommandKeyboardManager()

	class Meta:
		db_table = 'telegram_bot_command_keyboard'

class TelegramBotCommandKeyboardButton(models.Model):
	telegram_bot_command_keyboard = models.ForeignKey(TelegramBotCommandKeyboard, on_delete=models.CASCADE, related_name='buttons')
	row = models.IntegerField(_('Ряд'), blank=True, null=True)
	text = models.TextField(_('Текст'), max_length=4096)
	url = models.TextField(_('URL-адрес'), max_length=2048, blank=True, null=True)

	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.SET_NULL, blank=True, null=True)
	start_diagram_connector = models.TextField(blank=True, null=True)
	end_diagram_connector = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_keyboard_button'
		ordering = ['id']

class TelegramBotCommandApiRequest(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='api_request')
	url = models.TextField(_('URL-адрес'), max_length=2048)
	method = models.CharField(_('Метод'), max_length=6, choices=(
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	), default='get')
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	body = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_api_request'

class TelegramBotCommandDatabaseRecord(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='database_record')
	data = models.JSONField(_('Данные'))

	class Meta:
		db_table = 'telegram_bot_command_database_record'

class TelegramBotVariable(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='variables', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=64)
	value = models.TextField(_('Значение'), max_length=2048)
	description = models.CharField(_('Описание'), max_length=255)

class TelegramBotUser(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', verbose_name=_('Telegram бот'))
	telegram_id = models.BigIntegerField('Telegram ID')
	full_name = models.CharField(_('Полное имя'), max_length=129, null=True)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	is_blocked = models.BooleanField(_('Заблокирован'), default=False)
	last_activity_date = models.DateTimeField(_('Дата последней активности'), auto_now_add=True, null=True)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def __str__(self) -> str:
		return self.full_name if self.full_name else str(self.telegram_id)