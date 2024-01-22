from django.urls import path

from .views import PrivacyPolicySectionsAPIView


urlpatterns = [
	path('sections/', PrivacyPolicySectionsAPIView.as_view()),
]