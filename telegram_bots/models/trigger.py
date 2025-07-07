from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from .base import AbstractBlock

from typing import TYPE_CHECKING


class TriggerCommand(models.Model):
    trigger = models.OneToOneField(
        'Trigger',
        on_delete=models.CASCADE,
        related_name='command',
        verbose_name=_('Триггер'),
    )
    command = models.CharField(_('Команда'), max_length=32)
    payload = models.CharField(
        _('Полезная нагрузка'), max_length=64, blank=True, null=True
    )
    description = models.CharField(_('Описание'), max_length=255, blank=True, null=True)

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_trigger_command'
        verbose_name = _('Команда триггер')
        verbose_name_plural = _('Команды триггеры')

    def __str__(self) -> str:
        return self.command


class TriggerMessage(models.Model):
    trigger = models.OneToOneField(
        'Trigger',
        on_delete=models.CASCADE,
        related_name='message',
        verbose_name=_('Триггер'),
    )
    text = models.TextField(_('Текст'), max_length=4096)

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_trigger_message'
        verbose_name = _('Сообщение триггер')
        verbose_name_plural = _('Сообщения триггеры')

    def __str__(self) -> str:
        return self.text[:128]


class Trigger(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='triggers',
        verbose_name=_('Telegram бот'),
    )
    target_connections = None

    if TYPE_CHECKING:
        command: TriggerCommand
        message: TriggerMessage

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_trigger'
        verbose_name = _('Триггер')
        verbose_name_plural = _('Триггеры')

    def __str__(self) -> str:
        return self.name
