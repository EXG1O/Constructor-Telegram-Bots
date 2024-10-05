from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class TokenType(TextChoices):
	REFRESH = 'refresh', _('Токен обновления')
	ACCESS = 'access', _('Токен разрешения')
