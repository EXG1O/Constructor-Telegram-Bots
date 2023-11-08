from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UpdatesConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'updates'
	verbose_name = _('Обновления')
