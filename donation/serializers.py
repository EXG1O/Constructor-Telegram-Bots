from rest_framework import serializers

from .models import Button, Donation, Section


class DonationSerializer(serializers.ModelSerializer[Donation]):
	class Meta:
		model = Donation
		fields = ['id', 'sum', 'contact_link', 'date']


class SectionSerializer(serializers.ModelSerializer[Section]):
	class Meta:
		model = Section
		fields = ['id', 'title', 'text']


class ButtonSerializer(serializers.ModelSerializer[Button]):
	class Meta:
		model = Button
		fields = ['id', 'text', 'url']
