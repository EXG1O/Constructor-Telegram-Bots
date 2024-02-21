from rest_framework.generics import ListAPIView

from .models import InstructionSection
from .serializers import InstructionSectionSerializer


class InstructionSectionsAPIView(ListAPIView[InstructionSection]):
	authentication_classes = []
	permission_classes = []
	queryset = InstructionSection.objects.all()
	serializer_class = InstructionSectionSerializer