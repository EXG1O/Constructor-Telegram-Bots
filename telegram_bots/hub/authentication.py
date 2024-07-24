from django.utils.translation import gettext as _

from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import TelegramBotsHub


class TokenAuthentication(BaseTokenAuthentication):
	def authenticate_credentials(self, token: str) -> tuple[TelegramBotsHub, str]:
		try:
			hub: TelegramBotsHub = TelegramBotsHub.objects.get(service_token=token)
		except TelegramBotsHub.DoesNotExist:
			raise AuthenticationFailed(_('Недействительный токен.'))

		return hub, token
