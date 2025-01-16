from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class Update(models.Model):  # type: ignore [django-manager-missing]
	version = models.CharField(_('Версия'), max_length=255)
	description = models.TextField(_('Описание'))
	added_date = models.DateTimeField(_('Добавлено'), auto_now_add=True)

	class Meta(TypedModelMeta):
		db_table = 'update'
		ordering = ['-added_date']
		verbose_name = _('Обновление')
		verbose_name_plural = _('Обновления')

	def __str__(self) -> str:
		return self.version
