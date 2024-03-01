from django.urls import path, include

from .views import (
	TelegramBotsAPIView,
	TelegramBotAPIView,
	ConnectionsAPIView,
	ConnectionAPIView,
	CommandsAPIView,
	CommandAPIView,
	ConditionsAPIView,
	ConditionAPIView,
	DiagramCommandsAPIView,
	DiagramCommandAPIView,
	DiagramConditionsAPIView,
	DiagramConditionAPIView,
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

		path('connections/', ConnectionsAPIView.as_view(), name='connections'),
		path('connections/<int:connection_id>/', ConnectionAPIView.as_view(), name='connection'),

		path('commands/', CommandsAPIView.as_view(), name='commands'),
		path('commands/<int:command_id>/', CommandAPIView.as_view(), name='command'),

		path('conditions/', ConditionsAPIView.as_view(), name='conditions'),
		path('conditions/<int:condition_id>/', ConditionAPIView.as_view(), name='condition'),

		path('diagram/', include(([
			path('commands/', DiagramCommandsAPIView.as_view(), name='commands'),
			path('commands/<int:command_id>/', DiagramCommandAPIView.as_view(), name='command'),

			path('conditions/', DiagramConditionsAPIView.as_view(), name='conditions'),
			path('conditions/<int:condition_id>/', DiagramConditionAPIView.as_view(), name='condition'),
		], 'diagram'))),

		path('variables/', VariablesAPIView.as_view(), name='variables'),
		path('variables/<int:variable_id>/', VariableAPIView.as_view(), name='variable'),

		path('users/', UsersAPIView.as_view(), name='users'),
		path('users/<int:user_id>/', UserAPIView.as_view(), name='user'),
	], 'detail'))),
]