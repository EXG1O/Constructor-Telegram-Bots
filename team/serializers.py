from rest_framework import serializers

from utils import filters

from .models import Member

from typing import Any


class MemberSerializer(serializers.ModelSerializer[Member]):
	class Meta:
		model = Member
		fields = ('id', 'image', 'username', 'speciality')

	def to_representation(self, instance: Member) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['joined_date'] = filters.datetime(instance.joined_date)

		return representation