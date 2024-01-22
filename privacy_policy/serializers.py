from rest_framework import serializers

from .models import PrivacyPolicySection


class PrivacyPolicySectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PrivacyPolicySection
		fields = ('id', 'title', 'text')