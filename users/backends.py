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

		auth_unix_time: int = int(data['auth_date'])
		current_unix_time: int = int(time.time())

		if current_unix_time - auth_unix_time > 86400:
			if raise_exception:
				raise TelegramAuthDataOutdatedError()

			return None

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
			if raise_exception:
				raise FakeTelegramDataError()

			return None

		user, created = User.objects.get_or_create(
			telegram_id=telegram_id,
			defaults={'first_name': first_name, 'last_name': data.get('last_name')},
		)

		if not self.user_can_authenticate(user):
			if raise_exception:
				raise UserInactiveOrDeletedError()

			return None

		return user
