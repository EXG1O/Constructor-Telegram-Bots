from rest_framework.routers import SimpleRouter

from .views import (
    APIRequestViewSet,
    BackgroundTaskViewSet,
    ConditionViewSet,
    DatabaseOperationViewSet,
    DatabaseRecordViewSet,
    MessageKeyboardButtonViewSet,
    MessageViewSet,
    TelegramBotViewSet,
    TriggerViewSet,
    UserViewSet,
    VariableViewSet,
)

base_path: str = '<int:telegram_bot_id>'
base_name: str = 'telegram-bot'

router = SimpleRouter(use_regex_path=False)
router.register('', TelegramBotViewSet, basename=base_name)
router.register(
    f'{base_path}/triggers',
    TriggerViewSet,
    basename=f'{base_name}-trigger',
)
router.register(
    f'{base_path}/messages',
    MessageViewSet,
    basename=f'{base_name}-message',
)
router.register(
    f'{base_path}/messages-keyboard-buttons',
    MessageKeyboardButtonViewSet,
    basename=f'{base_name}-messages-keyboard-button',
)
router.register(
    f'{base_path}/conditions',
    ConditionViewSet,
    basename=f'{base_name}-condition',
)
router.register(
    f'{base_path}/background-tasks',
    BackgroundTaskViewSet,
    basename=f'{base_name}-background-task',
)
router.register(
    f'{base_path}/api-requests',
    APIRequestViewSet,
    basename=f'{base_name}-api-request',
)
router.register(
    f'{base_path}/database-operations',
    DatabaseOperationViewSet,
    basename=f'{base_name}-database-operation',
)
router.register(
    f'{base_path}/variables',
    VariableViewSet,
    basename=f'{base_name}-variable',
)
router.register(
    f'{base_path}/users',
    UserViewSet,
    basename=f'{base_name}-user',
)
router.register(
    f'{base_path}/database-records',
    DatabaseRecordViewSet,
    basename=f'{base_name}-database-record',
)

app_name = 'telegram-bots-hub'
urlpatterns = router.urls
