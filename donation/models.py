from django.db import models
from django.utils.translation import gettext_lazy as _


class Donation(models.Model):
	sum = models.FloatField(_('Сумма'))
	telegram_url = models.CharField(_('Ссылка на Telegram'), max_length=255)
	date = models.DateTimeField(_('Дата'))

	class Meta:
		db_table = 'donation'
		ordering = ('-sum',)

		verbose_name = _('Пожертвование')
		verbose_name_plural = _('Пожертвования')

	def __str__(self) -> str:
		return self.telegram_url

def donation_section_position_default() -> int:
	try:
		return DonationSection.objects.last().position + 1 # type: ignore [operator, union-attr]
	except AttributeError:
		return 1

class DonationSection(models.Model): # type: ignore [django-manager-missing]
	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	position = models.IntegerField(_('Позиция'), blank=True, default=donation_section_position_default)

	class Meta:
		db_table = 'donation_section'
		ordering = ('position',)

		verbose_name = _('Раздел')
		verbose_name_plural = _('Разделы')

	def __str__(self) -> str:
		return self.title

def donation_button_position_default() -> int:
	try:
		return DonationButton.objects.last().position + 1 # type: ignore [operator, union-attr]
	except AttributeError:
		return 1

class DonationButton(models.Model): # type: ignore [django-manager-missing]
	text = models.CharField(_('Текст'), max_length=255)
	url = models.URLField(_('Ссылка'))
	position = models.IntegerField(_('Позиция'), blank=True, default=donation_button_position_default)

	class Meta:
		db_table = 'donation_button'
		ordering = ('position',)

		verbose_name = _('Кнопку')
		verbose_name_plural = _('Кнопки')

	def __str__(self) -> str:
		return self.text