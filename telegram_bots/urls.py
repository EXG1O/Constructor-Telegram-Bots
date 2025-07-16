from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import (
    APIRequestViewSet,
    BackgroundTaskViewSet,
    CommandViewSet,
    ConditionViewSet,
    ConnectionViewSet,
    DatabaseRecordViewSet,
    DiagramAPIRequestViewSet,
    DiagramBackgroundTaskViewSet,
    DiagramCommandViewSet,
    DiagramConditionViewSet,
    DiagramTriggerViewSet,
    StatsAPIView,
    TelegramBotViewSet,
    TriggerViewSet,
    UserViewSet,
    VariableViewSet,
)

base_path: str = '<int:telegram_bot_id>'
base_name: str = 'telegram-bot'

base_diagram_path: str = f'{base_path}/diagram'
base_diagram_name: str = f'{base_name}-diagram'

router = SimpleRouter(use_regex_path=False)
router.register('', TelegramBotViewSet, basename=base_name)
router.register(
    f'{base_path}/connections',
    ConnectionViewSet,
    basename=f'{base_name}-connection',
)

router.register(
    f'{base_path}/triggers',
    TriggerViewSet,
    basename=f'{base_name}-trigger',
)
router.register(
    f'{base_diagram_path}/triggers',
    DiagramTriggerViewSet,
    basename=f'{base_diagram_name}-trigger',
)

router.register(
    f'{base_path}/commands',
    CommandViewSet,
    basename=f'{base_name}-command',
)
router.register(
    f'{base_diagram_path}/commands',
    DiagramCommandViewSet,
    basename=f'{base_diagram_name}-command',
)

router.register(
    f'{base_path}/conditions',
    ConditionViewSet,
    basename=f'{base_name}-condition',
)
router.register(
    f'{base_diagram_path}/conditions',
    DiagramConditionViewSet,
    basename=f'{base_diagram_name}-condition',
)

router.register(
    f'{base_path}/background-tasks',
    BackgroundTaskViewSet,
    basename=f'{base_name}-background-task',
)
router.register(
    f'{base_diagram_path}/background-tasks',
    DiagramBackgroundTaskViewSet,
    basename=f'{base_diagram_name}-background-task',
)

router.register(
    f'{base_path}/api-requests',
    APIRequestViewSet,
    basename=f'{base_name}-api-request',
)
router.register(
    f'{base_diagram_path}/api-requests',
    DiagramAPIRequestViewSet,
    basename=f'{base_diagram_name}-api-request',
)

router.register(
    f'{base_path}/variables',
    VariableViewSet,
    basename=f'{base_name}-variable',
)
router.register(f'{base_path}/users', UserViewSet, basename=f'{base_name}-user')
router.register(
    f'{base_path}/database-records',
    DatabaseRecordViewSet,
    basename=f'{base_name}-database-record',
)

app_name = 'telegram-bots'
urlpatterns = [path('stats/', StatsAPIView.as_view(), name='stats')] + router.urls
