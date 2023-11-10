from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from constructor_telegram_bots.environment import (
	create_user as env_create_user,
	delete_user as env_delete_user,
)

from .models import User

from typing import Any


@receiver(post_save, sender=User)
def post_save_user_signal_handler(instance: User, created: bool, **kwargs: Any) -> None:
	if created:
		Token.objects.create(user=instance)
		env_create_user(user=instance)

@receiver(post_delete, sender=User)
def post_delete_user_signal_handler(instance: User, **kwargs: Any) -> None:
	env_delete_user(user=instance)
