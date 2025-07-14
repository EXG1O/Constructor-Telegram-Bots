from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.fields import PublicURLField

from collections.abc import Iterable
from typing import TYPE_CHECKING
import random


def generate_random_coordinate() -> int:
    return random.randint(-150, 150)


class AbstractBlock(models.Model):
    name = models.CharField(_('Название'), max_length=128)
    x = models.FloatField(_('Координата X'), default=generate_random_coordinate)
    y = models.FloatField(_('Координата Y'), default=generate_random_coordinate)
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
        file: models.FileField

    from_url = PublicURLField(_('Из URL-адреса'), blank=True, null=True)
    position = models.PositiveSmallIntegerField(_('Позиция'))

    class Meta(TypedModelMeta):
        abstract = True

    def save(
        self,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if bool(self.file) is bool(self.from_url):
            raise FieldError(
                "Only one of the fields 'file' or 'from_url' should be specified."
            )

        super().save(force_insert, force_update, using, update_fields)

    def delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        if self.file:
            self.file.delete(save=False)

        return super().delete(using, keep_parents)
