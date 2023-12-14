from django.utils.translation import gettext as _
from django.template import defaultfilters as filters

from rest_framework import serializers

from .models import User

from typing import Any


class UserModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'telegram_id', 'first_name', 'is_staff', 'joined_date']

	def to_representation(self, instance: User) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['joined_date'] = f'{filters.date(instance.joined_date)} {filters.time(instance.joined_date)}'

		return representation

class AuthTokenSerializer(serializers.Serializer):
	user_id = serializers.IntegerField()
	confirm_code = serializers.CharField()