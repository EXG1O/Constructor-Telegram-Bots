from django.urls import path

from .views import index_view


app_name = 'personal_cabinet'
urlpatterns = [
	path('', index_view, name='index'),
]
