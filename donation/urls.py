from django.urls import path

from .views import DonationsAPIView, DonationButtonsAPIView, DonationSectionsAPIView


app_name = 'donations'
urlpatterns = [
	path('', DonationsAPIView.as_view(), name='index'),
	path('sections/', DonationSectionsAPIView.as_view(), name='sections'),
	path('buttons/', DonationButtonsAPIView.as_view(), name='buttons'),
]