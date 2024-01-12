from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Update

from typing import Any


@receiver(post_delete, sender=Update)
def post_delete_team_member_signal_handler(instance: Update, **kwargs: Any) -> None:
	if instance.image:
		instance.image.delete(save=False)