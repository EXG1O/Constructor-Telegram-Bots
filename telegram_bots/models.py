from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from utils.shortcuts import generate_random_string

from . import tasks
from .base_models import (
	AbstractAPIRequest,
	AbstractBlock,
	AbstractCommandMedia,
	AbstractDatabaseRecord,
)

from requests import Response
import requests

from collections.abc import Collection, Iterable
from itertools import chain
from typing import TYPE_CHECKING, Any
import hashlib
import os
import re
import string


def validate_api_token(api_token: str) -> None:
	if not settings.TEST and (
		not re.fullmatch(r'\d+:[A-Za-z0-9]+', api_token)
		or not requests.get(f'https://api.telegram.org/bot{api_token}/getMe').ok
	):
		raise ValidationError(_('Этот API-токен является недействительным!'))


class TelegramBot(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='telegram_bots',
		verbose_name=_('Владелец'),
	)
	username = models.CharField('@username', max_length=32)
	api_token = models.CharField(
		_('API-токен'),
		max_length=50,
		unique=True,
		validators=[validate_api_token],
		error_messages={
			'unique': _('Telegram бот с таким API-токеном уже существует.')
		},
	)
	storage_size = models.PositiveBigIntegerField(
		_('Размер хранилища'), default=41943040
	)
	is_private = models.BooleanField(_('Приватный'), default=False)
	is_enabled = models.BooleanField(_('Включён'), default=False)
	is_loading = models.BooleanField(_('Загружается'), default=False)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	if TYPE_CHECKING:
		_loaded_values: dict[str, Any]
		connections: models.Manager['Connection']
		commands: models.Manager['Command']
		conditions: models.Manager['Condition']
		background_tasks: models.Manager['BackgroundTask']
		variables: models.Manager['Variable']
		users: models.Manager['User']
		database_records: models.Manager['DatabaseRecord']

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot'
		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	@cached_property
	def used_storage_size(self) -> int:
		"""The property is cached, because it make heavy query to database."""

		return sum(
			media.file_field.size  # type: ignore [union-attr, misc]
			for media in chain(
				CommandImage.objects.filter(command__telegram_bot=self).exclude(
					image=None
				),
				CommandFile.objects.filter(command__telegram_bot=self).exclude(
					file=None
				),
			)
		)

	@property
	def remaining_storage_size(self) -> int:
		return self.storage_size - self.used_storage_size

	def start(self) -> None:
		if settings.TEST:
			return

		tasks.start_telegram_bot.delay(telegram_bot_id=self.id)

	def restart(self) -> None:
		if settings.TEST:
			return

		tasks.restart_telegram_bot.delay(telegram_bot_id=self.id)

	def stop(self) -> None:
		if settings.TEST:
			return

		tasks.stop_telegram_bot.delay(telegram_bot_id=self.id)

	def update_username(self) -> None:
		if settings.TEST:
			self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
			return

		response: Response = requests.get(
			f'https://api.telegram.org/bot{self.api_token}/getMe'
		)

		if response.ok:
			try:
				self.username = response.json()['result']['username']
			except KeyError:
				pass

	@classmethod
	def from_db(
		cls, db: str | None, field_names: Collection[str], values: Collection[Any]
	) -> 'TelegramBot':
		telegram_bot: TelegramBot = super().from_db(db, field_names, values)
		telegram_bot._loaded_values = dict(
			zip(
				field_names,
				(value for value in values if value is not models.DEFERRED),  # type: ignore [attr-defined]
				strict=False,
			)
		)

		return telegram_bot

	def save(
		self,
		force_insert: bool | tuple[ModelBase, ...] = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if not settings.TEST and (
			self._state.adding or self.api_token != self._loaded_values['api_token']
		):
			self.update_username()

			if not self._state.adding and self._loaded_values['is_enabled']:
				self.restart()

		super().save(force_insert, force_update, using, update_fields)

	def delete(
		self, using: str | None = None, keep_parents: bool = False
	) -> tuple[int, dict[str, int]]:
		if (
			not settings.TEST
			and not self._state.adding
			and self._loaded_values['is_enabled']
		):
			self.stop()

		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return f'@{self.username}'


class Connection(models.Model):
	HANDLE_POSITION_CHOICES = [
		('left', _('Слева')),
		('right', _('Справа')),
	]

	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='connections',
		verbose_name=_('Telegram бот'),
	)

	source_content_type = models.ForeignKey(
		ContentType, on_delete=models.CASCADE, related_name='source_connections'
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
		ContentType, on_delete=models.CASCADE, related_name='target_connections'
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
		indexes = [
			models.Index(
				fields=[
					'source_content_type',
					'source_object_id',
					'target_content_type',
					'target_object_id',
				]
			)
		]
		verbose_name = _('Подключение')
		verbose_name_plural = _('Подключения')


class CommandSettings(models.Model):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='settings',
		verbose_name=_('Команда'),
	)
	is_reply_to_user_message = models.BooleanField(
		_('Ответить на сообщение пользователя'), default=False
	)
	is_delete_user_message = models.BooleanField(
		_('Удалить сообщение пользователя'), default=False
	)
	is_send_as_new_message = models.BooleanField(
		_('Отправить сообщение как новое'), default=False
	)

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


