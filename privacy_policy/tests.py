from django.test import TestCase
from django.http import HttpResponse
from django import urls


class PrivacyPolicyViewsTests(TestCase):
	def test_privacy_policy_view(self) -> None:
		url: str = urls.reverse('privacy_policy')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'privacy_policy.html')
