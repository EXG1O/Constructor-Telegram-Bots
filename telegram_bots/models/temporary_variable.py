from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.validators import validate_no_special_chars

from .base import AbstractBlock


class TemporaryVariable(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='temporary_variables',
        verbose_name=_('Telegram бот'),
    )
    name = models.CharField(
        _('Название'), max_length=64, validators=[validate_no_special_chars]
    )
    value = models.CharField(_('Значение'), max_length=255)

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_temporary_variable'
        verbose_name = _('Временная переменная')
        verbose_name_plural = _('Временные переменные')

    def __str__(self) -> str:
        return self.name
