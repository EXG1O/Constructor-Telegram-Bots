from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegramBotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bots'
    verbose_name = _('Telegram боты')
