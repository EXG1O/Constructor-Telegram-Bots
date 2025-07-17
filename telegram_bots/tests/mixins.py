from users.models import User
from users.tokens import AccessToken, RefreshToken

from ..models import TelegramBot

from typing import TYPE_CHECKING


class UserMixin:
    def setUp(self) -> None:
        super().setUp()  # type: ignore [misc]
        self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
        self.user_refresh_token: RefreshToken = RefreshToken.for_user(self.user)
        self.user_access_token: AccessToken = self.user_refresh_token.access_token


class TelegramBotMixin:
    if TYPE_CHECKING:
        user: User

    def setUp(self) -> None:
        super().setUp()  # type: ignore [misc]
        self.telegram_bot: TelegramBot = self.user.telegram_bots.create(api_token='Hi!')
