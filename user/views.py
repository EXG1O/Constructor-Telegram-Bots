from django.utils.translation import gettext as _
from django.contrib.auth import login, logout

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from utils.custom_response import CustomResponse

from .models import User
from .serializers import UserSerializer, UserLoginSerializer

from typing import Any


class UserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		return Response(UserSerializer(request.user).data)

	def delete(self, request: Request) -> CustomResponse:
		request.user.delete()

		response = CustomResponse(_('Вы успешно удалили свой аккаунт.'))
		response.delete_cookie('auth-token')

		return response

class UserLoginAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request: Request) -> CustomResponse:
		serializer = UserLoginSerializer(data=request.data)
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

		login(request, user)

		user.confirm_code = None
		user.save()

		auth_token, created = Token.objects.get_or_create(user=user)

		response = CustomResponse(_('Вы успешно вошли в аккаунт.'))
		response.set_cookie('auth-token', auth_token.key)

		return response

class UserLogoutAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request: Request) -> CustomResponse:
		request.user.auth_token.delete() # type: ignore [arg-type, union-attr]

		logout(request)

		response = CustomResponse(_('Вы успешно вышли из своего аккаунта.'))
		response.delete_cookie('auth-token')

		return response