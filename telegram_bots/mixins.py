from django.shortcuts import get_object_or_404

from .models import TelegramBot

from typing import Any


class TelegramBotMixin:
	_telegram_bot: TelegramBot | None = None

	@property
	def telegram_bot(self) -> TelegramBot:
		if self._telegram_bot is None:
			self._telegram_bot = get_object_or_404(
				self.request.user.telegram_bots,  # type: ignore [attr-defined]
				id=self.kwargs['telegram_bot_id'],  # type: ignore [attr-defined]
			)

		return self._telegram_bot

	def get_serializer_context(self) -> dict[str, Any]:
		context: dict[str, Any] = super().get_serializer_context()  # type: ignore [misc]
		context.update({'telegram_bot': self.telegram_bot})

		return context
