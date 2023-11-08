from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TeamConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'team'
	verbose_name = _('Команда')
