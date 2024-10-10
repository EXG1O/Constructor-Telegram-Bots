from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

from .exceptions import (
	FakeTelegramDataError,
	TelegramAuthDataOutdatedError,
	UserInactiveOrDeletedError,
)
from .models import User

from typing import Any, Literal, overload
import hashlib
import hmac
import time


class TelegramBackend(ModelBackend):
	@overload  # type: ignore [override]
	def authenticate(
		self,
		request: HttpRequest,
		hash: str,
		raise_exception: Literal[False],
		**data: Any,
	) -> User | None: ...

	@overload
	def authenticate(
		self,
		request: HttpRequest,
		hash: str,
		raise_exception: Literal[True],
		**data: Any,
	) -> User: ...

	def authenticate(
		self,
		request: HttpRequest,
		hash: str,
		raise_exception: bool = False,
		**data: Any,
	) -> User | None:
		telegram_id: int = data['id']
		first_name: str = data['first_name']

		if settings.ENABLE_TELEGRAM_AUTH:
			try:
				self._validate_auth_date(int(data['auth_date']))
				self._validate_auth_data(data, hash)
			except (TelegramAuthDataOutdatedError, FakeTelegramDataError) as error:
				if raise_exception:
					raise error

				return None

		last_name: str | None = data.get('last_name')

		user, created = User.objects.get_or_create(
			telegram_id=telegram_id,
			defaults={'first_name': first_name, 'last_name': last_name},
		)

		if not self.user_can_authenticate(user):
			if raise_exception:
				raise UserInactiveOrDeletedError()

			return None

		if not created:
			user.first_name = first_name
			user.last_name = last_name
			user.save(update_fields=['first_name', 'last_name'])

		return user

	def _validate_auth_date(self, auth_unix_date: int) -> None:
		if int(time.time()) - auth_unix_date > 86400:
			raise TelegramAuthDataOutdatedError()

	def _validate_auth_data(self, data: dict[str, Any], hash: str) -> None:
		secret_key: bytes = hashlib.sha256(
			settings.TELEGRAM_BOT_TOKEN.encode()
		).digest()
		data_check_string: str = '\n'.join(
			[f'{key}={data[key]}' for key in sorted(data.keys())]
		)
		result_hash: str = hmac.new(
			secret_key, data_check_string.encode(), hashlib.sha256
		).hexdigest()

		if result_hash != hash:
			raise FakeTelegramDataError()
