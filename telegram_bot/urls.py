from django.urls import path, include


app_name = 'telegram_bot'
urlpatterns = [
	path('telegram-bot-menu/<int:telegram_bot_id>/', include('telegram_bot.frontend.urls')),
	path('api/telegram-bots/', include('telegram_bot.api.urls')),
]
