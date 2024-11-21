from rest_framework import serializers

from .models import Donation, Method, Section


class DonationSerializer(serializers.ModelSerializer[Donation]):
	class Meta:
		model = Donation
		fields = ['id', 'sum', 'sender', 'date']


class SectionSerializer(serializers.ModelSerializer[Section]):
	class Meta:
		model = Section
		fields = ['id', 'title', 'text']


class MethodSerializer(serializers.ModelSerializer[Method]):
	class Meta:
		model = Method
		fields = ['id', 'text', 'link', 'value']
