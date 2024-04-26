from rest_framework.generics import ListAPIView

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Update
from .serializers import UpdateSerializer


class UpdatesAPIView(ListAPIView[Update]):
	authentication_classes = []
	permission_classes = []
	queryset = Update.objects.all()
	serializer_class = UpdateSerializer
	pagination_class = LimitOffsetPagination
