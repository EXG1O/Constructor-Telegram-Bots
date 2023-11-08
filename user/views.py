from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext as _
from django import urls
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import User


def user_login_view(request: HttpRequest, user_id: int, confirm_code: str) -> HttpResponse:
	context = {
		'title': _('Ошибка авторизации'),
		'meta': {'refresh': {'url': urls.reverse('home')}},
		'content': {'text': _('Автоматический переход на главную страницу через 3 секунды.')},
	}

	try:
		user: User = User.objects.get(id=user_id)
	except User.DoesNotExist:
		context['content']['heading'] = _('Не удалось найти пользователя!')

		return render(request, 'base_success_or_error.html', context, status=404)

	if user.confirm_code != confirm_code:
		context['content']['heading'] = _('Неверный код подтверждения!')

		return render(request, 'base_success_or_error.html', context, status=401)

	user.confirm_code = None
	user.save()

	login(request, user)

	return redirect('personal_cabinet')

@login_required
def user_logout_view(request: HttpRequest) -> HttpResponse:
	logout(request)

	return render(request, 'base_success_or_error.html', {
		'title': _('Выход из аккаунта'),
		'meta': {'refresh': {'url': urls.reverse('home')}},
		'content': {
			'heading': _('Успешный выход из аккаунта'),
			'text': _('Автоматический переход на главную страницу через 3 секунды.'),
		},
	})
