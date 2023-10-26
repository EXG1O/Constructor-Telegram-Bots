from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from user.models import User

from .services import database_telegram_bot

import requests
from requests import Response

from typing import Optional
from asgiref.sync import sync_to_async


class TelegramBot(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_bots', verbose_name=_('Владелец'))
	username = models.CharField('@username', max_length=32, null=True)
	api_token = models.CharField(_('API-токен'), max_length=50, unique=True)
	is_private = models.BooleanField(_('Приватный'), default=False)
	is_running = models.BooleanField(_('Включён'), default=False)
	is_stopped = models.BooleanField(default=True)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	diagram_current_scale = models.FloatField(default=1.0)

	class Meta:
		db_table = 'telegram_bot'

		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	# TODO: Надо реализовать метод start для запуска Telegram бота, но проблема в том, что происходит циклический импорт.

	def stop(self) -> None:
		self.is_running = False
		self.save()

	def update_username(self) -> None:
		if settings.TEST:
			self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
			self.save()
		else:
			responce: Response = requests.get(f'https://api.telegram.org/bot{self.api_token}/getMe')

			if responce.status_code == 200:
				self.username = responce.json()['result']['username']
				self.save()
			else:
				self.delete()

	def __str__(self) -> str:
		return f'@{self.username}'

@receiver(post_save, sender=TelegramBot)
def post_save_telegram_bot_signal(instance: TelegramBot, created: bool, **kwargs) -> None:
	if created:
		instance.update_username()

@receiver(post_delete, sender=TelegramBot)
def post_delete_telegram_bot_signal(instance: TelegramBot, **kwargs) -> None:
	database_telegram_bot.delete_collection(instance)

class TelegramBotCommandManager(models.Manager):
	def create(
		self,
		telegram_bot: TelegramBot,
		name: str,
		command: dict | None,
		image: InMemoryUploadedFile | str | None,
		message_text: dict,
		keyboard: dict | None,
		api_request: dict | None,
		database_record: dict | None,
	) -> 'TelegramBotCommand':
		telegram_bot_command: TelegramBotCommand = super().create(
			telegram_bot=telegram_bot,
			name=name,
			image=image if isinstance(image, InMemoryUploadedFile) else None,
			database_record=database_record
		)

		if command:
			TelegramBotCommandCommand.objects.create(telegram_bot_command=telegram_bot_command, **command)

		TelegramBotCommandMessageText.objects.create(telegram_bot_command=telegram_bot_command, **message_text)

		if keyboard:
			TelegramBotCommandKeyboard.objects.create(telegram_bot_command=telegram_bot_command, **keyboard)

		if api_request:
			TelegramBotCommandApiRequest.objects.create(telegram_bot_command=telegram_bot_command, **api_request)

		return telegram_bot_command

	async def acreate(self, *args, **kwargs) -> 'TelegramBotCommand':
		return await sync_to_async(self.create)(*args, **kwargs)

def upload_telegram_bot_command_image_path(telegram_bot_command: 'TelegramBotCommand', file_name: str):
	return f'telegram_bots/{telegram_bot_command.telegram_bot.id}/commands/{file_name}'

class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)
	image = models.ImageField(_('Изображение'), upload_to=upload_telegram_bot_command_image_path, blank=True, null=True)
	database_record = models.JSONField(_('Запись в базу данных'), blank=True, null=True)

	x =	models.IntegerField(_('Координата X'), default=0)
	y = models.IntegerField(_('Координата Y'), default=0)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

	def get_command(self) -> Optional['TelegramBotCommandCommand']:
		try:
			return self.command
		except TelegramBotCommandCommand.DoesNotExist:
			return None

	async def aget_command(self) -> Optional['TelegramBotCommandCommand']:
		return await sync_to_async(self.get_command)()

	def get_message_text(self) -> Optional['TelegramBotCommandMessageText']:
		try:
			return self.message_text
		except TelegramBotCommandMessageText.DoesNotExist:
			return None

	async def aget_message_text(self) -> Optional['TelegramBotCommandMessageText']:
		return await sync_to_async(self.get_message_text)()

	def get_keyboard(self) -> Optional['TelegramBotCommandKeyboard']:
		try:
			return self.keyboard
		except TelegramBotCommandKeyboard.DoesNotExist:
			return None

	async def aget_keyboard(self) -> Optional['TelegramBotCommandKeyboard']:
		return await sync_to_async(self.get_keyboard)()

	def get_api_request(self) -> Optional['TelegramBotCommandApiRequest']:
		try:
			return self.api_request
		except TelegramBotCommandApiRequest.DoesNotExist:
			return None

	async def aget_api_request(self) -> Optional['TelegramBotCommandApiRequest']:
		return await sync_to_async(self.get_api_request)()

	def update(
		self,
		name: str,
		command: dict | None,
		image: InMemoryUploadedFile | str | None,
		message_text: dict,
		keyboard: dict | None,
		api_request: dict | None,
		database_record: dict | None,
	):
		self.name = name
		self.database_record = database_record
		self.save()

		telegram_bot_command_command: TelegramBotCommandCommand | None = self.get_command()

		if command:
			if telegram_bot_command_command:
				telegram_bot_command_command.text = command['text']
				telegram_bot_command_command.is_show_in_menu = command['is_show_in_menu']
				telegram_bot_command_command.description = command['description']
				telegram_bot_command_command.save()
			else:
				TelegramBotCommandCommand.objects.create(telegram_bot_command=self, **command)
		else:
			if telegram_bot_command_command:
				telegram_bot_command_command.delete()

		if isinstance(image, InMemoryUploadedFile) or image == 'null' and self.image != None:
			self.image.delete(save=False)

			if isinstance(image, InMemoryUploadedFile):
				self.image = image

			self.save()

		self.message_text.text = message_text['text']
		self.message_text.save()

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard | None = self.get_keyboard()

		if keyboard:
			if telegram_bot_command_keyboard:
				telegram_bot_command_keyboard.mode = keyboard['mode']
				telegram_bot_command_keyboard.save()

				buttons_id = []

				for button in keyboard['buttons']:
					is_finded_button = False

					if button['id']:
						button_id = int(button['id'])

						for button_ in telegram_bot_command_keyboard.buttons.all():
							if button_id == button_.id:
								is_finded_button = True
								break

					if is_finded_button:
						button_: TelegramBotCommandKeyboardButton = telegram_bot_command_keyboard.buttons.get(id=button_id)
						button_.row = button['row']
						button_.text = button['text']
						button_.url = button['url']
						button_.save()
					else:
						button_: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create(
							telegram_bot_command_keyboard=telegram_bot_command_keyboard,
							**button
						)

					buttons_id.append(button_.id)

				for button in telegram_bot_command_keyboard.buttons.all():
					if button.id not in buttons_id:
						button.delete()
			else:
				TelegramBotCommandKeyboard.objects.create(telegram_bot_command=self, **keyboard)
		else:
			if telegram_bot_command_keyboard:
				telegram_bot_command_keyboard.delete()

		telegram_bot_command_api_request: TelegramBotCommandApiRequest | None = self.get_api_request()

		if api_request:
			if telegram_bot_command_api_request:
				telegram_bot_command_api_request.url = api_request['url']
				telegram_bot_command_api_request.method = api_request['method']
				telegram_bot_command_api_request.headers = api_request['headers']
				telegram_bot_command_api_request.data = api_request['data']
				telegram_bot_command_api_request.save()
			else:
				TelegramBotCommandApiRequest.objects.create(telegram_bot_command=self, **api_request)
		else:
			if telegram_bot_command_api_request:
				telegram_bot_command_api_request.delete()

	def __str__(self) -> str:
		return self.name

