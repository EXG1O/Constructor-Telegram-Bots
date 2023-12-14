from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from constructor_telegram_bots.environment import (
	update_plugin as env_update_plugin,
	delete_plugin as env_delete_plugin,
)

from .models import Plugin

from typing import Any


@receiver(post_save, sender=Plugin)
def post_save_plugin_signal_handler(instance: Plugin, **kwargs: Any) -> None:
	if instance.is_checked:
		env_update_plugin(plugin=instance)

@receiver(post_delete, sender=Plugin)
def post_delete_plugin_signal_handler(instance: Plugin, **kwargs: Any) -> None:
	if instance.is_checked:
		env_delete_plugin(plugin=instance)