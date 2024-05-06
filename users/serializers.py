from rest_framework import serializers

from utils.formats import date_time_format

from .models import User

from typing import Any


class UserSerializer(serializers.ModelSerializer[User]):
	class Meta:
		model = User
		fields = [
			'id',
			'telegram_id',
			'first_name',
			'last_name',
			'full_name',
			'is_staff',
		]

	def to_representation(self, instance: User) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['joined_date'] = date_time_format(instance.joined_date)

		return representation


class UserLoginSerializer(serializers.Serializer[User]):
	user_id = serializers.IntegerField()
	confirm_code = serializers.CharField()
