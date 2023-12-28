from celery import shared_task

from .models import User

import time


@shared_task
def update_users_first_name_and_last_name() -> None:
	for user in User.objects.all():
		user.update_first_name()
		user.update_last_name()
		user.save()

		time.sleep(1)