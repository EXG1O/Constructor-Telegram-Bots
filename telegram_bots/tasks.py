from celery import shared_task

from .hub.utils import get_telegram_bots_hub_modal
from .utils import get_telegram_bot_modal

from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, Any, Concatenate, ParamSpec, TypeVar

if TYPE_CHECKING:
    from .hub.models import TelegramBotsHub
    from .models import TelegramBot
else:
    TelegramBot = Any
    TelegramBotsHub = Any


P = ParamSpec('P')
R = TypeVar('R')


def execute_task(func: Callable[Concatenate[TelegramBot, P], R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        telegram_bot_id = kwargs['telegram_bot_id']
        assert isinstance(telegram_bot_id, int)

        telegram_bot: TelegramBot = get_telegram_bot_modal().objects.get(
            id=telegram_bot_id
        )

        try:
            return func(telegram_bot, *args, **kwargs)
        finally:
            telegram_bot.is_loading = False
            telegram_bot.save(update_fields=['is_loading'])

    return wrapper


@shared_task
@execute_task
def start_telegram_bot(telegram_bot: TelegramBot, telegram_bot_id: int) -> None:
    hub: TelegramBotsHub | None = get_telegram_bots_hub_modal().objects.get_freest()

    if not hub:
        return

    hub.api.start_telegram_bot(telegram_bot.id, {'bot_token': telegram_bot.api_token})


@shared_task
@execute_task
def restart_telegram_bot(telegram_bot: TelegramBot, telegram_bot_id: int) -> None:
    if not telegram_bot.hub:
        return None

    telegram_bot.hub.api.restart_telegram_bot(telegram_bot.id)


@shared_task
@execute_task
def stop_telegram_bot(telegram_bot: TelegramBot, telegram_bot_id: int) -> None:
    if not telegram_bot.hub:
        return None

    telegram_bot.hub.api.stop_telegram_bot(telegram_bot.id)


@shared_task
def start_telegram_bots() -> None:
    for telegram_bot in get_telegram_bot_modal().objects.filter(must_be_enabled=True):
        if not telegram_bot.is_enabled:
            telegram_bot.start()
