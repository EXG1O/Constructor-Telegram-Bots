from django.urls import path

from .views import SectionsAPIView


app_name = 'instruction'
urlpatterns = [
	path('sections/', SectionsAPIView.as_view(), name='sections'),
]