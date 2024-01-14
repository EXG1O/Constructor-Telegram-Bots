from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import (
	TelegramBot,
	TelegramBotCommandImage,
	TelegramBotCommandFile,
)

from typing import Any


@receiver(post_save, sender=TelegramBot)
def post_save_telegram_bot_signal_handler(instance: TelegramBot, created: bool, **kwargs: Any) -> None:
	if created:
		instance.update_username()

@receiver(post_delete, sender=TelegramBotCommandImage)
def post_delete_telegram_bot_command_image_signal_handler(instance: TelegramBotCommandImage, **kwargs: Any) -> None:
	instance.image.delete(save=False)

@receiver(post_delete, sender=TelegramBotCommandFile)
def post_delete_telegram_bot_command_file_signal_handler(instance: TelegramBotCommandFile, **kwargs: Any) -> None:
	instance.file.delete(save=False)