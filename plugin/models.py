from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User
from telegram_bot.models import TelegramBot


class Plugin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='plugins', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)
	code = models.TextField(_('Код'))
	is_checked = models.BooleanField(_('Проверен'), default=False)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	class Meta:
		db_table = 'plugin'

		verbose_name = _('Плагин')
		verbose_name_plural = _('Плагины')

	def __str__(self) -> str:
		return self.name

class PluginLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, verbose_name=_('Telegram бот'))
	plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE, related_name='logs', verbose_name=_('Плагин'))
	message = models.TextField(_('Сообщение'))
	level = models.CharField(_('Уровень'), max_length=7, choices=(
		('info', _('Информация')),
		('success', _('Успех')),
		('danger', _('Ошибка'))
	), default='info')
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	class Meta:
		db_table = 'plugin_log'

		verbose_name = _('Логи')
		verbose_name_plural = _('Логи')

	def __str__(self) -> str:
		return self.plugin.name
