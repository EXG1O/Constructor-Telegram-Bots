from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Section
from .serializers import SectionSerializer


@method_decorator(cache_page(3600), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class SectionsViewSet(ListModelMixin, GenericViewSet[Section]):
    authentication_classes = []
    permission_classes = []
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
