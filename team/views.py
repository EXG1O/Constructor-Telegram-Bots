from rest_framework.generics import ListAPIView

from .models import Member
from .serializers import MemberSerializer


class MembersAPIView(ListAPIView[Member]):
	authentication_classes = []
	permission_classes = []
	queryset = Member.objects.all()
	serializer_class = MemberSerializer