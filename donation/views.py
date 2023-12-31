from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from .models import Donation, DonationSection, DonationButton
from .serializers import (
	DonationSerializer,
	DonationSectionSerializer,
	DonationButtonSerializer,
)


class DonationsAPIView(ListAPIView[Donation]):
	authentication_classes = []
	permission_classes = []

	queryset = Donation.objects.all()
	serializer_class = DonationSerializer
	pagination_class = LimitOffsetPagination

class DonationSectionsAPIView(ListAPIView[DonationSection]):
	authentication_classes = []
	permission_classes = []

	queryset = DonationSection.objects.all()
	serializer_class = DonationSectionSerializer

class DonationButtonsAPIView(ListAPIView[DonationButton]):
	authentication_classes = []
	permission_classes = []

	queryset = DonationButton.objects.all()
	serializer_class = DonationButtonSerializer