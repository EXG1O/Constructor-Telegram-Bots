from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from .models import TelegramBot

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
