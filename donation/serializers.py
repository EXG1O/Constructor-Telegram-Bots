from rest_framework import serializers

from utils import filters

from .models import Donation, DonationSection, DonationButton

from typing import Any


class DonationModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Donation
		fields = ['id', 'sum', 'telegram_url', 'date']

	def to_representation(self, instance: Donation) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['date'] = filters.datetime(instance.date)

		return representation

class DonationSectionModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = DonationSection
		fields = ['id', 'title', 'text']

class DonationButtonModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = DonationButton
		fields = ['id', 'text', 'url']

class GetDonationsSerializer(serializers.Serializer):
	offset = serializers.IntegerField(default=None)
	limit = serializers.IntegerField(default=None)