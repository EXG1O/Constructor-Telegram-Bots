from django.urls import include, path

from rest_framework.routers import SimpleRouter

from .views import (
	BackgroundTaskViewSet,
	CommandViewSet,
	ConditionViewSet,
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

base_name: str = 'telegram-bot'
base_path: str = '<int:telegram_bot_id>'

router = SimpleRouter(use_regex_path=False)  # type: ignore [call-arg]  # use_regex_path param exists
router.register('', TelegramBotViewSet, basename=base_name)
router.register(f'{base_path}/connections', ConnectionViewSet, basename=f'{base_name}-connection')
router.register(f'{base_path}/commands', CommandViewSet, basename=f'{base_name}-command')
router.register(f'{base_path}/conditions', ConditionViewSet, basename=f'{base_name}-condition')
router.register(f'{base_path}/background-tasks', BackgroundTaskViewSet, basename=f'{base_name}-background-task')

app_name = 'telegram-bots'
urlpatterns = [
	path('stats/', StatsAPIView.as_view(), name='stats'),
	path('hub/<int:telegram_bot_id>/', include('telegram_bots.hub.urls')),
	path(
		'<int:telegram_bot_id>/',
		include(
			(
				[
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
