from django.db.models.signals import post_delete

from .models import InvoiceImage, MessageDocument, MessageImage
from .models.base import AbstractMedia

from typing import Any


def delete_media_file(
    sender: type[AbstractMedia], instance: AbstractMedia, **kwargs: Any
) -> None:
    if instance.file:
        instance.file.delete(save=False)


def connect() -> None:
    post_delete.connect(delete_media_file, sender=MessageImage)
    post_delete.connect(delete_media_file, sender=MessageDocument)
    post_delete.connect(delete_media_file, sender=InvoiceImage)
