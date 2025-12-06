from rest_framework import serializers

from .jwt.tokens import RefreshToken
from .models import User
from .utils.auth import authenticate_token


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
    id = serializers.IntegerField()
    first_name = serializers.CharField(min_length=1, max_length=64)
    last_name = serializers.CharField(max_length=64, required=False)
    username = serializers.CharField(min_length=4, max_length=32, required=False)
    photo_url = serializers.URLField(required=False)
    auth_date = serializers.IntegerField()
    hash = serializers.CharField(min_length=64, max_length=64)


class UserTokenRefreshSerializer(serializers.Serializer[User]):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, raw_refresh_token: str) -> RefreshToken:
        _, refresh_token = authenticate_token(
            raw_refresh_token,
            token_cls=RefreshToken,
            exception_cls=serializers.ValidationError,
        )
        return refresh_token
