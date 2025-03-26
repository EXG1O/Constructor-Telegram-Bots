from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.fields import PublicURLField


class Donation(models.Model):
    sum = models.FloatField(_('Сумма'))
    sender = models.CharField(_('Отправитель'), max_length=64)
    date = models.DateField(_('Дата'))

    class Meta(TypedModelMeta):
        db_table = 'donation'
        ordering = ['-sum']
        verbose_name = _('Пожертвование')
        verbose_name_plural = _('Пожертвования')

    def __str__(self) -> str:
        return self.sender


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


class Method(models.Model):
    text = models.CharField(_('Текст'), max_length=128)
    link = PublicURLField(_('Ссылка'), blank=True, null=True)
    value = models.CharField(_('Значение'), max_length=255, blank=True, null=True)
    position = models.PositiveSmallIntegerField(_('Позиция'), blank=True)

    class Meta(TypedModelMeta):
        ordering = ['position']
        verbose_name = _('Метод поддержки')
        verbose_name_plural = _('Методы поддержки')

    def __str__(self) -> str:
        return self.text
