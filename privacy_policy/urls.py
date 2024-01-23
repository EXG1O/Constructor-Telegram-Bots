from django.urls import path

from .views import PrivacyPolicySectionsAPIView


app_name = 'privacy-policy'
urlpatterns = [
	path('sections/', PrivacyPolicySectionsAPIView.as_view(), name='sections'),
]