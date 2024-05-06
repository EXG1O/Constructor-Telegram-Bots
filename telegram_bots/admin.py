from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from utils.html import format_html_link

from .models import TelegramBot, User

from typing import Any, Literal


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin[TelegramBot]):
	search_fields = ['username']
	date_hierarchy = 'added_date'
	list_filter = ['is_enabled', 'added_date']
	list_display = [
		'id',
		'owner',
		'username_display',
		'storage_size_display',
		'used_storage_size_display',
		'remaining_storage_size_display',
		'commands_count',
		'users_count',
		'is_private',
		'is_enabled',
		'added_date',
	]
	fields = [
		'id',
		'owner',
		'username_display',
		'api_token',
		'storage_size_display',
		'used_storage_size_display',
		'remaining_storage_size_display',
		'commands_count',
		'users_count',
		'is_private',
		'is_enabled',
		'added_date',
	]

	def get_queryset(self, request: HttpRequest) -> QuerySet[TelegramBot]:
		return (
			super()
			.get_queryset(request)
			.annotate(commands_count=Count('commands'), users_count=Count('users'))
		)

	@admin.display(description='@username', ordering='username')
	def username_display(self, telegram_bot: TelegramBot) -> str:
		return format_html_link(
			f'tg://resolve?domain={telegram_bot.username}', f'@{telegram_bot.username}'
		)

	@admin.display(description=_('Размер хранилища'))
	def storage_size_display(self, telegram_bot: TelegramBot) -> str:
		return f'{(telegram_bot.storage_size / 1024 ** 2):.2f}MB'

	@admin.display(description=_('Используемый размер хранилища'))
	def used_storage_size_display(self, telegram_bot: TelegramBot) -> str:
		return f'{(telegram_bot.used_storage_size / 1024 ** 2):.2f}MB'

	@admin.display(description=_('Оставшийся размер хранилища'))
	def remaining_storage_size_display(self, telegram_bot: TelegramBot) -> str:
		return f'{(telegram_bot.remaining_storage_size / 1024 ** 2):.2f}MB'

	@admin.display(description=_('Команд'), ordering='commands_count')
	def commands_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.commands.count()

	@admin.display(description=_('Пользователей'), ordering='users_count')
	def users_count(self, telegram_bot: TelegramBot) -> int:
		return telegram_bot.users.count()

	def has_add_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False

	def has_change_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
	search_fields = ['telegram_id', 'full_name']
	date_hierarchy = 'activated_date'
	list_filter = ['is_allowed', 'is_blocked', 'last_activity_date', 'activated_date']
	list_display = [
		'id',
		'telegram_bot',
		'telegram_id',
		'full_name',
		'is_allowed',
		'is_blocked',
		'last_activity_date',
		'activated_date',
	]
	fields = [
		'id',
		'telegram_bot',
		'telegram_id',
		'full_name',
		'is_allowed',
		'is_blocked',
		'last_activity_date',
		'activated_date',
	]

	def has_add_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False

	def has_change_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False
