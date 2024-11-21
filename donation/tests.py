from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class CustomTestCase(TestCase):
	def setUp(self) -> None:
		self.client: APIClient = APIClient()


class DonationViewSetTests(CustomTestCase):
	url: str = reverse('api:donation:donation-list')

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class SectionViewSetTests(CustomTestCase):
	url: str = reverse('api:donation:section-list')

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class MethodViewSetTests(CustomTestCase):
	url: str = reverse('api:donation:method-list')

	def test_list(self) -> None:
		response: HttpResponse = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
