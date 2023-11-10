from django.http import HttpRequest, HttpResponse
from django import urls
from django.utils.translation import gettext as _
from django.shortcuts import render

from rest_framework.status import is_success


def render_success_or_error(
	request: HttpRequest,
	heading: str,
	text: str,
	redirect_to_url: str | None = None,
	status: int = 200,
) -> HttpResponse:
	if redirect_to_url is None:
		redirect_to_url = urls.reverse('home')

	if is_success(status):
		title = _('Успех')
	else:
		title = _('Ошибка')

	return render(request, 'base_success_or_error.html', {
		'title': title,
		'meta': {'refresh': {'url': redirect_to_url}},
		'content': {'heading': heading, 'text': text},
	}, status=status)
