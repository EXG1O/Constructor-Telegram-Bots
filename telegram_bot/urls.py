from django.urls import path, include

from .views import (
	TelegramBotsView,
	TelegramBotView,
	start_or_stop_telegram_bot,
	TelegramBotCommandsView,
	TelegramBotCommandView,
	TelegramBotCommandsDiagramAPIView,
	TelegramBotCommandDiagramAPIView,
	TelegramBotUsersView,
	TelegramBotUserView,
	TelegramBotAllowedUserView,
)


app_name = 'telegram_bot'
urlpatterns = [
	path('', TelegramBotsView.as_view(), name='index'),
	path('<int:telegram_bot_id>/', include([
		path('', TelegramBotView.as_view(), name='index'),
		path('start-or-stop/', start_or_stop_telegram_bot, name='start-or-stop-telegram-bot'),

		path('commands/', TelegramBotCommandsView.as_view(), name='commands'),
		path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandView.as_view(), name='command'),

		path('diagram/', include([
			path('commands/', TelegramBotCommandsDiagramAPIView.as_view(), name='commands'),
			path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandDiagramAPIView.as_view(), name='command'),
		]), name='diagram'),

		path('users/', TelegramBotUsersView.as_view(), name='users'),
		path('users/<int:telegram_bot_user_id>/', include([
			path('', TelegramBotUserView.as_view(), name='user'),
			path('allowed-user/', TelegramBotAllowedUserView.as_view(), name='allowed-user'),
		])),
	]), name='telegram-bot'),
]