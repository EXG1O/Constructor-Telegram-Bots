from django.utils.functional import cached_property

from ..models import TelegramBot

from typing import TYPE_CHECKING, Any


class TelegramBotMixin:
    if TYPE_CHECKING:
        context: dict[str, Any]

    @cached_property
    def telegram_bot(self) -> TelegramBot:
        telegram_bot: Any = self.context.get('telegram_bot')

        if not isinstance(telegram_bot, TelegramBot):
            raise TypeError(
                'You not passed a TelegramBot instance as telegram_bot to the '
                'serializer context.'
            )

        return telegram_bot
