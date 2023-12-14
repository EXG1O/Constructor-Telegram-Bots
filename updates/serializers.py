from django.template import defaultfilters as filters

from rest_framework import serializers

from .models import Update

from typing import Any


class UpdateModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Update
		fields = ['id', 'image', 'version', 'description', 'added_date']

	def to_representation(self, instance: Update) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = f'{filters.date(instance.added_date)} {filters.time(instance.added_date)}'

		return representation

class GetUpdatesSerializer(serializers.Serializer):
	offset = serializers.IntegerField(default=None)
	limit = serializers.IntegerField(default=None)