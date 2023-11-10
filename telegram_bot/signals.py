from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import TelegramBot, TelegramBotCommand
from .services import database_telegram_bot

from typing import Any


@receiver(post_save, sender=TelegramBot)
def post_save_telegram_bot_signal_handler(instance: TelegramBot, created: bool, **kwargs: Any) -> None:
	if created:
		instance.update_username()

@receiver(post_delete, sender=TelegramBot)
def post_delete_telegram_bot_signal_handler(instance: TelegramBot, **kwargs: Any) -> None:
	database_telegram_bot.delete_collection(instance)

@receiver(post_delete, sender=TelegramBotCommand)
def post_delete_telegram_bot_command_signal_handler(instance: TelegramBotCommand, **kwargs: Any) -> None:
	instance.image.delete(save=False)
