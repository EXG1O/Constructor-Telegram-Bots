from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Update
from .decorators import check_update_id


def updates_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'updates.html', {'updates': Update.objects.all()})

@check_update_id
def update_view(request: HttpRequest, **context) -> HttpResponse:
	return render(request, 'update.html', context)
