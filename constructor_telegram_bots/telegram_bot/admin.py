from django.contrib import admin, messages

from django.utils.translation import gettext_lazy as _

from django.core.handlers.wsgi import WSGIRequest

from django.utils import html

from telegram_bot.models import TelegramBot

from telegram_bots.tasks import start_telegram_bot as start_telegram_bot_
from telegram_bots.tasks import stop_telegram_bot as stop_telegram_bot_


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
	date_hierarchy = '_date_added'
	list_filter = ('is_running',)

	list_display = (
		'owner',
		'show_telegram_bot_username',
		'is_private',
		'is_running',
		'show_telegram_bot_commands_count',
		'show_telegram_bot_users_count',
		'_date_added',
	)
	list_display_links = None

	@admin.display(description='@username')
	def show_telegram_bot_username(self, telegram_bot: TelegramBot) -> int:
		return html.format_html(f'<a href="tg://resolve?domain={telegram_bot.username}">@{telegram_bot.username}</a>')

	@admin.display(description=_('Количество команд'))
	def show_telegram_bot_commands_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.commands.count()
	
	@admin.display(description=_('Количество активаций'))
	def show_telegram_bot_users_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.users.count()

	@admin.action(permissions=['change'], description=_('Включить Telegram бота'))
	def start_telegram_bot_button(self, request: WSGIRequest, telegram_bots: list[TelegramBot]) -> None:
		for telegram_bot in telegram_bots:
			if telegram_bot.is_stopped:
				start_telegram_bot_.delay(telegram_bot_id=telegram_bot.id)

				message = _('Telegram бот успешно включен.')

				self.log_change(
					request=request,
					obj=telegram_bot,
					message=message
				)

				messages.success(request, f'@{telegram_bot.name} {message}')
			else:
				messages.error(request, f'@{telegram_bot.name} {_("Telegram бот уже включен!")}')

	@admin.action(permissions=['change'], description=_('Выключить Telegram бота'))
	def stop_telegram_bot_button(self, request: WSGIRequest, telegram_bots: list[TelegramBot]) -> None:
		for telegram_bot in telegram_bots:
			if telegram_bot.is_running:
				stop_telegram_bot_.delay(telegram_bot_id=telegram_bot.id)

				message = _('Telegram бот успешно выключен.')

				self.log_change(
					request=request,
					obj=telegram_bot,
					message=message
				)

				messages.success(request, f'@{telegram_bot.name} {message}')
			else:
				messages.error(request, f'@{telegram_bot.name} {_("Telegram бот уже выключен!")}')

	actions = [
		start_telegram_bot_button,
		stop_telegram_bot_button,
	]
	
	def has_add_permission(self, request: WSGIRequest, obj: None=None) -> bool:
		return False

	def has_change_permission(self, request: WSGIRequest, obj: None=None) -> bool:
		return request.user.has_perm('change_telegrambot')