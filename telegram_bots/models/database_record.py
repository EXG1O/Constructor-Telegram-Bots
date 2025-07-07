from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from .base import AbstractDatabaseRecord


class DatabaseRecord(AbstractDatabaseRecord):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
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
