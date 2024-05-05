from rest_framework import serializers

from .base_models import AbstractBlock

from typing import Any, TypeVar

ABT = TypeVar('ABT', bound=AbstractBlock)


class DiagramSerializer(serializers.ModelSerializer[ABT]):
	class Meta:
		fields = ['x', 'y']

	def update(self, instance: ABT, validated_data: dict[str, Any]) -> ABT:
		instance.x = validated_data.get('x', instance.x)
		instance.y = validated_data.get('y', instance.y)
		instance.save()

		return instance
