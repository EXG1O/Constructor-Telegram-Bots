from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_stubs_ext.db.models import TypedModelMeta

from . import tasks

import requests
from requests import Response

from typing import TYPE_CHECKING, Iterable


def validate_api_token(api_token: str) -> None:
	if not settings.TEST and not requests.get(f'https://api.telegram.org/bot{api_token}/getMe').ok:
		raise ValidationError(_('Ваш API-токен Telegram бота является недействительным!'))

class TelegramBot(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='telegram_bots',
		verbose_name=_('Владелец'),
	)
	username = models.CharField('@username', max_length=32)
	api_token = models.CharField(_('API-токен'), max_length=50, unique=True, validators=(validate_api_token,))
	storage_size = models.PositiveBigIntegerField(_('Размер хранилища'), default=41943040)
	is_private = models.BooleanField(_('Приватный'), default=False)
	is_enabled = models.BooleanField(_('Включён'), default=False)
	is_loading = models.BooleanField(_('Загружаеться'), default=False)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	if TYPE_CHECKING:
		connections: models.Manager['Connection']
		commands: models.Manager['Command']
		conditions: models.Manager['Condition']
		background_tasks: models.Manager['BackgroundTask']
		variables: models.Manager['Variable']
		users: models.Manager['User']

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot'
		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	@property
	def used_storage_size(self) -> int:
		size: int = 0

		for command in self.commands.all():
			size += sum(file.file.size for file in command.files.all())
			size += sum(image.image.size for image in command.images.all())

		return size

	@property
	def remaining_storage_size(self) -> int:
		return self.storage_size - self.used_storage_size

	def start(self) -> None:
		tasks.start_telegram_bot.delay(telegram_bot_id=self.id)

	def restart(self) -> None:
		tasks.restart_telegram_bot.delay(telegram_bot_id=self.id)

	def stop(self) -> None:
		tasks.stop_telegram_bot.delay(telegram_bot_id=self.id)

	def update_username(self) -> None:
		if settings.TEST:
			self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
		else:
			responce: Response = requests.get(f'https://api.telegram.org/bot{self.api_token}/getMe')

			if responce.ok:
				self.username = responce.json()['result']['username']

	def save(
		self,
		force_insert: bool = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if not self._state.adding:
			telegram_bot: TelegramBot = TelegramBot.objects.get(id=self.id)

			if self.api_token != telegram_bot.api_token:
				self.update_username()

				if self.is_enabled and telegram_bot.is_enabled:
					self.restart()
		else:
			self.update_username()

		super().save(force_insert, force_update, using, update_fields)

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		if not self._state.adding:
			telegram_bot: TelegramBot = TelegramBot.objects.get(id=self.id)

			if self.is_enabled and telegram_bot.is_enabled:
				self.stop()

		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return f'@{self.username}'

class AbstractBlock(models.Model):
	name = models.CharField(_('Название'), max_length=128)
	x =	models.FloatField(_('Координата X'), default=0)
	y = models.FloatField(_('Координата Y'), default=0)
	source_connections = GenericRelation('Connection', 'source_object_id', 'source_content_type')
	target_connections = GenericRelation('Connection', 'target_object_id', 'target_content_type')

	class Meta(TypedModelMeta):
		abstract = True

	def __str__(self) -> str:
		return self.name

class Connection(models.Model):
	HANDLE_POSITION_CHOICES = (
		('left', _('Слева')),
		('right', _('Справа')),
	)

	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='connections',
		verbose_name=_('Telegram бот'),
	)

	source_content_type = models.ForeignKey(
		ContentType,
		on_delete=models.CASCADE,
		related_name='source_connections',
	)
	source_object_id = models.PositiveBigIntegerField()
	source_object = GenericForeignKey('source_content_type', 'source_object_id')
	source_handle_position = models.CharField(
		_('Стартовая позиция коннектора'),
		max_length=5,
		choices=HANDLE_POSITION_CHOICES,
		default='left',
	)

	target_content_type = models.ForeignKey(
		ContentType,
		on_delete=models.CASCADE,
		related_name='target_connections',
	)
	target_object_id = models.PositiveBigIntegerField()
	target_object = GenericForeignKey('target_content_type', 'target_object_id')
	target_handle_position = models.CharField(
		_('Окончательная позиция коннектора'),
		max_length=5,
		choices=HANDLE_POSITION_CHOICES,
		default='right',
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_connection'
		verbose_name = _('Подключение')
		verbose_name_plural = _('Подключения')

class AbstractAPIRequest(models.Model):
	METHOD_CHOICES = (
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	)

	url = models.URLField(_('URL-адрес'))
	method = models.CharField(_('Метод'), max_length=6, choices=METHOD_CHOICES, default='get')
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	body = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta(TypedModelMeta):
		abstract = True

	def __str__(self) -> str:
		return self.url

class CommandSettings(models.Model):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='settings',
		verbose_name=_('Команда'),
	)
	is_reply_to_user_message = models.BooleanField(_('Ответить на сообщение пользователя'), default=False)
	is_delete_user_message = models.BooleanField(_('Удалить сообщение пользователя'), default=False)
	is_send_as_new_message = models.BooleanField(_('Отправить сообщение как новое'), default=False)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_settings'
		verbose_name = _('Настройки команды')
		verbose_name_plural = _('Настройки команд')

	def __str__(self) -> str:
		return self.command.name

