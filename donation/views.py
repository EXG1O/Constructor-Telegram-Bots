from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Button, Donation, Section
from .serializers import ButtonSerializer, DonationSerializer, SectionSerializer


@method_decorator(cache_page(3600), name='dispatch')
class DonationViewSet(ListModelMixin, GenericViewSet[Donation]):
	authentication_classes = []
	permission_classes = []
	queryset = Donation.objects.all()
	serializer_class = DonationSerializer
	pagination_class = LimitOffsetPagination


@method_decorator(cache_page(3600), name='dispatch')
class SectionViewSet(ListModelMixin, GenericViewSet[Section]):
	authentication_classes = []
	permission_classes = []
	queryset = Section.objects.all()
	serializer_class = SectionSerializer


@method_decorator(cache_page(3600), name='dispatch')
class ButtonViewSet(ListModelMixin, GenericViewSet[Button]):
	authentication_classes = []
	permission_classes = []
	queryset = Button.objects.all()
	serializer_class = ButtonSerializer
