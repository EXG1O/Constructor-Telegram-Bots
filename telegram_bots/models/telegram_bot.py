from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from .. import tasks
from ..hub.models import TelegramBotsHub
from .api_request import APIRequest
from .background_task import BackgroundTask
from .command import (
    Command,
    CommandDocument,
    CommandImage,
)
from .condition import Condition
from .connection import Connection
from .database_record import DatabaseRecord
from .trigger import Trigger
from .user import User
from .variable import Variable

from requests import Response
import requests

from collections.abc import Collection, Iterable
from contextlib import suppress
from itertools import chain
from typing import TYPE_CHECKING, Any
import re


def validate_api_token(api_token: str) -> None:
    if not settings.TEST and (
        not re.fullmatch(r'^\d+:.+$', api_token)
        or not requests.get(f'https://api.telegram.org/bot{api_token}/getMe').ok
    ):
        raise ValidationError(_('Этот API-токен является недействительным.'))


class TelegramBot(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='telegram_bots',
        verbose_name=_('Владелец'),
    )
    username = models.CharField('@username', max_length=32)
    api_token = models.CharField(
        _('API-токен'),
        max_length=50,
        unique=True,
        validators=[validate_api_token],
        error_messages={
            'unique': _('Telegram бот с таким API-токеном уже существует.')
        },
    )
    storage_size = models.PositiveBigIntegerField(
        _('Размер хранилища'), default=41943040
    )
    is_private = models.BooleanField(_('Приватный'), default=False)
    must_be_enabled = models.BooleanField(_('Должен быть включен'), default=False)
    is_loading = models.BooleanField(_('Загружается'), default=False)
    added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

    if TYPE_CHECKING:
        _loaded_values: dict[str, Any]
        connections: models.Manager[Connection]
        triggers: models.Manager[Trigger]
        commands: models.Manager[Command]
        conditions: models.Manager[Condition]
        background_tasks: models.Manager[BackgroundTask]
        api_requests: models.Manager[APIRequest]
        variables: models.Manager[Variable]
        users: models.Manager[User]
        database_records: models.Manager[DatabaseRecord]

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot'
        verbose_name = _('Telegram бота')
        verbose_name_plural = _('Telegram боты')

    @cached_property
    def used_storage_size(self) -> int:
        """The property is cached, because it make heavy query to database."""

        return sum(
            media.file.size
            for media in chain(
                CommandImage.objects.filter(command__telegram_bot=self).exclude(
                    file=None
                ),
                CommandDocument.objects.filter(command__telegram_bot=self).exclude(
                    file=None
                ),
            )
        )

    @property
    def remaining_storage_size(self) -> int:
        return self.storage_size - self.used_storage_size

    @cached_property
    def hub(self) -> TelegramBotsHub | None:
        return TelegramBotsHub.objects.get_telegram_bot_hub(self.id)

    @property
    def is_enabled(self) -> bool:
        return self.must_be_enabled and bool(self.hub)

    def start(self, save: bool = True) -> None:
        self.must_be_enabled = True
        self.is_loading = True

        if save:
            self.save(update_fields=['must_be_enabled', 'is_loading'])

        tasks.start_telegram_bot.delay(telegram_bot_id=self.id)

    def restart(self, save: bool = True) -> None:
        self.is_loading = True

        if save:
            self.save(update_fields=['is_loading'])

        tasks.restart_telegram_bot.delay(telegram_bot_id=self.id)

    def stop(self, save: bool = True) -> None:
        self.must_be_enabled = False
        self.is_loading = True

        if save:
            self.save(update_fields=['must_be_enabled', 'is_loading'])

        tasks.stop_telegram_bot.delay(telegram_bot_id=self.id)

    def update_username(self) -> None:
        if settings.TEST:
            self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
            return

        response: Response = requests.get(
            f'https://api.telegram.org/bot{self.api_token}/getMe'
        )

        if not response.ok:
            return

        with suppress(KeyError):
            self.username = response.json()['result']['username']

    @classmethod
    def from_db(
        cls, db: str | None, field_names: Collection[str], values: Collection[Any]
    ) -> 'TelegramBot':
        telegram_bot: TelegramBot = super().from_db(db, field_names, values)
        telegram_bot._loaded_values = dict(
            zip(
                field_names,
                (value for value in values if value is not models.DEFERRED),  # type: ignore [attr-defined]
                strict=False,
            )
        )

        return telegram_bot

    def save(
        self,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if not settings.TEST and (
            self._state.adding or self.api_token != self._loaded_values['api_token']
        ):
            self.update_username()

            if not self._state.adding and self.is_enabled:
                self.restart(save=False)
                should_update_fields: list[str] = ['must_be_enabled', 'is_loading']
                update_fields = (
                    (list(update_fields) + should_update_fields)
                    if update_fields
                    else should_update_fields
                )

        super().save(force_insert, force_update, using, update_fields)

    def delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        if not settings.TEST and not self._state.adding and self.is_enabled:
            self.stop(save=False)

        return super().delete(using, keep_parents)

    def __str__(self) -> str:
        return f'@{self.username}'
