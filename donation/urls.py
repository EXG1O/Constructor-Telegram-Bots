from django.urls import path

from .views import (
	DonationsAPIView,
	ButtonsAPIView,
	SectionsAPIView,
)


app_name = 'donation'
urlpatterns = [
	path('', DonationsAPIView.as_view(), name='index'),
	path('sections/', SectionsAPIView.as_view(), name='sections'),
	path('buttons/', ButtonsAPIView.as_view(), name='buttons'),
]
