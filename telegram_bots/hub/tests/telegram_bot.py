from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from ...tests.mixins import TelegramBotMixin, UserMixin
from ..views import TelegramBotViewSet
from .mixins import HubMixin
from .utils import assert_view_basic_protected

from typing import TYPE_CHECKING


class TelegramBotViewSetTests(TelegramBotMixin, UserMixin, HubMixin, TestCase):
    list_url: str = reverse('api:telegram-bots-hub:telegram-bot-list')

    def setUp(self) -> None:
        super().setUp()

        self.factory = APIRequestFactory()

        self.detail_true_url: str = reverse(
            'api:telegram-bots-hub:telegram-bot-detail',
            kwargs={'id': self.telegram_bot.id},
        )
        self.detail_false_url: str = reverse(
            'api:telegram-bots-hub:telegram-bot-detail', kwargs={'id': 0}
        )

    def test_list(self) -> None:
        view = TelegramBotViewSet.as_view({'get': 'list'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.list_url)
        assert_view_basic_protected(request, view, self.hub.service_token)

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get(self.list_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self) -> None:
        view = TelegramBotViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)
        assert_view_basic_protected(
            request, view, self.hub.service_token, id=self.telegram_bot.id
        )

        request = self.factory.get(self.detail_false_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(request, id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(request, id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
