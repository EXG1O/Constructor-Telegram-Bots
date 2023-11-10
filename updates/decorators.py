from django.http import HttpRequest
from django.utils.translation import gettext as _

from constructor_telegram_bots.utils.shortcuts import render_success_or_error

from .models import Update

from functools import wraps


def check_update_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: HttpRequest = args[0]
		update_id: int = kwargs.pop('update_id', 0)

		try:
			kwargs['update'] = Update.objects.get(id=update_id)
		except Update.DoesNotExist:
			return render_success_or_error(
				request,
				'Обновление не найдено!',
				_('Автоматический переход на главную страницу через 3 секунды.'),
				status=404,
			)

		return func(*args, **kwargs)
	return wrapper
