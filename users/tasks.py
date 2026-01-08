from django.utils import timezone

from celery import shared_task

from .models import Token, User

from datetime import timedelta


@shared_task
def delete_expired_tokens() -> None:
    Token.objects.filter(expiry_date__lt=timezone.now()).delete()


@shared_task
def delete_users_not_accepted_terms() -> None:
    User.objects.filter(
        accepted_terms=False, joined_date__lt=timezone.now() - timedelta(days=30)
    ).delete()
