from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpRequest, HttpResponse

from jwt.exceptions import InvalidTokenError

from .models import BlacklistedToken, Token, User
from .tokens import AccessToken, RefreshToken

from typing import Any


def get_refresh_token(request: HttpRequest) -> RefreshToken:
    raw_refresh_token: str | None = request.COOKIES.get(
        settings.JWT_REFRESH_TOKEN_COOKIE_NAME
    )

    if not raw_refresh_token:
        raise InvalidTokenError()

    return RefreshToken(token=raw_refresh_token)


def get_access_token(request: HttpRequest) -> AccessToken:
    raw_access_token: str | None = request.COOKIES.get(
        settings.JWT_ACCESS_TOKEN_COOKIE_NAME
    )

    if not raw_access_token:
        raise InvalidTokenError()

    return AccessToken(token=raw_access_token)


def add_jwt_tokens_to_cookies(
    response: HttpResponse, refresh_token: str, access_token: str
) -> None:
    options: dict[str, Any] = {
        'secure': settings.JWT_TOKEN_COOKIE_SECURE,
        'httponly': settings.JWT_TOKEN_COOKIE_HTTPONLY,
        'samesite': settings.JWT_TOKEN_COOKIE_SAMESITE,
    }

    response.set_cookie(
        settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
        refresh_token,
        max_age=settings.JWT_REFRESH_TOKEN_LIFETIME,
        **options,
    )
    response.set_cookie(
        settings.JWT_ACCESS_TOKEN_COOKIE_NAME,
        access_token,
        max_age=settings.JWT_ACCESS_TOKEN_LIFETIME,
        **options,
    )


def delete_jwt_tokens_from_cookies(response: HttpResponse) -> None:
    response.delete_cookie(settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
    response.delete_cookie(settings.JWT_ACCESS_TOKEN_COOKIE_NAME)


def login(request: HttpRequest, user: User) -> RefreshToken:
    auth_login(request, user)
    return RefreshToken.for_user(user)


def logout(request: HttpRequest, refresh_token: RefreshToken) -> None:
    auth_logout(request)
    refresh_token.to_blacklist()


def logout_all(request: HttpRequest, user: User, refresh_token: RefreshToken) -> None:
    logout(request, refresh_token)
    BlacklistedToken.objects.bulk_create(
        BlacklistedToken(token=token)
        for token in Token.objects.filter(user=user).exclude(blacklisted__isnull=False)
    )
