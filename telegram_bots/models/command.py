from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.fields import PublicURLField

from ..enums import KeyboardType
from .base import AbstractBlock, AbstractCommandMedia

from contextlib import suppress
from itertools import chain
from typing import TYPE_CHECKING, cast
import hashlib
import os
import secrets


class CommandSettings(models.Model):
    command = models.OneToOneField(
        'Command',
        on_delete=models.CASCADE,
        related_name='settings',
        verbose_name=_('Команда'),
    )
    reply_to_user_message = models.BooleanField(
        _('Ответить на сообщение пользователя'), default=False
    )
    delete_user_message = models.BooleanField(
        _('Удалить сообщение пользователя'), default=False
    )
    send_as_new_message = models.BooleanField(
        _('Отправить сообщение как новое'), default=True
    )

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_command_settings'
        verbose_name = _('Настройки команды')
        verbose_name_plural = _('Настройки команд')

    def __str__(self) -> str:
        return self.command.name


def upload_command_media_path(instance: AbstractCommandMedia, file_name: str) -> str:
    name, ext = os.path.splitext(file_name)

    salt: str = secrets.token_hex(8)
    hash: str = hashlib.sha256((name + salt).encode()).hexdigest()

    return f'telegram_bots/{name}_{hash}{ext}'


class CommandImage(AbstractCommandMedia):
    related_name = 'images'

    command = models.ForeignKey(
        'Command',
        on_delete=models.CASCADE,
        related_name=related_name,
        verbose_name=_('Команда'),
    )
    file = models.ImageField(
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


class CommandDocument(AbstractCommandMedia):
    related_name = 'documents'

    command = models.ForeignKey(
        'Command',
        on_delete=models.CASCADE,
        related_name=related_name,
        verbose_name=_('Команда'),
    )
    file = models.FileField(
        _('Документ'),
        upload_to=upload_command_media_path,
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_command_document'
        verbose_name = _('Документ команды')
        verbose_name_plural = _('Документы команд')

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
    url = PublicURLField(_('URL-адрес'), blank=True, null=True)
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
    command = models.OneToOneField(
        'Command',
        on_delete=models.CASCADE,
        related_name='keyboard',
        verbose_name=_('Команда'),
    )
    type = models.CharField(
        _('Режим'), max_length=7, choices=KeyboardType, default=KeyboardType.DEFAULT
    )

    if TYPE_CHECKING:
        buttons: models.Manager[CommandKeyboardButton]

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_command_keyboard'
        verbose_name = _('Клавиатура команды')
        verbose_name_plural = _('Клавиатуры команд')

    def __str__(self) -> str:
        return self.command.name


class Command(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='commands',
        verbose_name=_('Telegram бот'),
    )
    source_connections = None

    if TYPE_CHECKING:
        settings: CommandSettings
        images: models.Manager[CommandImage]
        documents: models.Manager[CommandDocument]
        message: CommandMessage
        keyboard: CommandKeyboard

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_command'
        verbose_name = _('Команда')
        verbose_name_plural = _('Команды')

    def delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        for file_path in chain(
            self.images.exclude(file=None).values_list('file', flat=True),
            self.documents.exclude(file=None).values_list('file', flat=True),
        ):
            file_path = cast(str, file_path)

            with suppress(FileNotFoundError):
                os.remove(settings.MEDIA_ROOT / file_path)

        return super().delete(using, keep_parents)

    def __str__(self) -> str:
        return self.name
