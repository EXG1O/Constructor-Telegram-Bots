from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from ..models import TelegramBot

from typing import Any


class TelegramBotMixin:
	@cached_property
	def telegram_bot(self) -> TelegramBot:
		return get_object_or_404(
			self.request.user.telegram_bots,  # type: ignore [attr-defined]
			id=self.kwargs['telegram_bot_id'],  # type: ignore [attr-defined]
		)

	def get_serializer_context(self) -> dict[str, Any]:
		context: dict[str, Any] = super().get_serializer_context()  # type: ignore [misc]
		context.update({'telegram_bot': self.telegram_bot})

		return context


class TelegramBotContextMixin:
	@cached_property
	def telegram_bot(self) -> TelegramBot:
		telegram_bot: Any = self.context.get('telegram_bot')  # type: ignore [attr-defined]

		if not isinstance(telegram_bot, TelegramBot):
			raise TypeError(
				'You not passed a TelegramBot instance as '
				'telegram_bot to the serializer context.'
			)

		return telegram_bot
