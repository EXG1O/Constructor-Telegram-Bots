from django.urls import path

from .views import (
	TelegramBotsView,
	TelegramBotView,
	start_or_stop_telegram_bot,
	update_telegram_bot_diagram_current_scale,
	TelegramBotCommandsView,
	TelegramBotCommandView,
	update_telegram_bot_command_position,
	TelegramBotCommandKeyboardButtonTelegramBotCommandView,
	TelegramBotUsersView,
	TelegramBotUserView,
	TelegramBotAllowedUserView,
)


urlpatterns = [
	path('', TelegramBotsView.as_view(), name='telegram_bots'),
    path('<int:telegram_bot_id>/', TelegramBotView.as_view(), name='telegram_bot'),
	path('<int:telegram_bot_id>/start-or-stop/', start_or_stop_telegram_bot, name='start_or_stop_telegram_bot'),
    path('<int:telegram_bot_id>/update-diagram-current-scale/', update_telegram_bot_diagram_current_scale, name='update_telegram_bot_diagram_current_scale'),

	path('<int:telegram_bot_id>/commands/', TelegramBotCommandsView.as_view(), name='telegram_bot_commands'),
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/', TelegramBotCommandView.as_view(), name='telegram_bot_command'),
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/update-position/', update_telegram_bot_command_position, name='update_telegram_bot_command_position'),
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/keyboard-buttons/<int:telegram_bot_command_keyboard_button_id>/telegram-bot-command/', TelegramBotCommandKeyboardButtonTelegramBotCommandView.as_view(), name='telegram_bot_command_keyboard_button_telegram_bot_command'),

	path('<int:telegram_bot_id>/users/', TelegramBotUsersView.as_view(), name='telegram_bot_users'),
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/', TelegramBotUserView.as_view(), name='telegram_bot_user'),
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/allowed-user/', TelegramBotAllowedUserView.as_view(), name='telegram_bot_allowed_user'),
]