from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import DonationSection, DonationButton


def donation_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation.html', {
		'donation_sections': DonationSection.objects.all(),
		'donation_buttons': DonationButton.objects.all(),
	})

def donation_completed_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation_completed.html')
