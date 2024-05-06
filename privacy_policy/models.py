from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


def section_default_position() -> int:
	section: Section | None = Section.objects.last()
	return section.position + 1 if section else 1


class Section(models.Model):  # type: ignore [django-manager-missing]
	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	position = models.PositiveSmallIntegerField(
		_('Позиция'), blank=True, default=section_default_position
	)

	class Meta(TypedModelMeta):
		ordering = ['position']
		verbose_name = _('Раздел')
		verbose_name_plural = _('Разделы')

	def __str__(self) -> str:
		return self.title
