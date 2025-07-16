from django.test import TestCase

from rest_framework.test import APIRequestFactory

from users.models import User as SiteUser
from users.tokens import AccessToken, RefreshToken

from ..models import TelegramBot


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.site_user: SiteUser = SiteUser.objects.create(
            telegram_id=123456789, first_name='exg1o'
        )
        self.refresh_token: RefreshToken = RefreshToken.for_user(self.site_user)
        self.access_token: AccessToken = self.refresh_token.access_token
        self.telegram_bot: TelegramBot = self.site_user.telegram_bots.create(
            api_token='Hi!'
        )
