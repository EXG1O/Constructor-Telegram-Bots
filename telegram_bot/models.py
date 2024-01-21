from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import requests
from requests import Response


class TelegramBot(models.Model): # type: ignore [django-manager-missing]
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telegram_bots', verbose_name=_('Владелец'))
	username = models.CharField('@username', max_length=32)
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

class TelegramBotCommand(models.Model): # type: ignore [django-manager-missing]
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=128)

	x =	models.FloatField(_('Координата X'), default=0)
	y = models.FloatField(_('Координата Y'), default=0)

	class Meta:
		db_table = 'telegram_bot_command'

		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

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
	text = models.CharField(_('Команда'), max_length=255)
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

class TelegramBotCommandKeyboard(models.Model): # type: ignore [django-manager-missing]
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='keyboard')
	type = models.CharField(_('Режим'), max_length=7, choices=(
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
	), default='default')

	class Meta:
		db_table = 'telegram_bot_command_keyboard'

class TelegramBotCommandKeyboardButton(models.Model):
	telegram_bot_command_keyboard = models.ForeignKey(TelegramBotCommandKeyboard, on_delete=models.CASCADE, related_name='buttons')
	row = models.IntegerField(_('Ряд'), blank=True, null=True)
	text = models.TextField(_('Текст'), max_length=4096)
	url = models.URLField(_('URL-адрес'), blank=True, null=True)

	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.SET_NULL, blank=True, null=True)
	start_diagram_connector = models.TextField(max_length=1024, blank=True, null=True)
	end_diagram_connector = models.TextField(max_length=1024, blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_keyboard_button'
		ordering = ['id']

class TelegramBotCommandApiRequest(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='api_request')
	url = models.URLField(_('URL-адрес'))
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