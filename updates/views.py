from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from constructor_telegram_bots.pagination import LimitOffsetPagination

from .models import Update
from .serializers import UpdateSerializer


@method_decorator(cache_page(3600), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class UpdateViewSet(ListModelMixin, GenericViewSet[Update]):
    authentication_classes = []
    permission_classes = []
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    pagination_class = LimitOffsetPagination
