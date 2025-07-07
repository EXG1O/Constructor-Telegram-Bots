from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class Variable(models.Model):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
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
