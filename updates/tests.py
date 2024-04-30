from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class UpdatesAPIViewTests(TestCase):
	url: str = reverse('api:updates:update-list')

	def setUp(self) -> None:
		self.client: APIClient = APIClient()

	def test_get_method(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
