from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (
	BackgroundTaskAPIView,
	BackgroundTasksAPIView,
	CommandAPIView,
	CommandsAPIView,
	ConditionAPIView,
	ConditionsAPIView,
	ConnectionViewSet,
	DatabaseRecordAPIView,
	DatabaseRecordsAPIView,
	DiagramBackgroundTaskAPIView,
	DiagramBackgroundTasksAPIView,
	DiagramCommandAPIView,
	DiagramCommandsAPIView,
	DiagramConditionAPIView,
	DiagramConditionsAPIView,
	StatsAPIView,
	TelegramBotViewSet,
	UserAPIView,
	UsersAPIView,
	VariableAPIView,
	VariablesAPIView,
)

router = SimpleRouter(use_regex_path=False)  # type: ignore [call-arg]  # use_regex_path param exists
router.register('', TelegramBotViewSet, basename='telegram-bot')
router.register('<int:telegram_bot_id>/connections', ConnectionViewSet, basename='telegram-bot-connection')

app_name = 'telegram-bots'
urlpatterns = [
	path('stats/', StatsAPIView.as_view(), name='stats'),
	path('hub/<int:telegram_bot_id>/', include('telegram_bots.hub.urls')),
	path(
		'<int:telegram_bot_id>/',
		include(
			(
				[
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
] + router.urls
