from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class AbstractBlock(models.Model):
	name = models.CharField(_('Название'), max_length=128)
	x = models.FloatField(_('Координата X'), default=0)
	y = models.FloatField(_('Координата Y'), default=0)
	source_connections = GenericRelation(
		'Connection', 'source_object_id', 'source_content_type'
	)
	target_connections = GenericRelation(
		'Connection', 'target_object_id', 'target_content_type'
	)

	class Meta(TypedModelMeta):
		abstract = True

	def __str__(self) -> str:
		return self.name


class AbstractAPIRequest(models.Model):
	METHOD_CHOICES = [
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	]

	url = models.URLField(_('URL-адрес'))
	method = models.CharField(
		_('Метод'), max_length=6, choices=METHOD_CHOICES, default='get'
	)
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	body = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta(TypedModelMeta):
		abstract = True

	def __str__(self) -> str:
		return self.url


class AbstractDatabaseRecord(models.Model):
	data = models.JSONField(_('Данные'))

	class Meta(TypedModelMeta):
		abstract = True
