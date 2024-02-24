from django.urls import path

from .views import MembersAPIView


app_name = 'team'
urlpatterns = [
	path('members/', MembersAPIView.as_view(), name='members'),
]