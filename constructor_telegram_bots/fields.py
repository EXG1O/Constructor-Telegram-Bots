from django.db import models

from .validators import PublicURLValidator

from typing import TypeVar

_ST = TypeVar('_ST', contravariant=True)
_GT = TypeVar('_GT', covariant=True)


class PublicURLField(models.URLField[_ST, _GT]):
    default_validators = [PublicURLValidator()]
