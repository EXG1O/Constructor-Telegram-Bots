from django.urls import path, include

from .views import (
	TelegramBotsAPIView,
	TelegramBotAPIView,
	TelegramBotCommandsAPIView,
	TelegramBotCommandAPIView,
	TelegramBotCommandsDiagramAPIView,
	TelegramBotCommandDiagramAPIView,
	TelegramBotUsersAPIView,
	TelegramBotUserAPIView,
)


urlpatterns = [
	path('', TelegramBotsAPIView.as_view()),
	path('<int:telegram_bot_id>/', include([
		path('', TelegramBotAPIView.as_view()),

		path('commands/', TelegramBotCommandsAPIView.as_view()),
		path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandAPIView.as_view()),

		path('diagram/', include([
			path('commands/', TelegramBotCommandsDiagramAPIView.as_view()),
			path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandDiagramAPIView.as_view()),
		])),

		path('users/', TelegramBotUsersAPIView.as_view()),
		path('users/<int:telegram_bot_user_id>/', TelegramBotUserAPIView.as_view()),
	])),
]