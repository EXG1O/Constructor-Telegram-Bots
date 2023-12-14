from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import InstructionSection
from .serializers import InstructionSectionModelSerializer


class InstructionSectionsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response(
			InstructionSectionModelSerializer(
				InstructionSection.objects.all(),
				many=True,
			).data
		)