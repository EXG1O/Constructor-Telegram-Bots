from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import TeamMember


def team_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'team.html', {'team_members': TeamMember.objects.all()})
