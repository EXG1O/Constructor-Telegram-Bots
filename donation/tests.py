from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()


class DonationsAPIViewTests(CustomTestCase):
	url: str = reverse('api:donation:index')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)


class SectionsAPIViewTests(CustomTestCase):
	url: str = reverse('api:donation:sections')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)


class ButtonsAPIViewTests(CustomTestCase):
	url: str = reverse('api:donation:buttons')

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
