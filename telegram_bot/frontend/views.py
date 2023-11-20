from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from telegram_bot.decorators import check_telegram_bot_id


class CustomTemplateView(TemplateView):
	@method_decorator(login_required)
	@check_telegram_bot_id
	def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
		return super().get(request, *args, **kwargs)
