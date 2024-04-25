from django.urls import path

from .views import UpdatesAPIView


app_name = 'updates'
urlpatterns = [
	path('', UpdatesAPIView.as_view(), name='list'),
]
