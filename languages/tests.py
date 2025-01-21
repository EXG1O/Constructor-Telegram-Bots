from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class LanguagesAPIViewTests(TestCase):
    url: str = reverse('api:languages:index')

    def setUp(self) -> None:
        self.client: APIClient = APIClient()

    def test_get_method(self) -> None:
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method(self) -> None:
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, {'lang_code': 'ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
