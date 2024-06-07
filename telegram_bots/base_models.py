from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import FieldError
from django.core.files.base import File
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from collections.abc import Iterable
from typing import TYPE_CHECKING, AnyStr


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


class AbstractCommandMedia(models.Model):
	if TYPE_CHECKING:
		related_name: str
		file_field_name: str

	position = models.PositiveSmallIntegerField(_('Позиция'))
	from_url = models.URLField(_('Из URL-адреса'), blank=True, null=True)

	class Meta(TypedModelMeta):
		abstract = True

	@property
	def file_field(self) -> File[AnyStr] | FieldFile | None:
		return getattr(self, self.file_field_name)

	@file_field.setter
	def file_field(self, file: File[AnyStr] | None) -> None:
		setattr(self, self.file_field_name, file)

	def save(
		self,
		force_insert: bool | tuple[ModelBase, ...] = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if bool(self.file_field) is bool(self.from_url):
			raise FieldError(
				f"Only one of the fields '{self.file_field_name}' or 'from_url' "
				'should be specified.'
			)

		super().save(force_insert, force_update, using, update_fields)

	def delete(
		self, using: str | None = None, keep_parents: bool = False
	) -> tuple[int, dict[str, int]]:
		if self.file_field:
			self.file_field.delete(save=False)

		return super().delete(using, keep_parents)


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
