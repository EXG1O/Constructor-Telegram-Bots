from django.db import models
from django.utils.translation import gettext_lazy as _


class InstructionSection(models.Model):
	def position_default() -> int:
		try:
			return InstructionSection.objects.last().position + 1
		except AttributeError:
			return 1

	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	position = models.IntegerField(_('Позиция'), blank=True, default=position_default)

	class Meta:
		db_table = 'instruction_section'
		ordering = ['position']

		verbose_name = _('Раздел')
		verbose_name_plural = _('Разделы')

	def __str__(self) -> str:
		return self.title
