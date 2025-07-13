from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.fields import PublicURLField

from ..enums import APIRequestMethod
from .base import AbstractBlock


class APIRequest(AbstractBlock):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='api_requests',
        verbose_name=_('Telegram бот'),
    )
    url = PublicURLField(_('URL-адрес'))
    method = models.CharField(
        _('Метод'), max_length=6, choices=APIRequestMethod, default=APIRequestMethod.GET
    )
    headers = models.JSONField(_('Заголовки'), blank=True, null=True)
    body = models.JSONField(_('Данные'), blank=True, null=True)

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_api_request'
        verbose_name = _('API-запрос')
        verbose_name_plural = _('API-запрос')

    def __str__(self) -> str:
        return self.name
