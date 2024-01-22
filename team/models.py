from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model): # type: ignore [django-manager-missing]
	image = models.ImageField(_('Изображение'), upload_to='team/')
	username = models.CharField('@username', max_length=32)
	speciality = models.CharField(_('Специальность'), max_length=255)
	joined_date = models.DateTimeField(_('Присоединился'))

	class Meta:
		db_table = 'team_member'
		ordering = ('joined_date',)

		verbose_name = _('Члена')
		verbose_name_plural = _('Члены')

	def __str__(self) -> str:
		return f'@{self.username}'