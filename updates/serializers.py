from rest_framework import serializers

from utils.formats import date_time_format

from .models import Update

from typing import Any


class UpdateSerializer(serializers.ModelSerializer[Update]):
	class Meta:
		model = Update
		fields = ['id', 'version', 'description']

	def to_representation(self, instance: Update) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = date_time_format(instance.added_date)

		return representation
