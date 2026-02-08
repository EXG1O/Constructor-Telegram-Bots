from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import FieldError
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from constructor_telegram_bots.fields import PublicURLField

from collections.abc import Iterable
from typing import TYPE_CHECKING
import hashlib
import os
import random
import secrets


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


def upload_media_path(instance: 'AbstractMedia', file_name: str) -> str:
    name, ext = os.path.splitext(file_name)

    salt: str = secrets.token_hex(8)
    hash: str = hashlib.sha256((name + salt).encode()).hexdigest()

    return f'telegram_bots/{name}_{hash}{ext}'


class AbstractMedia(models.Model):
    if TYPE_CHECKING:
        related_name: str
        file: models.FileField

    from_url = PublicURLField(_('Из URL-адреса'), blank=True, null=True)

    class Meta(TypedModelMeta):
        abstract = True

    def save(
        self,
        *,
        force_insert: bool | tuple[ModelBase, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if bool(self.file) is bool(self.from_url):
            raise FieldError(
                "Only one of the fields 'file' or 'from_url' should be specified."
            )

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def get_original_filename(self) -> str | None:
        if not self.file:
            return None

        name, ext = os.path.splitext(os.path.basename(self.file.name))
        return '_'.join(name.split('_')[:-1]) + ext


class AbstractMessageMedia(AbstractMedia):
    position = models.PositiveSmallIntegerField(_('Позиция'))

    class Meta(TypedModelMeta):
        abstract = True
