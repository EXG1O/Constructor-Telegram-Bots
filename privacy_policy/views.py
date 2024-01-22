from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from utils import filters

from .models import PrivacyPolicySection
from .serializers import PrivacyPolicySectionSerializer


class PrivacyPolicySectionsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		last_updated_section: PrivacyPolicySection | None = PrivacyPolicySection.objects.order_by('last_update_date').first()

		return Response({
			'last_update_date': filters.datetime(last_updated_section.last_update_date) if last_updated_section else None,
			'results': PrivacyPolicySectionSerializer(
				PrivacyPolicySection.objects.all(),
				many=True,
			).data,
		})