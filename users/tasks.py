from django.utils import timezone

from celery import shared_task

from .models import User

from datetime import datetime, timedelta
import time


@shared_task
def update_users_first_and_last_name() -> None:
	for user in User.objects.all():
		user.update_first_name()
		user.update_last_name()
		user.save()

		time.sleep(1)


@shared_task
def check_confirm_code_generation_date() -> None:
	one_hour_ahead_date: datetime = timezone.now() + timedelta(hours=1)

	for user in User.objects.filter(
		confirm_code_generation_date__gt=one_hour_ahead_date
	):
		user.confirm_code = None
		user.save()
