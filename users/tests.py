from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import User


class StatsAPIViewTests(TestCase):
	url: str = reverse('api:users:stats')

	def setUp(self) -> None:
		self.client: APIClient = APIClient()

	def test_get_method(self) -> None:
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')
		self.token: Token = Token.objects.create(user=self.user)


class UserAPIViewTests(CustomTestCase):
	url: str = reverse('api:users:detail:index')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)

	def test_delete_method(self) -> None:
		response: HttpResponse = self.client.delete(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.delete(self.url)
		self.assertEqual(response.status_code, 200)

		try:
			self.user.refresh_from_db()
			raise self.failureException('User has not been deleted from database!')
		except User.DoesNotExist:
			pass


class UserLoginAPIViewTests(CustomTestCase):
	url: str = reverse('api:users:detail:login')

	def setUp(self) -> None:
		super().setUp()

		self.user.confirm_code = 'Do you love Python?'
		self.user.save()

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			self.url, {'user_id': 0, 'confirm_code': self.user.confirm_code}
		)
		self.assertEqual(response.status_code, 404)

		response = self.client.post(
			self.url, {'user_id': self.user.id, 'confirm_code': 'Yes, I love Python <3'}
		)
		self.assertEqual(response.status_code, 403)

		response = self.client.post(
			self.url, {'user_id': self.user.id, 'confirm_code': self.user.confirm_code}
		)
		self.assertEqual(response.status_code, 200)

		self.user.refresh_from_db()

		self.assertTrue(self.user.last_login)


class UserLogoutAPIViewTests(CustomTestCase):
	url: str = reverse('api:users:detail:logout')

	def test_post_method(self) -> None:
		response: HttpResponse = self.client.post(self.url)
		self.assertEqual(response.status_code, 401)

		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		response = self.client.post(self.url)
		self.assertEqual(response.status_code, 200)
