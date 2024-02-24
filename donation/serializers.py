from rest_framework import serializers

from utils import filters

from .models import Donation, Section, Button

from typing import Any


class DonationSerializer(serializers.ModelSerializer[Donation]):
	class Meta:
		model = Donation
		fields = ('id', 'sum', 'contact_link')

	def to_representation(self, instance: Donation) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['date'] = filters.datetime(instance.date)

		return representation

class SectionSerializer(serializers.ModelSerializer[Section]):
	class Meta:
		model = Section
		fields = ('id', 'title', 'text')

class ButtonSerializer(serializers.ModelSerializer[Button]):
	class Meta:
		model = Button
		fields = ('id', 'text', 'url')