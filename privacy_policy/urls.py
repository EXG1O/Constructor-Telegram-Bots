from django.urls import path

from .views import SectionsAPIView

app_name = 'privacy-policy'
urlpatterns = [
	path('sections/', SectionsAPIView.as_view(), name='sections'),
]
