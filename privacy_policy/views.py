from rest_framework.generics import ListAPIView

from .models import PrivacyPolicySection
from .serializers import PrivacyPolicySectionSerializer


class PrivacyPolicySectionsAPIView(ListAPIView[PrivacyPolicySection]):
	authentication_classes = []
	permission_classes = []

	queryset = PrivacyPolicySection.objects.all()
	serializer_class = PrivacyPolicySectionSerializer