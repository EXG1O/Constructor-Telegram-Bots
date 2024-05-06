from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class Donation(models.Model):
	sum = models.FloatField(_('Сумма'))
	contact_link = models.URLField(_('Контактная ссылка'))
	date = models.DateTimeField(_('Дата'))

	class Meta(TypedModelMeta):
		db_table = 'donation'
		ordering = ['-sum']
		verbose_name = _('Пожертвование')
		verbose_name_plural = _('Пожертвования')

	def __str__(self) -> str:
		return self.contact_link


def section_position_default() -> int:
	section: Section | None = Section.objects.last()
	return section.position + 1 if section else 1


class Section(models.Model):  # type: ignore [django-manager-missing]
	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	position = models.PositiveSmallIntegerField(
		_('Позиция'), blank=True, default=section_position_default
	)

	class Meta(TypedModelMeta):
		ordering = ['position']
		verbose_name = _('Раздел')
		verbose_name_plural = _('Разделы')

	def __str__(self) -> str:
		return self.title


def button_position_default() -> int:
	button: Button | None = Button.objects.last()
	return button.position + 1 if button else 1


class Button(models.Model):  # type: ignore [django-manager-missing]
	text = models.CharField(_('Текст'), max_length=255)
	url = models.URLField(_('Ссылка'))
	position = models.PositiveSmallIntegerField(
		_('Позиция'), blank=True, default=button_position_default
	)

	class Meta(TypedModelMeta):
		ordering = ['position']
		verbose_name = _('Кнопку')
		verbose_name_plural = _('Кнопки')

	def __str__(self) -> str:
		return self.text
