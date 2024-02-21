from rest_framework import serializers

from utils import filters

from .models import Update

from typing import Any


class UpdateSerializer(serializers.ModelSerializer[Update]):
	class Meta:
		model = Update
		fields = ('id', 'version', 'description', 'added_date')

	def to_representation(self, instance: Update) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = filters.datetime(instance.added_date)

		return representation