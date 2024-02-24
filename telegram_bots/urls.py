from django.urls import path, include

from .views import (
	TelegramBotsAPIView,
	TelegramBotAPIView,
	TelegramBotCommandsAPIView,
	TelegramBotCommandAPIView,
	TelegramBotCommandsDiagramAPIView,
	TelegramBotCommandDiagramAPIView,
	TelegramBotVariablesAPIView,
	TelegramBotVariableAPIView,
	TelegramBotUsersAPIView,
	TelegramBotUserAPIView,
)


app_name = 'telegram-bots'
urlpatterns = [
	path('', TelegramBotsAPIView.as_view(), name='index'),
	path('hub/<int:telegram_bot_id>/', include('telegram_bots.hub.urls')),
	path('<int:telegram_bot_id>/', include(([
		path('', TelegramBotAPIView.as_view(), name='index'),

		path('commands/', TelegramBotCommandsAPIView.as_view(), name='commands'),
		path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandAPIView.as_view(), name='command'),

		path('diagram/', include(([
			path('commands/', TelegramBotCommandsDiagramAPIView.as_view(), name='commands'),
			path('commands/<int:telegram_bot_command_id>/', TelegramBotCommandDiagramAPIView.as_view(), name='command'),
		], 'diagram'))),

		path('variables/', TelegramBotVariablesAPIView.as_view(), name='variables'),
		path('variables/<int:telegram_bot_variable_id>/', TelegramBotVariableAPIView.as_view(), name='variable'),

		path('users/', TelegramBotUsersAPIView.as_view(), name='users'),
		path('users/<int:telegram_bot_user_id>/', TelegramBotUserAPIView.as_view(), name='user'),
	], 'detail'))),
]