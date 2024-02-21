from rest_framework import serializers

from utils import filters

from .models import TeamMember

from typing import Any


class TeamMemberSerializer(serializers.ModelSerializer[TeamMember]):
	class Meta:
		model = TeamMember
		fields = ('id', 'image', 'username', 'speciality', 'joined_date')

	def to_representation(self, instance: TeamMember) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['joined_date'] = filters.datetime(instance.joined_date)

		return representation