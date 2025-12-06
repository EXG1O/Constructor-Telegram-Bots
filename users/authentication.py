from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt.tokens import AccessToken
from .models import User
from .utils.auth import authenticate_token


class JWTAuthentication(TokenAuthentication):
    def authenticate_credentials(self, raw_token: str) -> tuple[User, AccessToken]:
        return authenticate_token(
            raw_token, token_cls=AccessToken, exception_cls=AuthenticationFailed
        )
