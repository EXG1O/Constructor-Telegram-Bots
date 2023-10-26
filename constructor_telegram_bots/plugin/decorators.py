from django.utils.translation import gettext as _

from rest_framework.response import Response

from .models import Plugin

from functools import wraps


def check_plugin_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		plugin_id: int = kwargs.pop('plugin_id', 0)

		try:
			kwargs['plugin'] = Plugin.objects.get(id=plugin_id)
		except Plugin.DoesNotExist:
			return Response({
				'message': _('Плагин не найден!'),
				'level': 'danger',
			}, status=404)

		return func(*args, **kwargs)
	return wrapper
