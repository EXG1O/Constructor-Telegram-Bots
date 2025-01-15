from rest_framework.routers import SimpleRouter

from .views import (
	BackgroundTaskViewSet,
	CommandKeyboardButtonViewSet,
	CommandTriggerViewSet,
	CommandViewSet,
	ConditionViewSet,
	DatabaseRecordViewSet,
	TelegramBotViewSet,
	UserViewSet,
	VariableViewSet,
)

base_path: str = '<int:telegram_bot_id>'
base_name: str = 'telegram-bot'

router = SimpleRouter(use_regex_path=False)
router.register('', TelegramBotViewSet, basename=base_name)
router.register(
	f'{base_path}/commands',
	CommandViewSet,
	basename=f'{base_name}-command',
)
router.register(
	f'{base_path}/command-triggers',
	CommandTriggerViewSet,
	basename=f'{base_name}-command-trigger',
)
router.register(
	f'{base_path}/commands-keyboard-buttons',
	CommandKeyboardButtonViewSet,
	basename=f'{base_name}-commands-keyboard-button',
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
