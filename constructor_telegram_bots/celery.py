from celery import Celery, signals

from typing import Any
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructor_telegram_bots.settings')

celery_app = Celery('constructor_telegram_bots')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(['user', 'telegram_bot'])


@signals.celeryd_after_setup.connect
def celery_after_setup(*args: Any, **kwargs: Any) -> None:
	from telegram_bots.tasks import start_telegram_bots

	start_telegram_bots.delay()
