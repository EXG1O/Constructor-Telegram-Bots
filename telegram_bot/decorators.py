from django.http import HttpRequest
from django.utils.translation import gettext as _

from rest_framework.request import Request

from constructor_telegram_bots.utils.drf import CustomResponse
from constructor_telegram_bots.utils.shortcuts import render_success_or_error

from .models import TelegramBot

from functools import wraps


def check_telegram_bot_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: HttpRequest | Request = args[-1]
		telegram_bot_id: int = kwargs.pop('telegram_bot_id', 0)

		try:
			kwargs['telegram_bot'] = request.user.telegram_bots.get(id=telegram_bot_id)
		except TelegramBot.DoesNotExist:
			status = 404

			if isinstance(request, HttpRequest):
				return render_success_or_error(
					request,
					'Telegram бот не найден!',
					_('Автоматический переход на главную страницу через 3 секунды.'),
					status=404,
				)
			else:
				return CustomResponse(_('Telegram бот не найден!'), status=status)

		return func(*args, **kwargs)
	return wrapper
