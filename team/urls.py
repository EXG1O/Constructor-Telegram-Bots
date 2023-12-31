from django.urls import path

from .views import TeamMembersAPIView


urlpatterns = [
	path('members/', TeamMembersAPIView.as_view()),
]