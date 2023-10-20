from django.http import JsonResponse
from django.utils.translation import gettext as _

from rest_framework.status import HTTP_404_NOT_FOUND

from .models import Update

from functools import wraps


def check_update_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		update_id: int = kwargs.pop('update_id', 0)

		try:
			kwargs['update'] = Update.objects.get(id=update_id)
		except Update.DoesNotExist:
			return JsonResponse({
				'message': _('Обновление не найдено!'),
				'level': 'danger',
			}, status=HTTP_404_NOT_FOUND)

		return func(*args, **kwargs)
	return wrapper
