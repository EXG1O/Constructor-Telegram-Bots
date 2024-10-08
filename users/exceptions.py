from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException

from jwt import InvalidTokenError


class InvalidTokenTypeError(InvalidTokenError):
	pass


class InvalidTokenSubjectError(InvalidTokenError):
	pass


class InvalidTokenRefreshJTIError(InvalidTokenError):
	pass


class TelegramAuthDataOutdatedError(APIException):
	status_code = status.HTTP_400_BAD_REQUEST
	default_detail = _('Данные аутентификации через Telegram устарели.')
	default_code = 'tg_auth_data_outdated'


class FakeTelegramDataError(APIException):
	status_code = status.HTTP_400_BAD_REQUEST
	default_detail = _('Эти данные не от Telegram, потому-что они подделанные.')
	default_code = 'fake_tg_data'


class TokenBlacklistedError(APIException):
	status_code = status.HTTP_403_FORBIDDEN
	default_detail = _('Токен в чёрном списке.')
	default_code = 'token_blacklisted'


class UserInactiveOrDeletedError(APIException):
	status_code = status.HTTP_403_FORBIDDEN
	default_detail = _('Пользователь неактивен или удалён.')
	default_code = 'user_inactive_or_deleted'
