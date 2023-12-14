from django.utils.translation import gettext as _
from django.template import defaultfilters as filters

from rest_framework import serializers

from .models import TeamMember

from typing import Any


class TeamMemberModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = TeamMember
		fields = ['id', 'image', 'username', 'speciality', 'joined_date']

	def to_representation(self, instance: TeamMember) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['joined_date'] = f'{filters.date(instance.joined_date)} {filters.time(instance.joined_date)}'

		return representation