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
	TelegramBotDatabeseRecordsView,
	TelegramBotDatabeseRecordView,
)


urlpatterns = [
	path('', TelegramBotsView.as_view(), name='telegram_bots'), # POST, GET
    path('<int:telegram_bot_id>/', TelegramBotView.as_view(), name='telegram_bot'), # PATCH, DELETE, GET
	path('<int:telegram_bot_id>/start-or-stop/', start_or_stop_telegram_bot, name='start_or_stop_telegram_bot'), # POST
    path('<int:telegram_bot_id>/update-diagram-current-scale/', update_telegram_bot_diagram_current_scale, name='update_telegram_bot_diagram_current_scale'), # PATCH

	path('<int:telegram_bot_id>/commands/', TelegramBotCommandsView.as_view(), name='telegram_bot_commands'), # POST, GET
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/', TelegramBotCommandView.as_view(), name='telegram_bot_command'), # PATCH, DELETE, GET
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/update-position/', update_telegram_bot_command_position, name='update_telegram_bot_command_position'), # PATCH
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/keyboard-buttons/<int:telegram_bot_command_keyboard_button_id>/telegram-bot-command/', TelegramBotCommandKeyboardButtonTelegramBotCommandView.as_view(), name='telegram_bot_command_keyboard_button_telegram_bot_command'), # POST, DELETE

	path('<int:telegram_bot_id>/users/', TelegramBotUsersView.as_view(), name='telegram_bot_users'), # GET
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/', TelegramBotUserView.as_view(), name='telegram_bot_user'), # DELETE
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/allowed-user/', TelegramBotAllowedUserView.as_view(), name='telegram_bot_allowed_user'), # POST, DELETE

	path('<int:telegram_bot_id>/database/records/', TelegramBotDatabeseRecordsView.as_view(), name='telegram_bot_databese_records'), # POST, GET
    path('<int:telegram_bot_id>/database/records/<int:record_id>/', TelegramBotDatabeseRecordView.as_view(), name='telegram_bot_databese_record'), # PATCH, DELETE
]