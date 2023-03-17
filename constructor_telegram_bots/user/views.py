from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.contrib.auth import login

from user.models import User

from scripts.decorators import SiteDecorators

import json

@SiteDecorators.get_user_data
def user_auth(request: WSGIRequest, user_id: int, confirm_code: str, data: dict) -> HttpResponse:
	data.update(
		{
			'title': 'Авторизация',
		}
	)
	
	if User.objects.filter(id=user_id).exists():
		user = User.objects.get(id=user_id)

		if user.confirm_code == confirm_code:
			user.confirm_code = None
			user.save()

			login(request=request, user=user)

			data.update(
				{
					'meta': {
						'url': '/personal_cabinet/',
					},
					'content': {
						'heading': 'Успешная авторизация.',
						'text': 'Автоматический переход в личный кабинет через 3 секунды.',
					},
				}
			)
		else:
			data.update(
				{
					'meta': {
						'url': '/',
					},
					'content': {
						'heading': 'Неверный код подтверждения!',
						'text': 'Автоматический переход на главную страницу через 3 секунды.',
					},
				}
			)
	else:
		data.update(
			{
				'meta': {
					'url': '/',
				},
				'content': {
					'heading': 'Не удалось найти пользователя!',
					'text': 'Автоматический переход на главную страницу через 3 секунды.',
				},
			}
		)

	return render(request, 'auth.html', context=data)

@csrf_exempt
@SiteDecorators.is_auth(render_page=False)
def get_user_added_telegram_bots(request: WSGIRequest) -> HttpResponse:
	added_telegram_bots = {}
	for telegram_bot in request.user.telegram_bots.all():
		added_telegram_bots.update(
			{
				telegram_bot.id: {
					'name': telegram_bot.name,
					'is_running': telegram_bot.is_running,
				},
			}
		)
	added_telegram_bots = json.dumps(added_telegram_bots)

	return HttpResponse(added_telegram_bots)