from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Section
from .serializers import SectionSerializer


class SectionsViewSet(ListModelMixin, GenericViewSet[Section]):
	authentication_classes = []
	permission_classes = []
	queryset = Section.objects.all()
	serializer_class = SectionSerializer
