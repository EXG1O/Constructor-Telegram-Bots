from django.utils.translation import gettext as _

from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import TelegramBotsHub


class TokenAuthentication(BaseTokenAuthentication):
	def authenticate_credentials(self, token: str) -> tuple[TelegramBotsHub, str]:
		try:
			telegram_bots_hub: TelegramBotsHub = TelegramBotsHub.objects.get(
				token=token
			)
		except TelegramBotsHub.DoesNotExist:
			raise AuthenticationFailed(_('Неверный токен!'))

		return telegram_bots_hub, token
