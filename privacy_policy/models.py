from django.db import models
from django.utils.translation import gettext_lazy as _


def privacy_policy_section_position_default() -> int:
	try:
		return PrivacyPolicySection.objects.last().position + 1
	except AttributeError:
		return 1

class PrivacyPolicySection(models.Model):
	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	position = models.IntegerField(_('Позиция'), blank=True, default=privacy_policy_section_position_default)
	last_update_date = models.DateTimeField(_('Дата последнего обновления'), auto_now=True)

	class Meta:
		db_table = 'privacy_policy_section'
		ordering = ('position',)

		verbose_name = _('Раздел')
		verbose_name_plural = _('Разделы')

	def __str__(self) -> str:
		return self.title