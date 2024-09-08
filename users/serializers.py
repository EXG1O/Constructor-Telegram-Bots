from rest_framework import serializers

from .models import User


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
			'joined_date',
		]


class UserLoginSerializer(serializers.Serializer[User]):
	user_id = serializers.IntegerField()
	confirm_code = serializers.CharField()
