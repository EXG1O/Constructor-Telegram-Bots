from rest_framework.generics import ListAPIView

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Donation, Section, Button
from .serializers import (
	DonationSerializer,
	SectionSerializer,
	ButtonSerializer,
)


class DonationsAPIView(ListAPIView[Donation]):
	authentication_classes = []
	permission_classes = []
	queryset = Donation.objects.all()
	serializer_class = DonationSerializer
	pagination_class = LimitOffsetPagination

class SectionsAPIView(ListAPIView[Section]):
	authentication_classes = []
	permission_classes = []
	queryset = Section.objects.all()
	serializer_class = SectionSerializer

class ButtonsAPIView(ListAPIView[Button]):
	authentication_classes = []
	permission_classes = []
	queryset = Button.objects.all()
	serializer_class = ButtonSerializer