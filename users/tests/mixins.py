from ..jwt.tokens import AccessToken, RefreshToken
from ..models import User


class UserMixin:
    def setUp(self) -> None:
        super().setUp()  # type: ignore [misc]
        self.user: User = User.objects.create(
            telegram_id=123456789, first_name='exg1o', accepted_terms=True
        )
        self.user_refresh_token: RefreshToken = RefreshToken.for_user(self.user)
        self.user_access_token: AccessToken = self.user_refresh_token.access_token
