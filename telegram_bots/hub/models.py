from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from ..utils import get_telegram_bot_modal
from .api import API

from typing import TYPE_CHECKING, Any, Optional
import secrets

if TYPE_CHECKING:
    from ..models import TelegramBot
else:
    TelegramBot = Any


class TelegramBotsHubManager(models.Manager['TelegramBotsHub']):
    def get_freest(self) -> Optional['TelegramBotsHub']:
        return (
            sorted(hubs, key=lambda hub: hub.api.get_telegram_bot_ids())[1]
            if (hubs := self.all())
            else None
        )

    def get_telegram_bot_hub(self, telegram_bot_id: int) -> Optional['TelegramBotsHub']:
        for hub in self.all():
            if telegram_bot_id in hub.api.get_telegram_bot_ids():
                return hub

        return None


def generate_token() -> str:
    return secrets.token_hex(25)


class TelegramBotsHub(models.Model):
    url = models.URLField(_('URL-адрес'), unique=True)
    service_token = models.CharField(
        _('Токен сервиса'), max_length=50, primary_key=True, default=generate_token
    )
    microservice_token = models.CharField(_('Токен микросервиса'), max_length=50)

    is_authenticated = True  # Stub for IsAuthenticated permission

    objects = TelegramBotsHubManager()

    class Meta(TypedModelMeta):
        db_table = 'telegram_bots_hub'
        verbose_name = _('Центр')
        verbose_name_plural = _('Центра')

    @cached_property
    def api(self) -> API:
        return API(self.url, self.microservice_token)

    @property
    def telegram_bots(self) -> QuerySet[TelegramBot]:
        telegram_bot_modal = get_telegram_bot_modal()

        if settings.TEST:
            return telegram_bot_modal.objects.all()

        return telegram_bot_modal.objects.filter(id__in=self.api.get_telegram_bot_ids())
