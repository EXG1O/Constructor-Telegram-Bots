from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from jwt import PyJWTError

from .exceptions import TokenBlacklistedError, UserInactiveOrDeletedError
from .models import User
from .tokens import AccessToken
from .utils import get_access_token


class JWTCookieAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[User, AccessToken] | None:
        try:
            access_token: AccessToken = get_access_token(request)
        except PyJWTError:
            return None

        if access_token.is_blacklisted:
            raise TokenBlacklistedError()

        user: User = access_token.user

        if not user.is_active:
            raise UserInactiveOrDeletedError()

        return user, access_token
