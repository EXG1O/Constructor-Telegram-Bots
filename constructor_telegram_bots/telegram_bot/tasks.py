from celery import shared_task

from django.conf import settings

from aiogram.exceptions import (
	TelegramNetworkError,
	TelegramUnauthorizedError,
	TelegramServerError,
	RestartingTelegram,
)

from .models import TelegramBot
from .services.constructor_telegram_bot.telegram_bot import ConstructorTelegramBot
from .services.user_telegram_bot.telegram_bot import UserTelegramBot

from threading import Thread


def start_telegram_bot_(aiogram_telegram_bot: ConstructorTelegramBot | UserTelegramBot) -> None:
	try:
		aiogram_telegram_bot.loop.run_until_complete(aiogram_telegram_bot.start())
	except (TelegramNetworkError, TelegramServerError, RestartingTelegram):
		start_telegram_bot_(aiogram_telegram_bot)
	except TelegramUnauthorizedError:
		aiogram_telegram_bot.django_telegram_bot.delete()

@shared_task
def start_telegram_bot(telegram_bot_id: int) -> None:
	django_telegram_bot: TelegramBot = TelegramBot.objects.get(id=telegram_bot_id)
	django_telegram_bot.is_running = True
	django_telegram_bot.is_stopped = False
	django_telegram_bot.save()

	Thread(
		target=start_telegram_bot_,
		args=(UserTelegramBot(django_telegram_bot),),
		daemon=True,
	).start()

@shared_task
def start_all_telegram_bots() -> None:
	Thread(
		target=start_telegram_bot_,
		args=(ConstructorTelegramBot(settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN),),
		daemon=True,
	).start()

	for django_telegram_bot in TelegramBot.objects.all():
		if django_telegram_bot.is_running:
			Thread(
				target=start_telegram_bot_,
				args=(UserTelegramBot(django_telegram_bot),),
				daemon=True,
			).start()
