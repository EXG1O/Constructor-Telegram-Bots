from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User

from typing import Any


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
	search_fields = ('telegram_id', 'first_name', 'last_name')
	date_hierarchy = 'joined_date'
	list_filter = ('is_staff', 'last_login', 'joined_date')
	list_display = ('id', 'telegram_id', 'first_name', 'last_name', 'telegram_bots_count', 'is_staff', 'last_login', 'joined_date')

	fields = ('id', 'telegram_id', 'first_name', 'last_name', 'telegram_bots_count', 'is_staff', 'groups', 'last_login', 'joined_date')
	readonly_fields = ('id', 'telegram_id', 'first_name', 'last_name', 'telegram_bots_count', 'last_login', 'joined_date')

	@admin.display(description=_('Количество Telegram ботов'))
	def telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()

	def has_add_permission(self, *args: Any, **kwargs: Any) -> bool:
		return False