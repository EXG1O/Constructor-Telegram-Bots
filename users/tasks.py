from django.utils import timezone

from celery import shared_task

from .models import Token

# FIXME: In 30 days after the release of v3.1.0, the code for automating the removal ...
# of users who have not accepted the Terms of Service within 30 days needs to be uncommented.

# from .models import User

# from datetime import timedelta


# @shared_task
# def delete_users_not_accepted_terms() -> None:
#     User.objects.filter(
#         accepted_terms=False, joined_date__lt=timezone.now() - timedelta(days=30)
#     ).delete()


@shared_task
def check_tokens_expiration_date() -> None:
    Token.objects.filter(expiry_date__lt=timezone.now()).delete()
