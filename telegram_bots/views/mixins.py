from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from rest_framework.exceptions import PermissionDenied

from users.models import User

from ..models import TelegramBot

from typing import TYPE_CHECKING, Any


class TelegramBotMixin:
    if TYPE_CHECKING:
        request: Any
        kwargs: dict[str, Any]

    @cached_property
    def telegram_bot(self) -> TelegramBot:
        if not isinstance(self.request.user, User):
            raise PermissionDenied()

        return get_object_or_404(
            self.request.user.telegram_bots,
            id=self.kwargs['telegram_bot_id'],
        )

    def get_serializer_context(self) -> dict[str, Any]:
        context: dict[str, Any] = super().get_serializer_context()  # type: ignore [misc]
        context.update({'telegram_bot': self.telegram_bot})

        return context
