from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import TeamMember
from .serializers import TeamMemberModelSerializer


class TeamMembersAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response(
			TeamMemberModelSerializer(
				TeamMember.objects.all(),
				many=True,
			).data
		)