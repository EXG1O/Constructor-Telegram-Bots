from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from ..enums import BackgroundTaskInterval
from .base import AbstractBlock


class BackgroundTask(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='background_tasks',
        verbose_name=_('Telegram бот'),
    )
    interval = models.PositiveSmallIntegerField(
        _('Интервал'), choices=BackgroundTaskInterval
    )
    target_connections = None

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_background_task'
        verbose_name = _('Фоновая задача')
        verbose_name_plural = _('Фоновые задачи')

    def __str__(self) -> str:
        return self.name
