from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PrivacyPolicyConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'privacy_policy'
	verbose_name = _('Политика конфиденциальности')
