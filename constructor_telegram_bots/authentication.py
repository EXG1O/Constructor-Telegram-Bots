from django.utils.translation import gettext as _

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from users.models import User


class CookiesTokenAuthentication(TokenAuthentication):
	"""
	Simple token based authentication that supports authentication via cookies.

	Clients can authenticate by passing the token key either in the `Authorization`
	HTTP header or by storing the token in a cookie named `auth-token`.

	Authorization header example:
		Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

	Cookie example:
		auth-token=401f7ac837da42b97f613d789819ff93537bee6a
	"""

	def get_token(self, key: str) -> Token:
		return Token.objects.select_related('user').get(key=key)

	def authenticate(self, request: Request) -> tuple[User, Token] | None:
		auth_token: str | None = request.COOKIES.get('auth-token')

		if auth_token:
			try:
				token: Token = self.get_token(auth_token)

				return self.authenticate_credentials(token)
			except Token.DoesNotExist:
				pass

		return super().authenticate(request)

	def authenticate_credentials(self, token: Token | str) -> tuple[User, Token]:
		if isinstance(token, str):
			try:
				token = self.get_token(token)
			except Token.DoesNotExist:
				raise AuthenticationFailed(_('Неверный токен.'))

		if not token.user.is_active:
			raise AuthenticationFailed(_('Пользователь неактивен или удалён.'))

		return (token.user, token)
