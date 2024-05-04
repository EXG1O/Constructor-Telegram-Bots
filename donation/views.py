from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Button, Donation, Section
from .serializers import ButtonSerializer, DonationSerializer, SectionSerializer


class DonationViewSet(ListModelMixin, GenericViewSet[Donation]):
	authentication_classes = []
	permission_classes = []
	queryset = Donation.objects.all()
	serializer_class = DonationSerializer
	pagination_class = LimitOffsetPagination


class SectionViewSet(ListModelMixin, GenericViewSet[Section]):
	authentication_classes = []
	permission_classes = []
	queryset = Section.objects.all()
	serializer_class = SectionSerializer


class ButtonViewSet(ListModelMixin, GenericViewSet[Button]):
	authentication_classes = []
	permission_classes = []
	queryset = Button.objects.all()
	serializer_class = ButtonSerializer
