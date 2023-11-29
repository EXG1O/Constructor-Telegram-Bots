from django.urls import path

from .views import CustomTemplateView


app_name = 'frontend'
urlpatterns = [
	path('', CustomTemplateView.as_view(template_name='telegram_bot_menu/index.html'), name='index'),
	path('variables/', CustomTemplateView.as_view(template_name='telegram_bot_menu/variables/main.html'), name='variables'),
	path('users/', CustomTemplateView.as_view(template_name='telegram_bot_menu/users.html'), name='users'),
	path('database/', CustomTemplateView.as_view(template_name='telegram_bot_menu/database.html'), name='database'),
	path('plugins/', CustomTemplateView.as_view(template_name='telegram_bot_menu/plugins.html'), name='plugins'),
	path('constructor/', CustomTemplateView.as_view(template_name='telegram_bot_menu/constructor.html'), name='constructor'),
]
