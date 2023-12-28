from rest_framework.generics import ListAPIView

from .models import InstructionSection
from .serializers import InstructionSectionSerializer


class InstructionSectionsAPIView(ListAPIView):
	authentication_classes = []
	permission_classes = []

	queryset = InstructionSection.objects.all()
	serializer_class = InstructionSectionSerializer