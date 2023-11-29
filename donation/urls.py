from django.urls import path

from .views import index_view, completed_view


app_name = 'donation'
urlpatterns = [
	path('', index_view, name='index'),
    path('completed/', completed_view, name='completed'),
]
