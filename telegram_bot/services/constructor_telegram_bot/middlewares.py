from aiogram import BaseMiddleware
from aiogram.types import (
	Update,
	User as AiogramUser,
)

from user.models import User as DjangoUser

from ..typing import Handler

from typing import Any


class CreateDjangoUserMiddleware(BaseMiddleware):
	async def __call__(self, handler: Handler, event: Update, data: dict[str, Any]) -> Any:
		event_from_user: AiogramUser = data['event_from_user']

		await DjangoUser.objects.aget_or_create(
			telegram_id=event_from_user.id,
			defaults={'first_name': event_from_user.first_name},
		)

		return await handler(event, data)
