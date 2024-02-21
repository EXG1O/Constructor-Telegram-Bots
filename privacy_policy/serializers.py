from rest_framework import serializers

from .models import PrivacyPolicySection


class PrivacyPolicySectionSerializer(serializers.ModelSerializer[PrivacyPolicySection]):
	class Meta:
		model = PrivacyPolicySection
		fields = ('id', 'title', 'text')