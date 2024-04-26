from django.contrib import admin

from .models import TelegramBotsHub

from typing import Any, Literal


@admin.register(TelegramBotsHub)
class TelegramBotsHubAdmin(admin.ModelAdmin[TelegramBotsHub]):
	search_fields = ('pid', 'port', 'token')
	list_display = ('pid', 'port', 'token')
	fields = ('pid', 'port', 'token')

	def has_add_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False

	def has_change_permission(self, *args: Any, **kwargs: Any) -> Literal[False]:
		return False
