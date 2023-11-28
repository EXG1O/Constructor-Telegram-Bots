from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def index_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'personal_cabinet/index/main.html')