class CommandTrigger(models.Model):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='trigger',
		verbose_name=_('Команда'),
	)
	text = models.CharField(_('Текст'), max_length=255)
	description = models.CharField(_('Описание'), max_length=255, blank=True, null=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_trigger'
		verbose_name = _('Триггер команды')
		verbose_name_plural = _('Триггеры команд')

	def __str__(self) -> str:
		return self.command.name

def upload_command_image_path(instance: 'CommandImage', file_name: str) -> str:
	return f'telegram_bots/{instance.command.telegram_bot.id}/commands/{instance.command.id}/images/{file_name}'

def upload_command_file_path(instance: 'CommandFile', file_name: str) -> str:
	return f'telegram_bots/{instance.command.telegram_bot.id}/commands/{instance.command.id}/files/{file_name}'

class CommandImage(models.Model):
	command = models.ForeignKey(
		'Command',
		on_delete=models.CASCADE,
		related_name='images',
		verbose_name=_('Команда'),
	)
	image = models.ImageField(_('Изображение'), upload_to=upload_command_image_path)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_image'
		verbose_name = _('Изображение команды')
		verbose_name_plural = _('Изображения команд')

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		self.image.delete(save=False)
		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return self.command.name

class CommandFile(models.Model):
	command = models.ForeignKey(
		'Command',
		on_delete=models.CASCADE,
		related_name='files',
		verbose_name=_('Команда'),
	)
	file = models.ImageField(_('Файл'), upload_to=upload_command_file_path)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_file'
		verbose_name = _('Файл команды')
		verbose_name_plural = _('Файлы команд')

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		self.file.delete(save=False)
		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return self.command.name

class CommandMessage(models.Model):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='message',
		verbose_name=_('Команда'),
	)
	text = models.TextField(_('Текст'), max_length=4096)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_message'
		verbose_name = _('Сообщение команды')
		verbose_name_plural = _('Сообщения команд')

	def __str__(self) -> str:
		return self.command.name

class CommandKeyboardButton(models.Model):
	keyboard = models.ForeignKey(
		'CommandKeyboard',
		on_delete=models.CASCADE,
		related_name='buttons',
		verbose_name=_('Клавиатура'),
	)
	row = models.PositiveSmallIntegerField(_('Ряд'), blank=True, null=True)
	text = models.TextField(_('Текст'), max_length=512)
	url = models.URLField(_('URL-адрес'), blank=True, null=True)
	source_connections = GenericRelation('Connection', 'source_object_id', 'source_content_type')

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_keyboard_button'
		verbose_name = _('Кнопка клавиатуры команды')
		verbose_name_plural = _('Кнопки клавиатур команд')

	def __str__(self) -> str:
		return self.keyboard.command.name

class CommandKeyboard(models.Model):
	TYPE_CHOICES = (
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
	)

	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='keyboard',
		verbose_name=_('Команда'),
	)
	type = models.CharField(
		_('Режим'),
		max_length=7,
		choices=TYPE_CHOICES,
		default='default',
	)

	if TYPE_CHECKING:
		buttons: models.Manager[CommandKeyboardButton]

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_keyboard'
		verbose_name = _('Клавиатура команды')
		verbose_name_plural = _('Клавиатуры команд')

	def __str__(self) -> str:
		return self.command.name

class CommandAPIRequest(AbstractAPIRequest):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='api_request',
		verbose_name=_('Команда'),
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_api_request'
		verbose_name = _('API-запрос команды')
		verbose_name_plural = _('API-запросы команд')

	def __str__(self) -> str:
		return self.command.name

