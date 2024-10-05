from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from jwt import PyJWTError

from .authentication import JWTCookieAuthentication
from .backends import TelegramBackend
from .exceptions import TokenBlacklistedError, UserInactiveOrDeletedError
from .models import User
from .serializers import UserLoginSerializer, UserSerializer
from .tokens import RefreshToken
from .utils import (
	add_jwt_tokens_to_cookies,
	delete_jwt_tokens_from_cookies,
	get_refresh_token,
)
from .utils import login as user_login
from .utils import logout as user_logout
from .utils import logout_all as user_logout_all

from typing import Any


class StatsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	@method_decorator(cache_page(3600))
	def get(self, request: Request) -> Response:
		return Response({'total': User.objects.count()})


class UserViewSet(RetrieveModelMixin, DestroyModelMixin, GenericViewSet[User]):
	authentication_classes = [JWTCookieAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = UserSerializer

	def get_object(self) -> User:
		return self.request.user  # type: ignore [return-value]

	@action(
		detail=False, methods=['POST'], authentication_classes=[], permission_classes=[]
	)
	def login(self, request: Request) -> Response:
		data: dict[str, Any] = request.data

		serializer = UserLoginSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		user: User = TelegramBackend().authenticate(
			request, hash=data.pop('hash'), raise_exception=True, **data
		)
		refresh_token: RefreshToken = user_login(request, user)

		response = Response()
		add_jwt_tokens_to_cookies(
			response, str(refresh_token), str(refresh_token.access_token)
		)

		return response

	@action(detail=True, methods=['POST'])
	def logout(self, request: Request, pk: str | None = None) -> Response:
		user_logout(request, get_refresh_token(request))

		response = Response()
		delete_jwt_tokens_from_cookies(response)

		return response

	@action(detail=True, url_path='logout-all', methods=['POST'])
	def logout_all(self, request: Request, pk: str | None = None) -> Response:
		user_logout_all(request, request.user, get_refresh_token(request))  # type: ignore[arg-type]

		response = Response()
		delete_jwt_tokens_from_cookies(response)

		return response

	@action(
		detail=True,
		url_path='token-refresh',
		methods=['POST'],
		authentication_classes=[],
		permission_classes=[],
	)
	def token_refresh(self, request: Request, pk: str | None = None) -> Response:
		try:
			refresh_token: RefreshToken = get_refresh_token(request)
		except PyJWTError:
			raise PermissionDenied()

		if refresh_token.is_blacklisted:
			raise TokenBlacklistedError()

		if not refresh_token.user.is_active:
			raise UserInactiveOrDeletedError()

		response = Response()
		response.set_cookie(
			settings.JWT_ACCESS_TOKEN_COOKIE_NAME,
			str(refresh_token.access_token),
			max_age=settings.JWT_ACCESS_TOKEN_LIFETIME,
			secure=settings.JWT_TOKEN_COOKIE_SECURE,
			httponly=settings.JWT_TOKEN_COOKIE_HTTPONLY,
			samesite=settings.JWT_TOKEN_COOKIE_SAMESITE,
		)

		return response

	def destroy(self, request: Request, pk: str | None = None) -> Response:
		user_logout_all(request, request.user, get_refresh_token(request))  # type: ignore[arg-type]

		response: Response = super().destroy(request, pk=pk)
		delete_jwt_tokens_from_cookies(response)

		return response
