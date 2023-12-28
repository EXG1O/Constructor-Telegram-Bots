from rest_framework.generics import ListAPIView

from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamMembersAPIView(ListAPIView):
	authentication_classes = []
	permission_classes = []

	queryset = TeamMember.objects.all()
	serializer_class = TeamMemberSerializer