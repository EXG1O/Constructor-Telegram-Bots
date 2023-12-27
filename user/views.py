from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from utils.drf import CustomResponse

from .models import User
from .serializers import UserModelSerializer, AuthTokenSerializer

from typing import Any


class UsersAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response({'users_count': User.objects.count()})

class UserAPIView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		return Response(UserModelSerializer(request.user).data)

	def delete(self, request: Request) -> CustomResponse:
		request.user.delete()

		return CustomResponse(_('Вы успешно удалили свой аккаунт.'))

class UserLoginAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request: Request) -> CustomResponse:
		serializer = AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		user_id: int = validated_data['user_id']
		confirm_code: str = validated_data['confirm_code']

		try:
			user: User = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return CustomResponse(_('Не удалось найти пользователя!'), status=404)

		if user.confirm_code != confirm_code:
			return CustomResponse(_('Неверный код подтверждения!'), status=401)

		user.confirm_code = None
		user.save()

		auth_token, created = Token.objects.get_or_create(user=user)

		response = CustomResponse(_('Вы успешно вошли в аккаунт.'))
		response.set_cookie('auth-token', auth_token.key)

		return response

class UserLogoutAPIView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> CustomResponse:
		request.user.auth_token.delete()

		response = CustomResponse(_('Вы успешно вышли из своего аккаунта.'))
		response.delete_cookie('auth-token')

		return response