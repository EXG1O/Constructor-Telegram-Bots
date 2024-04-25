from rest_framework.authentication import TokenAuthentication
from rest_framework.request import Request
from rest_framework.authtoken.models import Token

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

	def authenticate(self, request: Request) -> tuple[User, str] | None:
		auth_token: str | None = request.COOKIES.get('auth-token')

		try:
			token: Token = Token.objects.get(key=auth_token)

			return self.authenticate_credentials(token.key)
		except Token.DoesNotExist:
			return super().authenticate(request)
