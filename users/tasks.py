from django.utils import timezone

from celery import shared_task

from .models import Token


@shared_task
def check_tokens_expiration_date() -> None:
	Token.objects.filter(expiry_date__lt=timezone.now()).delete()
