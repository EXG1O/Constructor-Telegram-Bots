from django.urls import path

from telegram_bot import views


urlpatterns = [
	path('add/', views.add_telegram_bot),
	path('<int:telegram_bot_id>/edit/', views.edit_telegram_bot),
	path('<int:telegram_bot_id>/duplicate/', views.duplicate_telegram_bot),
	path('<int:telegram_bot_id>/delete/', views.delete_telegram_bot),

	path('<int:telegram_bot_id>/start/', views.start_telegram_bot),
	path('<int:telegram_bot_id>/stop/', views.stop_telegram_bot),

	path('<int:telegram_bot_id>/command/add/', views.add_telegram_bot_command),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/get-data/', views.get_telegram_bot_command_data),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/edit/', views.edit_telegram_bot_command),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/delete/', views.delete_telegram_bot_command),

	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/add-allowed-user/', views.add_allowed_user),
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/delete-allowed-user/', views.delete_allowed_user),
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/delete/', views.delete_telegram_bot_user),

	path('<int:telegram_bot_id>/get-commands/', views.get_telegram_bot_commands),
	path('<int:telegram_bot_id>/get-users/', views.get_telegram_bot_users),
]