class CommandDatabaseRecord(models.Model):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='database_record',
		verbose_name=_('Команда'),
	)
	data = models.JSONField(_('Данные'))

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_database_record'
		verbose_name = _('Запись в БД команды')
		verbose_name_plural = _('Записи в БД команд')

	def __str__(self) -> str:
		return self.command.name

class Command(AbstractBlock):
	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='commands',
		verbose_name=_('Telegram бот'),
	)

	if TYPE_CHECKING:
		settings: CommandSettings
		trigger: CommandTrigger
		images: models.Manager[CommandImage]
		files: models.Manager[CommandFile]
		message: CommandMessage
		keyboard: CommandKeyboard
		api_request: CommandAPIRequest
		database_record: CommandDatabaseRecord

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command'
		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

	def __str__(self) -> str:
		return self.name

class ConditionPart(models.Model):
	TYPE_CHOICES = (
		('+', _('Положительный')),
		('-', _('Отрицательный')),
	)
	OPERATOR_CHOICES = (
		('==', _('Равно')),
		('!=', _('Не равно')),
		('>', _('Больше')),
		('>=', _('Больше или равно')),
		('<', _('Меньше')),
		('<=', _('Меньше или равно')),
	)
	NEXT_PART_OPERATOR_CHOICES = (
		('&&', _('И')),
		('||', _('ИЛИ')),
	)

	condition = models.ForeignKey(
		'Condition',
		on_delete=models.CASCADE,
		related_name='parts',
		verbose_name=_('Условие'),
	)
	type = models.CharField(_('Тип'), max_length=1, choices=TYPE_CHOICES)
	first_value = models.CharField(_('Первое значение'), max_length=255)
	operator = models.CharField(_('Оператор'), max_length=2, choices=OPERATOR_CHOICES)
	second_value = models.CharField(_('Второе значение'), max_length=255)
	next_part_operator = models.CharField(
		_('Оператор для следующей части'),
		max_length=2,
		choices=NEXT_PART_OPERATOR_CHOICES,
		blank=True,
		null=True,
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_condition_part'
		verbose_name = _('Часть условия')
		verbose_name_plural = _('Части условий')

	def __str__(self) -> str:
		return self.condition.name

class Condition(AbstractBlock):
	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='conditions',
		verbose_name=_('Telegram бот'),
	)

	if TYPE_CHECKING:
		parts = models.Manager[ConditionPart]

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_condition'
		verbose_name = _('Условие')
		verbose_name_plural = _('Условия')

	def __str__(self) -> str:
		return self.name

class BackgroundTaskAPIRequest(AbstractAPIRequest):
	background_task = models.OneToOneField(
		'BackgroundTask',
		on_delete=models.CASCADE,
		related_name='api_request',
		verbose_name=_('Фоновая задача'),
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_background_task_api_request'
		verbose_name = _('API-запрос фоновой задачи')
		verbose_name_plural = _('API-запросы фоновых задач')

	def __str__(self) -> str:
		return self.url

class BackgroundTask(AbstractBlock):
	INTERVAL_CHOICES = (
		(1, _('1 день')),
		(3, _('3 дня')),
		(7, _('7 дней')),
		(14, _('14 дней')),
		(28, _('28 дней')),
	)

	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='background_tasks',
		verbose_name=_('Telegram бот'),
	)
	interval = models.PositiveSmallIntegerField(_('Интервал'), choices=INTERVAL_CHOICES)
	source_connections = None

	if TYPE_CHECKING:
		api_request: BackgroundTaskAPIRequest

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_background_task'
		verbose_name = _('Фоновая задача')
		verbose_name_plural = _('Фоновые задачи')

	def __str__(self) -> str:
		return self.name

class Variable(models.Model):
	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='variables',
		verbose_name=_('Telegram бот'),
	)
	name = models.CharField(_('Название'), max_length=64)
	value = models.TextField(_('Значение'), max_length=2048)
	description = models.CharField(_('Описание'), max_length=255)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_variable'
		verbose_name = _('Переменная')
		verbose_name_plural = _('Переменные')

	def __str__(self) -> str:
		return self.name

class User(models.Model):
	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='users',
		verbose_name=_('Telegram бот'),
	)
	telegram_id = models.PositiveBigIntegerField('Telegram ID')
	full_name = models.CharField(_('Имя и фамилия'), max_length=129)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	is_blocked = models.BooleanField(_('Заблокирован'), default=False)
	last_activity_date = models.DateTimeField(_('Дата последней активности'), auto_now_add=True)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_user'
		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def __str__(self) -> str:
		return self.full_name