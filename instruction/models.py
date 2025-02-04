from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class Section(models.Model):  # type: ignore [django-manager-missing]
    title = models.CharField(_('Заголовок'), max_length=255)
    text = models.TextField(_('Текст'))
    position = models.PositiveSmallIntegerField(_('Позиция'), blank=True)

    class Meta(TypedModelMeta):
        ordering = ['position']
        verbose_name = _('Раздел')
        verbose_name_plural = _('Разделы')

    def __str__(self) -> str:
        return self.title
