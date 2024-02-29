from django.urls import path, include

from .views import (
	TelegramBotsAPIView,
	TelegramBotAPIView,
	CommandsAPIView,
	CommandAPIView,
	DiagramCommandsAPIView,
	DiagramCommandAPIView,
	ConnectionsAPIView,
	ConnectionAPIView,
	VariablesAPIView,
	VariableAPIView,
	UsersAPIView,
	UserAPIView,
)


app_name = 'telegram-bots'
urlpatterns = [
	path('', TelegramBotsAPIView.as_view(), name='list'),
	path('hub/<int:telegram_bot_id>/', include('telegram_bots.hub.urls')),
	path('<int:telegram_bot_id>/', include(([
		path('', TelegramBotAPIView.as_view(), name='index'),

		path('commands/', CommandsAPIView.as_view(), name='commands'),
		path('commands/<int:command_id>/', CommandAPIView.as_view(), name='command'),

		path('diagram/', include(([
			path('commands/', DiagramCommandsAPIView.as_view(), name='commands'),
			path('commands/<int:command_id>/', DiagramCommandAPIView.as_view(), name='command'),

			path('connections/', ConnectionsAPIView.as_view(), name='connections'),
			path('connections/<int:connection_id>/', ConnectionAPIView.as_view(), name='connection'),
		], 'diagram'))),

		path('variables/', VariablesAPIView.as_view(), name='variables'),
		path('variables/<int:variable_id>/', VariableAPIView.as_view(), name='variable'),

		path('users/', UsersAPIView.as_view(), name='users'),
		path('users/<int:user_id>/', UserAPIView.as_view(), name='user'),
	], 'detail'))),
]