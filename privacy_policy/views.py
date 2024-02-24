from rest_framework.generics import ListAPIView

from .models import Section
from .serializers import SectionSerializer


class SectionsAPIView(ListAPIView[Section]):
	authentication_classes = []
	permission_classes = []
	queryset = Section.objects.all()
	serializer_class = SectionSerializer