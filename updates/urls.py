from django.urls import path

from .views import UpdatesAPIView


urlpatterns = [
	path('updates/', UpdatesAPIView.as_view(), name='updates'),
]