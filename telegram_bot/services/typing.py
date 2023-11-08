from aiogram.types import TelegramObject

from typing import Callable, Awaitable, Any


Handler = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
