from django.urls import path

from .views import DonationsAPIView, DonationButtonsAPIView, DonationSectionsAPIView


urlpatterns = [
	path('', DonationsAPIView.as_view(), name='donations'),
	path('sections/', DonationSectionsAPIView.as_view(), name='donation-sections'),
	path('buttons/', DonationButtonsAPIView.as_view(), name='donation-buttons'),
]