from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from .base import AbstractBlock, AbstractMedia, upload_media_path

from typing import TYPE_CHECKING


class InvoiceImage(AbstractMedia):
    related_name = 'image'

    invoice = models.OneToOneField(
        'Invoice',
        on_delete=models.CASCADE,
        related_name=related_name,
        verbose_name=_('Счёт'),
    )
    file = models.ImageField(
        _('Изображение'),
        upload_to=upload_media_path,
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_invoice_image'
        verbose_name = _('Изображение счёта')
        verbose_name_plural = _('Изображения счетов')

    def __str__(self) -> str:
        return self.file.url if self.file else self.from_url or 'ERROR'


class InvoicePrice(models.Model):
    invoice = models.ForeignKey(
        'Invoice',
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name=_('Счёт'),
    )
    label = models.CharField(_('Подпись'), max_length=128)
    amount = models.PositiveIntegerField(_('Сумма'), validators=[MinValueValidator(1)])

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_invoice_price'
        verbose_name = _('Цена счёта')
        verbose_name_plural = _('Цены счетов')

    def __str__(self) -> str:
        return f'{self.label} | {self.amount}'


class Invoice(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name=_('Telegram бот'),
    )
    title = models.CharField(_('Заголовок'), max_length=32)
    description = models.CharField(_('Описание'), max_length=255)

    if TYPE_CHECKING:
        image: InvoiceImage
        prices: models.Manager[InvoicePrice]

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_invoice'
        verbose_name = _('Счёт')
        verbose_name_plural = _('Счета')

    def __str__(self) -> str:
        return self.name
