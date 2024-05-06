from django.apps import apps

from celery import shared_task


@shared_task
def start_telegram_bot(telegram_bot_id: int) -> None:
	TelegramBot = apps.get_model('telegram_bots.TelegramBot')  # noqa: N806
	TelegramBotsHub = apps.get_model('telegram_bots_hub.TelegramBotsHub')  # noqa: N806

	telegram_bot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bot.is_loading = True
	telegram_bot.save()

	telegram_bots_hub = TelegramBotsHub.objects.get_free()
	telegram_bots_hub.start_telegram_bot(telegram_bot)


@shared_task
def restart_telegram_bot(telegram_bot_id: int) -> None:
	TelegramBot = apps.get_model('telegram_bots.TelegramBot')  # noqa: N806
	TelegramBotsHub = apps.get_model('telegram_bots_hub.TelegramBotsHub')  # noqa: N806

	telegram_bot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bots_hub = TelegramBotsHub.objects.get_telegram_bot_hub(id=telegram_bot.id)

	if telegram_bots_hub:
		telegram_bot.is_loading = True
		telegram_bot.save()

		telegram_bots_hub.restart_telegram_bot(telegram_bot)
	else:
		telegram_bot.is_enabled = False
		telegram_bot.is_loading = False
		telegram_bot.save()


@shared_task
def stop_telegram_bot(telegram_bot_id: int) -> None:
	TelegramBot = apps.get_model('telegram_bots.TelegramBot')  # noqa: N806
	TelegramBotsHub = apps.get_model('telegram_bots_hub.TelegramBotsHub')  # noqa: N806

	telegram_bot = TelegramBot.objects.get(id=telegram_bot_id)
	telegram_bots_hub = TelegramBotsHub.objects.get_telegram_bot_hub(id=telegram_bot.id)

	if telegram_bots_hub:
		telegram_bot.is_loading = True
		telegram_bot.save()

		telegram_bots_hub.stop_telegram_bot(telegram_bot)
	else:
		telegram_bot.is_enabled = False
		telegram_bot.is_loading = False
		telegram_bot.save()


@shared_task
def start_telegram_bots() -> None:
	TelegramBot = apps.get_model('telegram_bots.TelegramBot')  # noqa: N806
	TelegramBotsHub = apps.get_model('telegram_bots_hub.TelegramBotsHub')  # noqa: N806

	for telegram_bot in TelegramBot.objects.filter(is_enabled=True):
		telegram_bots_hub = TelegramBotsHub.objects.get_telegram_bot_hub(
			id=telegram_bot.id
		)

		if not telegram_bots_hub:
			telegram_bot.start()
