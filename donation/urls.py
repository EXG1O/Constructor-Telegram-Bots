from django.urls import path

from .views import DonationsAPIView, DonationButtonsAPIView, DonationSectionsAPIView


urlpatterns = [
	path('', DonationsAPIView.as_view()),
	path('sections/', DonationSectionsAPIView.as_view()),
	path('buttons/', DonationButtonsAPIView.as_view()),
]