from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import DonationSection, DonationButton


def index_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation/index.html', {
		'donation_sections': DonationSection.objects.all(),
		'donation_buttons': DonationButton.objects.all(),
	})

def completed_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation/completed.html')
