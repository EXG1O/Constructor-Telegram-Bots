from django.urls import path

from . import views


app_name = 'frontend'
urlpatterns = [
	path('', views.telegram_bot_view, name='telegram_bot'),
	path('variables/', views.telegram_bot_variables_view, name='telegram_bot_variables'),
	path('users/', views.telegram_bot_users_view, name='telegram_bot_users'),
	path('database/', views.telegram_bot_database_view, name='telegram_bot_database'),
	path('plugins/', views.telegram_bot_plugins_view, name='telegram_bot_plugins'),
	path('constructor/', views.telegram_bot_constructor_view, name='telegram_bot_constructor'),
]
