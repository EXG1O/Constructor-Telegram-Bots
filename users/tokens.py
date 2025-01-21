from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property

import jwt

from .data import AccessTokenPayload, TokenPayload
from .enums import TokenType
from .exceptions import (
    InvalidTokenRefreshJTIError,
    InvalidTokenSubjectError,
    InvalidTokenTypeError,
)
from .models import BlacklistedToken, Token, User

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, tzinfo
from typing import Any, Generic, TypeVar, overload

PT = TypeVar('PT', bound=TokenPayload)


class BaseToken(ABC, Generic[PT]):
    @property
    @abstractmethod
    def _type(self) -> TokenType: ...

    @property
    @abstractmethod
    def lifetime(self) -> timedelta: ...

    @property
    @abstractmethod
    def payload_cls(self) -> type[PT]: ...

    require_claims: list[str] = ['jti', 'typ', 'sub', 'exp', 'iat']

    def __init__(self, token: str | None = None, **kwargs: Any) -> None:
        self.payload: PT = (
            self.decode(token) if token else self._create_payload(**kwargs)
        )

        tz: tzinfo = timezone.get_current_timezone()

        self.expiry_date: datetime = datetime.fromtimestamp(self.payload.exp, tz)
        self.created_date: datetime = datetime.fromtimestamp(self.payload.iat, tz)

    @abstractmethod
    def _create_payload(self, **kwargs: Any) -> PT: ...

    @cached_property
    def user(self) -> User:
        return User.objects.get(id=self.payload.sub)

    def create_token(self) -> Token:
        """
        The method creates a record to DB about the token.

        ONLY REQUIRED FOR REFRESH TOKENS, OPTIONAL FOR OTHER.
        """
        self.validate(self.payload.to_dict())

        return Token.objects.create(
            user_id=self.payload.sub,
            jti=self.payload.jti,
            type=self.payload.typ,
            expiry_date=self.expiry_date,
        )

    @cached_property
    def token(self) -> Token:
        try:
            return Token.objects.get(jti=self.payload.jti, type=self.payload.typ)
        except Token.DoesNotExist:
            return self.create_token()

    @property
    def is_blacklisted(self) -> bool:
        return BlacklistedToken.objects.filter(
            token__jti=self.payload.jti, token__type=self.payload.typ
        ).exists()

    def to_blacklist(self) -> BlacklistedToken:
        return BlacklistedToken.objects.get_or_create(token=self.token)[0]

    def _validate_type(self, payload: dict[str, Any]) -> None:
        if payload.get('typ') != self._type:
            raise InvalidTokenTypeError()

    def _validate_subject(self, payload: dict[str, Any]) -> None:
        subject: Any = payload.get('sub')

        if not isinstance(subject, str) or not subject.isdigit():
            raise InvalidTokenSubjectError()

    def validate(self, payload: dict[str, Any]) -> None:
        if 'typ' in self.require_claims:
            self._validate_type(payload)

        if 'sub' in self.require_claims:
            self._validate_subject(payload)

        jwt.api_jwt._jwt_global_obj._validate_claims(
            payload,
            options={
                'require': self.require_claims,
                'verify_nbf': 'nbf' in self.require_claims,
                'verify_aud': 'aud' in self.require_claims,
                'verify_iss': 'iss' in self.require_claims,
                'verify_exp': 'exp' in self.require_claims,
                'verify_iat': 'iat' in self.require_claims,
            },
        )

    def encode(self) -> str:
        payload: dict[str, Any] = self.payload.to_dict()

        self.validate(payload)

        return jwt.encode(payload, settings.SECRET_KEY)

    def decode(self, token: str) -> PT:
        payload: dict[str, Any] = jwt.decode(
            token, settings.SECRET_KEY, algorithms=['HS256']
        )
        self.validate(payload)

        return self.payload_cls(**payload)

    def __str__(self) -> str:
        return self.encode()


class RefreshToken(BaseToken[TokenPayload]):
    _type = TokenType.REFRESH
    lifetime = settings.JWT_REFRESH_TOKEN_LIFETIME
    payload_cls = TokenPayload

    @overload
    def __init__(self, *, token: str) -> None: ...

    @overload
    def __init__(self, *, user: User) -> None: ...

    def __init__(self, *, token: str | None = None, user: User | None = None) -> None:
        super().__init__(token, user=user)

    def _create_payload(self, user: User) -> TokenPayload:  # type: ignore [override]
        return TokenPayload.create(self, sub=str(user.id))

    @classmethod
    def for_user(cls, user: User) -> 'RefreshToken':
        token: RefreshToken = cls(user=user)
        token.create_token()

        return token

    @cached_property
    def access_token(self) -> 'AccessToken':
        return AccessToken(refresh_token=self)


class AccessToken(BaseToken[AccessTokenPayload]):
    _type = TokenType.ACCESS
    lifetime = settings.JWT_ACCESS_TOKEN_LIFETIME
    payload_cls = AccessTokenPayload
    require_claims = BaseToken.require_claims + ['refresh_jti']

    @overload
    def __init__(self, *, token: str) -> None: ...

    @overload
    def __init__(self, *, refresh_token: RefreshToken) -> None: ...

    def __init__(
        self, *, token: str | None = None, refresh_token: RefreshToken | None = None
    ) -> None:
        super().__init__(token, refresh_token=refresh_token)

    def _create_payload(self, refresh_token: RefreshToken) -> AccessTokenPayload:  # type: ignore [override]
        return AccessTokenPayload.create(self, refresh_token)

    @property
    def is_blacklisted(self) -> bool:
        return (
            BlacklistedToken.objects.filter(
                token__jti=self.payload.refresh_jti, token__type=TokenType.REFRESH
            ).exists()
            and super().is_blacklisted
        )

    def _validate_refresh_jti(self, payload: dict[str, Any]) -> None:
        refresh_jti: Any = payload.get('refresh_jti')

        if not isinstance(refresh_jti, str) or not refresh_jti:
            raise InvalidTokenRefreshJTIError()

    def validate(self, payload: dict[str, Any]) -> None:
        self._validate_refresh_jti(payload)
        super().validate(payload)
