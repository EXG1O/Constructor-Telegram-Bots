from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from .models import User
from .tokens import AccessToken, RefreshToken
from .views import UserViewSet

from contextlib import suppress
from importlib import import_module
from typing import TYPE_CHECKING, Any
import hashlib
import hmac
import time

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class StatsAPIViewTests(TestCase):
	url: str = reverse('api:users:stats')

	def setUp(self) -> None:
		self.client: APIClient = APIClient()

	def test_get_method(self) -> None:
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTests(TestCase):
	def setUp(self) -> None:
		self.factory = APIRequestFactory()
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
		self.refresh_token: RefreshToken = RefreshToken.for_user(self.user)
		self.access_token: AccessToken = self.refresh_token.access_token

	def emulate_auth_user_request(self, request: Request) -> None:
		request.session = SessionStore()

		request.COOKIES[settings.JWT_REFRESH_TOKEN_COOKIE_NAME] = str(
			self.refresh_token
		)
		request.COOKIES[settings.JWT_ACCESS_TOKEN_COOKIE_NAME] = str(self.access_token)

		force_authenticate(request, self.user, self.access_token)  # type: ignore [arg-type]

	def test_retrieve(self) -> None:
		view = UserViewSet.as_view({'get': 'retrieve'})

		request: Request = self.factory.get(reverse('api:users:user-detail'))

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		force_authenticate(request, self.user, self.access_token)  # type: ignore [arg-type]

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_login(self) -> None:
		view = UserViewSet.as_view({'post': 'login'})

		data: dict[str, Any] = {
			'id': self.user.telegram_id,
			'first_name': self.user.first_name,
			'auth_date': int(time.time()),
		}

		secret_key: bytes = hashlib.sha256(
			settings.TELEGRAM_BOT_TOKEN.encode()
		).digest()
		data_check_string: str = '\n'.join(
			[f'{key}={data[key]}' for key in sorted(data.keys())]
		)
		data['hash'] = hmac.new(
			secret_key, data_check_string.encode(), hashlib.sha256
		).hexdigest()

		request: Request = self.factory.post(
			reverse('api:users:user-login'), data=data, format='json'
		)
		request.session = SessionStore()

		# FIXME: I don't know why, but `APIRequestFactory` doesn't see that...
		# `permission_classes` and `permission_classes` are set to empty for this action.
		force_authenticate(request, self.user, None)

		response: Response = view(request)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(
			response.cookies.get(settings.JWT_REFRESH_TOKEN_COOKIE_NAME)
		)
		self.assertIsNotNone(
			response.cookies.get(settings.JWT_ACCESS_TOKEN_COOKIE_NAME)
		)

	def test_logout(self) -> None:
		view = UserViewSet.as_view({'post': 'logout'})

		request: Request = self.factory.post(reverse('api:users:user-logout'))

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		self.emulate_auth_user_request(request)

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(self.refresh_token.is_blacklisted)

	def test_logout_all(self) -> None:
		view = UserViewSet.as_view({'post': 'logout_all'})

		request: Request = self.factory.post(reverse('api:users:user-logout-all'))

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		self.emulate_auth_user_request(request)

		second_refresh_token: RefreshToken = RefreshToken.for_user(self.user)

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(self.refresh_token.is_blacklisted)
		self.assertTrue(second_refresh_token.is_blacklisted)

	def test_token_refresh(self) -> None:
		view = UserViewSet.as_view({'post': 'token_refresh'})

		request: Request = self.factory.post(reverse('api:users:user-token-refresh'))

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		self.emulate_auth_user_request(request)

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(
			response.cookies.get(settings.JWT_ACCESS_TOKEN_COOKIE_NAME),
			str(self.access_token),
		)

	def test_destroy(self) -> None:
		view = UserViewSet.as_view({'delete': 'destroy'})

		request: Request = self.factory.delete(reverse('api:users:user-detail'))

		if TYPE_CHECKING:
			response: Response

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

		self.emulate_auth_user_request(request)

		second_refresh_token: RefreshToken = RefreshToken.for_user(self.user)

		response = view(request)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		with suppress(User.DoesNotExist):
			self.user.refresh_from_db()
			raise self.failureException('User has not been deleted from database!')

		self.assertTrue(self.refresh_token.is_blacklisted)
		self.assertTrue(second_refresh_token.is_blacklisted)
