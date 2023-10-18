from django.contrib import admin, messages
from django.utils.html import format_html
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import TelegramBot, TelegramBotUser
from .tasks import start_telegram_bot as celery_start_telegram_bot

import sys


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
	search_fields = ('username',)
	date_hierarchy = 'added_date'
	list_filter = ('is_running', 'added_date')

	actions = ('start_telegram_bot_action', 'stop_telegram_bot_action')

	list_display = ('id', 'owner', 'username_', 'is_private', 'is_running', 'commands_count', 'users_count', 'added_date')
	fields = ('id', 'owner', 'username_', 'api_token', 'is_private', 'is_running', 'commands_count', 'users_count', 'added_date')

	@admin.display(description='@username', ordering='username')
	def username_(self, telegram_bot: TelegramBot) -> str:
		return format_html(f'<a href="tg://resolve?domain={telegram_bot.username}" style="font-weight: 600;" target="_blank">@{telegram_bot.username}</a>')

	@admin.display(description=_('Команд'))
	def commands_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.commands.count()

	@admin.display(description=_('Активаций'))
	def users_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.users.count()

	@admin.action(description=_('Включить Telegram бота'))
	def start_telegram_bot_action(self, request: HttpRequest, telegram_bots: list[TelegramBot]) -> None:
		for telegram_bot in telegram_bots:
			if not telegram_bot.is_running and telegram_bot.is_stopped:
				if sys.platform == 'win32':
					celery_start_telegram_bot(telegram_bot_id=telegram_bot.id)
				else:
					celery_start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

				messages.success(request, f"@{telegram_bot.username} {_('Telegram бот успешно включен.')}")
			else:
				messages.error(request, f"@{telegram_bot.username} {_('Telegram бот уже включен!')}")

	@admin.action(description=_('Выключить Telegram бота'))
	def stop_telegram_bot_action(self, request: HttpRequest, telegram_bots: list[TelegramBot]) -> None:
		for telegram_bot in telegram_bots:
			if telegram_bot.is_running and not telegram_bot.is_stopped:
				telegram_bot.stop()

				messages.success(request, f"@{telegram_bot.username} {_('Telegram бот успешно выключен.')}")
			else:
				messages.error(request, f"@{telegram_bot.username} {_('Telegram бот уже выключен!')}")

	def has_add_permission(self, *args, **kwargs) -> bool:
		return False

	def has_change_permission(self, *args, **kwargs) -> bool:
		return False

@admin.register(TelegramBotUser)
class TelegramBotUserAdmin(admin.ModelAdmin):
	search_fields = ('user_id', 'full_name')
	date_hierarchy = 'activated_date'
	list_filter = ('activated_date',)

	list_display = ('id', 'telegram_bot', 'user_id', 'full_name', 'is_allowed', 'activated_date')
	fields = ('id', 'telegram_bot', 'user_id', 'full_name', 'is_allowed', 'activated_date')

	def has_add_permission(self, *args, **kwargs) -> bool:
		return False

	def has_change_permission(self, *args, **kwargs) -> bool:
		return False