def upload_command_media_path(instance: AbstractCommandMedia, file_name: str) -> str:
	name, ext = os.path.splitext(file_name)

	salt: str = generate_random_string(string.ascii_letters + string.digits, 15)
	hash: str = hashlib.sha256((name + salt).encode()).hexdigest()

	return f'telegram_bots/{name}_{hash}{ext}'


class CommandImage(AbstractCommandMedia):
	related_name = 'images'
	file_field_name = 'image'

	command = models.ForeignKey(
		'Command',
		on_delete=models.CASCADE,
		related_name=related_name,
		verbose_name=_('Команда'),
	)
	image = models.ImageField(
		_('Изображение'),
		upload_to=upload_command_media_path,
		max_length=500,
		blank=True,
		null=True,
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_image'
		verbose_name = _('Изображение команды')
		verbose_name_plural = _('Изображения команд')

	def __str__(self) -> str:
		return self.command.name


class CommandFile(AbstractCommandMedia):
	related_name = 'files'
	file_field_name = 'file'

	command = models.ForeignKey(
		'Command',
		on_delete=models.CASCADE,
		related_name=related_name,
		verbose_name=_('Команда'),
	)
	file = models.FileField(
		_('Файл'),
		upload_to=upload_command_media_path,
		max_length=500,
		blank=True,
		null=True,
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_file'
		verbose_name = _('Файл команды')
		verbose_name_plural = _('Файлы команд')

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
	row = models.PositiveSmallIntegerField(_('Ряд'))
	position = models.PositiveSmallIntegerField(_('Позиция'))
	text = models.TextField(_('Текст'), max_length=512)
	url = models.URLField(_('URL-адрес'), blank=True, null=True)
	source_connections = GenericRelation(
		'Connection', 'source_object_id', 'source_content_type'
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_keyboard_button'
		verbose_name = _('Кнопка клавиатуры команды')
		verbose_name_plural = _('Кнопки клавиатур команд')

	def __str__(self) -> str:
		return self.keyboard.command.name


class CommandKeyboard(models.Model):
	TYPE_CHOICES = [
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
	]

	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='keyboard',
		verbose_name=_('Команда'),
	)
	type = models.CharField(
		_('Режим'), max_length=7, choices=TYPE_CHOICES, default='default'
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


class CommandDatabaseRecord(AbstractDatabaseRecord):
	command = models.OneToOneField(
		'Command',
		on_delete=models.CASCADE,
		related_name='database_record',
		verbose_name=_('Команда'),
	)

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

	def delete(
		self, using: str | None = None, keep_parents: bool = False
	) -> tuple[int, dict[str, int]]:
		for file_path in chain(
			self.images.exclude(image=None).values_list('image', flat=True),
			self.files.exclude(file=None).values_list('file', flat=True),
		):
			try:
				os.remove(settings.MEDIA_ROOT / file_path)  # type: ignore [operator]
			except FileNotFoundError:
				pass

		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return self.name


class ConditionPart(models.Model):
	TYPE_CHOICES = [
		('+', _('Положительный')),
		('-', _('Отрицательный')),
	]
	OPERATOR_CHOICES = [
		('==', _('Равно')),
		('!=', _('Не равно')),
		('>', _('Больше')),
		('>=', _('Больше или равно')),
		('<', _('Меньше')),
		('<=', _('Меньше или равно')),
	]
	NEXT_PART_OPERATOR_CHOICES = [
		('&&', _('И')),
		('||', _('ИЛИ')),
	]

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
		parts: models.Manager[ConditionPart]

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
	INTERVAL_CHOICES = [
		(1, _('1 день')),
		(3, _('3 дня')),
		(7, _('7 дней')),
		(14, _('14 дней')),
		(28, _('28 дней')),
	]

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
	last_activity_date = models.DateTimeField(
		_('Дата последней активности'), auto_now_add=True
	)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_user'
		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def __str__(self) -> str:
		return self.full_name


class DatabaseRecord(AbstractDatabaseRecord):
	telegram_bot = models.ForeignKey(
		TelegramBot,
		on_delete=models.CASCADE,
		related_name='database_records',
		verbose_name=_('Telegram бот'),
	)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_database_record'
		verbose_name = _('Запись в БД')
		verbose_name_plural = _('Записи в БД')

	def __str__(self) -> str:
		return f"{self.telegram_bot.username} | {getattr(self, 'id', 'NULL')}"
