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


urlpatterns = [
	path('', TelegramBotsView.as_view(), name='telegram_bots'),
	path('<int:telegram_bot_id>/', include([
		path('', TelegramBotView.as_view(), name='telegram_bot'),
		path('start-or-stop/', start_or_stop_telegram_bot, name='start_or_stop_telegram_bot'),

		path('commands/', TelegramBotCommandsView.as_view(), name='telegram_bot_commands'),
		path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandView.as_view(), name='telegram_bot_command'),

		path('diagram/', include([
			path('commands/', TelegramBotCommandsDiagramAPIView.as_view(), name='diagram_telegram_bot_commands'),
			path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandDiagramAPIView.as_view(), name='diagram_telegram_bot_command'),
		])),

		path('users/', TelegramBotUsersView.as_view(), name='telegram_bot_users'),
		path('users/<int:telegram_bot_user_id>/', include([
			path('', TelegramBotUserView.as_view(), name='telegram_bot_user'),
			path('allowed-user/', TelegramBotAllowedUserView.as_view(), name='telegram_bot_allowed_user'),
		])),
	])),
]