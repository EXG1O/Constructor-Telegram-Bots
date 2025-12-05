from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpRequest
from django.utils.translation import gettext as _

from rest_framework.exceptions import APIException

from jwt import PyJWTError

from .enums import TokenType
from .jwt.tokens import AccessToken, RefreshToken
from .models import BlacklistedToken, Token, User

from typing import TypeVar

JWT = TypeVar('JWT', RefreshToken, AccessToken)


def authenticate_token(
    raw_token: str, token_cls: type[JWT], exception_cls: type[APIException]
) -> tuple[User, JWT]:
    try:
        token = token_cls(token=raw_token)
    except PyJWTError as error:
        raise exception_cls(_('Недействительный токен.')) from error

    if token.is_blacklisted:
        raise exception_cls(_('Токен в чёрном списке.'))

    user: User | None = token.user

    if not user or not user.is_active:
        raise exception_cls(_('Пользователь неактивен или удалён.'))

    return user, token


def login(request: HttpRequest, user: User) -> RefreshToken:
    auth_login(request, user)
    return RefreshToken.for_user(user)


def logout(request: HttpRequest, jwt_token: RefreshToken | AccessToken) -> None:
    auth_logout(request)

    if isinstance(jwt_token, RefreshToken):
        jwt_token.to_blacklist()
        return

    token: Token = Token.objects.get(
        jti=jwt_token.payload.refresh_jti, type=TokenType.REFRESH
    )
    BlacklistedToken.objects.create(token=token)


def logout_all(request: HttpRequest, user: User) -> None:
    auth_logout(request)
    BlacklistedToken.objects.bulk_create(
        BlacklistedToken(token=token)
        for token in Token.objects.filter(user=user).exclude(blacklisted__isnull=False)
    )
