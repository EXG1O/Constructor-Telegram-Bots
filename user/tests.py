from django.test import TestCase
from django import urls
from django.conf import settings

from .models import User


class BaseTestCase(TestCase):
	def setUp(self) -> None:
		self.user: User = User.objects.create(telegram_id=123456789, first_name='exg1o')

class UserModelTests(BaseTestCase):
	def test_fields(self) -> None:
		self.assertEqual(self.user.telegram_id, 123456789)
		self.assertEqual(self.user.first_name, 'exg1o')
		self.assertFalse(self.user.is_superuser)
		self.assertFalse(self.user.is_staff)
		self.assertIsNone(self.user.confirm_code)
		self.assertIsNone(self.user.last_login)

	def test_login_url(self) -> None:
		self.user.generate_confirm_code()

		self.assertEqual(
			self.user.login_url,
			settings.SITE_DOMAIN + urls.reverse('user:login', kwargs={
				'user_id': self.user.id,
				'confirm_code': self.user.confirm_code,
			})
		)
		self.assertIsNotNone(self.user.confirm_code)
		self.assertIsNone(self.user.last_login)

		self.client.get(self.user.login_url)
		self.user.refresh_from_db()

		self.assertIsNone(self.user.confirm_code)
		self.assertIsNotNone(self.user.last_login)