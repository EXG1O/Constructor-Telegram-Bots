from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class SectionViewSetTests(TestCase):
	url: str = reverse('api:instruction:section-list')

	def setUp(self) -> None:
		self.client: APIClient = APIClient()

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
