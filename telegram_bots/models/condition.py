from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from ..enums import (
    ConditionPartNextPartOperator,
    ConditionPartOperatorType,
    ConditionPartType,
)
from .base import AbstractBlock

from typing import TYPE_CHECKING


class ConditionPart(models.Model):
    condition = models.ForeignKey(
        'Condition',
        on_delete=models.CASCADE,
        related_name='parts',
        verbose_name=_('Условие'),
    )
    type = models.CharField(_('Тип'), max_length=1, choices=ConditionPartType)
    first_value = models.CharField(_('Первое значение'), max_length=255)
    operator = models.CharField(
        _('Оператор'), max_length=2, choices=ConditionPartOperatorType
    )
    second_value = models.CharField(_('Второе значение'), max_length=255)
    next_part_operator = models.CharField(
        _('Оператор для следующей части'),
        max_length=2,
        choices=ConditionPartNextPartOperator,
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
        'TelegramBot',
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
