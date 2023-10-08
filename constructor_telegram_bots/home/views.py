from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from donation.models import Donation


def home_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'home.html', {'donations': Donation.objects.all()})
