from django.urls import path

from .views import TeamMembersAPIView


app_name = 'team'
urlpatterns = [
	path('members/', TeamMembersAPIView.as_view(), name='members'),
]