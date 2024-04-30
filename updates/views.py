from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Update
from .serializers import UpdateSerializer


class UpdateViewSet(ListModelMixin, GenericViewSet[Update]):
	authentication_classes = []
	permission_classes = []
	queryset = Update.objects.all()
	serializer_class = UpdateSerializer
	pagination_class = LimitOffsetPagination
