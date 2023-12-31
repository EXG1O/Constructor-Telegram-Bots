from django.urls import path

from .views import UpdatesAPIView


urlpatterns = [
	path('', UpdatesAPIView.as_view()),
]