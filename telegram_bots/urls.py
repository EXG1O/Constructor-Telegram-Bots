from django.urls import path, include

from .views import (
	StatsAPIView,
	TelegramBotsAPIView,
	TelegramBotAPIView,
	ConnectionsAPIView,
	ConnectionAPIView,
	CommandsAPIView,
	CommandAPIView,
	ConditionsAPIView,
	ConditionAPIView,
	BackgroundTasksAPIView,
	BackgroundTaskAPIView,
	DiagramCommandsAPIView,
	DiagramCommandAPIView,
	DiagramConditionsAPIView,
	DiagramConditionAPIView,
	DiagramBackgroundTasksAPIView,
	DiagramBackgroundTaskAPIView,
	VariablesAPIView,
	VariableAPIView,
	UsersAPIView,
	UserAPIView,
	DatabaseRecordsAPIView,
	DatabaseRecordAPIView,
)


app_name = 'telegram-bots'
urlpatterns = [
	path('stats/', StatsAPIView.as_view(), name='stats'),
	path('', TelegramBotsAPIView.as_view(), name='list'),
	path('hub/<int:telegram_bot_id>/', include('telegram_bots.hub.urls')),
	path(
		'<int:telegram_bot_id>/',
		include(
			(
				[
					path('', TelegramBotAPIView.as_view(), name='index'),
					path('connections/', ConnectionsAPIView.as_view(), name='connections'),
					path('connections/<int:connection_id>/', ConnectionAPIView.as_view(), name='connection'),
					path('commands/', CommandsAPIView.as_view(), name='commands'),
					path('commands/<int:command_id>/', CommandAPIView.as_view(), name='command'),
					path('conditions/', ConditionsAPIView.as_view(), name='conditions'),
					path('conditions/<int:condition_id>/', ConditionAPIView.as_view(), name='condition'),
					path('background-tasks/', BackgroundTasksAPIView.as_view(), name='background-tasks'),
					path(
						'background-tasks/<int:background_task_id>/',
						BackgroundTaskAPIView.as_view(),
						name='background-task',
					),
					path(
						'diagram/',
						include(
							(
								[
									path('commands/', DiagramCommandsAPIView.as_view(), name='commands'),
									path('commands/<int:command_id>/', DiagramCommandAPIView.as_view(), name='command'),
									path('conditions/', DiagramConditionsAPIView.as_view(), name='conditions'),
									path(
										'conditions/<int:condition_id>/',
										DiagramConditionAPIView.as_view(),
										name='condition',
									),
									path(
										'background-tasks/',
										DiagramBackgroundTasksAPIView.as_view(),
										name='background-tasks',
									),
									path(
										'background-tasks/<int:background_task_id>/',
										DiagramBackgroundTaskAPIView.as_view(),
										name='background-task',
									),
								],
								'diagram',
							)
						),
					),
					path('variables/', VariablesAPIView.as_view(), name='variables'),
					path('variables/<int:variable_id>/', VariableAPIView.as_view(), name='variable'),
					path('users/', UsersAPIView.as_view(), name='users'),
					path('users/<int:user_id>/', UserAPIView.as_view(), name='user'),
					path('database-records/', DatabaseRecordsAPIView.as_view(), name='database-records'),
					path(
						'database-records/<int:database_record_id>/',
						DatabaseRecordAPIView.as_view(),
						name='database-record',
					),
				],
				'detail',
			)
		),
	),
]
