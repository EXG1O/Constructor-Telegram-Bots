from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TermsOfServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'terms_of_service'
    verbose_name = _('Условия использования сервиса')
