from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import InstructionSection


def index_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'instruction/index.html', {'instruction_sections': InstructionSection.objects.all()})
