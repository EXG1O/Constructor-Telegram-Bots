from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from .models import Update
from .serializers import UpdateSerializer


class UpdatesAPIView(ListAPIView):
	authentication_classes = []
	permission_classes = []

	queryset = Update.objects.all()
	serializer_class = UpdateSerializer
	pagination_class = LimitOffsetPagination