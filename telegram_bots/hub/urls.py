from django.urls import path

from .views import (
	TelegramBotAPIView,
	CommandsAPIView,
	CommandAPIView,
	VariablesAPIView,
	UsersAPIView,
)


app_name = 'hub'
urlpatterns = [
	path('', TelegramBotAPIView.as_view(), name='detail'),
	path('commands/', CommandsAPIView.as_view(), name='commands'),
	path('commands/<int:command_id>/', CommandAPIView.as_view(), name='command'),
	path('variables/', VariablesAPIView.as_view(), name='variables'),
	path('users/', UsersAPIView.as_view(), name='users'),
]
