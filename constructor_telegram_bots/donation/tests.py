from django.test import TestCase
from django.http import HttpResponse
from django import urls

from .models import Donation, DonationSection, DonationButton

from datetime import datetime


class DonationModelTests(TestCase):
	def setUp(self) -> None:
		self.current_date: datetime = datetime.now()
		self.donation: Donation = Donation.objects.create(
			sum=50.00,
			telegram_url='https://example.com/',
			date=self.current_date,
		)

	def test_fields(self) -> None:
		self.assertEqual(self.donation.sum, 50.00)
		self.assertEqual(self.donation.telegram_url, 'https://example.com/')
		self.assertEqual(self.donation.date, self.current_date)

class DonationSectionModelTests(TestCase):
	def setUp(self) -> None:
		self.donation_section: DonationSection = DonationSection.objects.create(
			title='Test',
			text='Test...',
		)

	def test_fields(self) -> None:
		self.assertEqual(self.donation_section.title, 'Test')
		self.assertEqual(self.donation_section.text, 'Test...')
		self.assertEqual(self.donation_section.position, 1)

class DonationButtonModelTests(TestCase):
	def setUp(self) -> None:
		self.donation_button: DonationButton = DonationButton.objects.create(
			text='Test',
			url='https://example.com/',
		)

	def test_fields(self) -> None:
		self.assertEqual(self.donation_button.text, 'Test')
		self.assertEqual(self.donation_button.url, 'https://example.com/')
		self.assertEqual(self.donation_button.position, 1)

class ViewsTests(TestCase):
	def test_donation_view(self) -> None:
		url: str = urls.reverse('donation')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation.html')

	def test_donation_completed_view(self) -> None:
		url: str = urls.reverse('donation_completed')

		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation_completed.html')
