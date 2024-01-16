from django.utils.translation import gettext as _

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.authtoken.models import Token

from user.models import User


class CookiesTokenAuthentication(BaseAuthentication):
	def authenticate(self, request: Request) -> tuple[User, str] | None:
		auth_token: str | None  = request.COOKIES.get('auth-token')

		if not auth_token:
			return None

		try:
			token: Token = Token.objects.get(key=auth_token)
		except Token.DoesNotExist:
			raise AuthenticationFailed(_('Неверный токен.'))

		return (token.user, auth_token)