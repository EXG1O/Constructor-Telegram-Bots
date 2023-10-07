from celery import shared_task

from django.conf import settings

from .models import TelegramBot
from .services.constructor_telegram_bot.telegram_bot import ConstructorTelegramBot
from .services.user_telegram_bot.telegram_bot import UserTelegramBot

from threading import Thread
from typing import Union


def start_telegram_bot_(telegram_bot: Union[ConstructorTelegramBot, UserTelegramBot]) -> None:
	telegram_bot.loop.run_until_complete(telegram_bot.start())

@shared_task
def start_telegram_bot(telegram_bot_id: int) -> None:
	telegram_bot: TelegramBot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bot.is_running = True
	telegram_bot.is_stopped = False
	telegram_bot.save()

	Thread(
		target=start_telegram_bot_,
		args=(UserTelegramBot(django_telegram_bot=telegram_bot),),
		daemon=True
	).start()

@shared_task
def start_all_telegram_bots() -> None:
	Thread(
		target=start_telegram_bot_,
		args=(ConstructorTelegramBot(api_token=settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN),),
		daemon=True
	).start()

	for telegram_bot in TelegramBot.objects.all():
		if telegram_bot.is_running:
			Thread(
				target=start_telegram_bot_,
				args=(UserTelegramBot(django_telegram_bot=telegram_bot),),
				daemon=True
			).start()

@shared_task
def stop_telegram_bot(telegram_bot_id: int) -> None:
	telegram_bot: TelegramBot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bot.is_running = False
	telegram_bot.save()
