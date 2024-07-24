from django.contrib import admin

from .models import TelegramBotsHub


@admin.register(TelegramBotsHub)
class TelegramBotsHubAdmin(admin.ModelAdmin[TelegramBotsHub]):
	search_fields = ['url']
	list_display = ['url']
	fields = ['url', 'service_token', 'microservice_token']
