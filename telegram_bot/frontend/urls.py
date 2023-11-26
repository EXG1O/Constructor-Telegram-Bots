from django.urls import path

from .views import CustomTemplateView


app_name = 'frontend'
urlpatterns = [
	path('', CustomTemplateView.as_view(template_name='index.html'), name='index'),
	path('variables/', CustomTemplateView.as_view(template_name='variables/main.html'), name='variables'),
	path('users/', CustomTemplateView.as_view(template_name='users.html'), name='users'),
	path('database/', CustomTemplateView.as_view(template_name='database.html'), name='database'),
	path('plugins/', CustomTemplateView.as_view(template_name='plugins.html'), name='plugins'),
	path('constructor/', CustomTemplateView.as_view(template_name='constructor.html'), name='constructor'),
]
