from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import TeamMember

from typing import Any


@receiver(post_delete, sender=TeamMember)
def post_delete_team_member_signal_handler(instance: TeamMember, **kwargs: Any) -> None:
	instance.image.delete(save=False)
