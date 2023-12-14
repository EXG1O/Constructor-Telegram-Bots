from django.utils.translation import gettext as _

from constructor_telegram_bots.utils.drf import CustomResponse

from .models import Plugin

from functools import wraps


def check_plugin_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		plugin_id: int = kwargs.pop('plugin_id', 0)

		try:
			kwargs['plugin'] = Plugin.objects.get(id=plugin_id)
		except Plugin.DoesNotExist:
			return CustomResponse(_('Плагин не найден!'), status=404)

		return func(*args, **kwargs)
	return wrapper