from rest_framework import serializers

from utils.formats import date_time_format

from .models import Button, Donation, Section

from typing import Any


class DonationSerializer(serializers.ModelSerializer[Donation]):
	class Meta:
		model = Donation
		fields = ['id', 'sum', 'contact_link']

	def to_representation(self, instance: Donation) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['date'] = date_time_format(instance.date)

		return representation


class SectionSerializer(serializers.ModelSerializer[Section]):
	class Meta:
		model = Section
		fields = ['id', 'title', 'text']


class ButtonSerializer(serializers.ModelSerializer[Button]):
	class Meta:
		model = Button
		fields = ['id', 'text', 'url']
