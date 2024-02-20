from django.urls import path

from .views import (
	TelegramBotAPIView,
	TelegramBotCommandsAPIView,
	TelegramBotCommandAPIView,
	TelegramBotVariablesAPIView,
	TelegramBotUsersAPIView,
)


app_name = 'hub'
urlpatterns = [
	path('', TelegramBotAPIView.as_view(), name='detail'),
	path('commands/', TelegramBotCommandsAPIView.as_view(), name='commands'),
	path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandAPIView.as_view(), name='command'),
	path('variables/', TelegramBotVariablesAPIView.as_view(), name='variables'),
	path('users/', TelegramBotUsersAPIView.as_view(), name='users'),
]