@receiver(post_delete, sender=TelegramBotCommand)
def post_delete_telegram_bot_signal(instance: TelegramBotCommand, **kwargs) -> None:
	instance.image.delete(save=False)

class TelegramBotCommandCommand(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='command')
	text = models.CharField(_('Команда'), max_length=32)
	is_show_in_menu = models.BooleanField(_('Отображать в меню'), default=False)
	description = models.CharField(_('Описание'), max_length=255, blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_command'

class TelegramBotCommandMessageText(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='message_text')
	text = models.TextField(_('Текст'), max_length=4096)

	class Meta:
		db_table = 'telegram_bot_command_message_text'

class TelegramBotCommandKeyboardManager(models.Manager):
	def create(
		self,
		telegram_bot_command: TelegramBotCommand,
		mode: str,
		buttons: list
	) -> 'TelegramBotCommandKeyboard':
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = super().create(telegram_bot_command=telegram_bot_command, mode=mode)

		for button in buttons:
			TelegramBotCommandKeyboardButton.objects.create(
				telegram_bot_command_keyboard=telegram_bot_command_keyboard,
				row=button['row'],
				text=button['text'],
				url=button['url']
			)

		return telegram_bot_command_keyboard

class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='keyboard')
	mode = models.CharField(_('Режим'), max_length=7, choices=(
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

	telegram_bot_command = models.ForeignKey(TelegramBotCommand, on_delete=models.SET_NULL, blank=True, null=True)

	start_diagram_connector = models.TextField(blank=True, null=True)
	end_diagram_connector = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_keyboard_button'
		ordering = ['id']

	def get_telegram_bot_command(self) -> TelegramBotCommand | None:
		return self.telegram_bot_command

	async def aget_telegram_bot_command(self) -> TelegramBotCommand | None:
		return await sync_to_async(self.get_telegram_bot_command)()

class TelegramBotCommandApiRequest(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='api_request')
	url = models.TextField(_('URL-адрес'), max_length=2048)
	method = models.CharField(_('Метод'), max_length=6, choices=(
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	), default='get')
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	data = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_api_request'

class TelegramBotUser(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', verbose_name=_('Telegram бот'))
	user_id = models.BigIntegerField('Telegram ID')
	full_name = models.CharField(_('Полное имя'), max_length=129, null=True)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def __str__(self) -> str:
		return self.full_name if self.full_name else str(self.user_id)
