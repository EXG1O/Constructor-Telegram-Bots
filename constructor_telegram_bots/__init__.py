from constructor_telegram_bots.celery import celery_app
import django_stubs_ext

django_stubs_ext.monkeypatch()

__all__ = ('celery_app',)