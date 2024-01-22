from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from utils.admin import format_html_url

from .models import TelegramBot, TelegramBotUser
from .tasks import start_telegram_bot

from typing import Any


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
		return format_html_url(f'tg://resolve?domain={telegram_bot.username}', f'@{telegram_bot.username}')

	@admin.display(description=_('Команд'))
	def commands_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.commands.count()

	@admin.display(description=_('Активаций'))
	def users_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.users.count()

	@admin.action(description=_('Включить Telegram бота'))
	def start_telegram_bot_action(self, request: HttpRequest, telegram_bots: 'QuerySet[TelegramBot]') -> None:
		for telegram_bot in telegram_bots:
			if not telegram_bot.is_running and telegram_bot.is_stopped:
				start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

				messages.success(request, f"@{telegram_bot.username} {_('Telegram бот успешно включен.')}")
			else:
				messages.error(request, f"@{telegram_bot.username} {_('Telegram бот уже включен!')}")

	@admin.action(description=_('Выключить Telegram бота'))
	def stop_telegram_bot_action(self, request: HttpRequest, telegram_bots: 'QuerySet[TelegramBot]') -> None:
		for telegram_bot in telegram_bots:
			if telegram_bot.is_running and not telegram_bot.is_stopped:
				telegram_bot.stop()

				messages.success(request, f"@{telegram_bot.username} {_('Telegram бот успешно выключен.')}")
			else:
				messages.error(request, f"@{telegram_bot.username} {_('Telegram бот уже выключен!')}")

	def has_add_permission(self, *args: Any, **kwargs: Any) -> bool:
		return False

	def has_change_permission(self, *args: Any, **kwargs: Any) -> bool:
		return False

@admin.register(TelegramBotUser)
class TelegramBotUserAdmin(admin.ModelAdmin):
	search_fields = ('telegram_id', 'full_name')
	date_hierarchy = 'activated_date'
	list_filter = ('is_allowed', 'is_blocked', 'last_activity_date', 'activated_date')
	list_display = ('id', 'telegram_bot', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked', 'last_activity_date', 'activated_date')

	fields = ('id', 'telegram_bot', 'telegram_id', 'full_name', 'is_allowed', 'is_blocked', 'last_activity_date', 'activated_date')

	def has_add_permission(self, *args: Any, **kwargs: Any) -> bool:
		return False

	def has_change_permission(self, *args: Any, **kwargs: Any) -> bool:
		return False