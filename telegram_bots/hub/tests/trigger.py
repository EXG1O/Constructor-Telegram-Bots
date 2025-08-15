from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from ...tests.mixins import TelegramBotMixin, TriggerMixin, UserMixin
from ..views import TriggerViewSet
from .mixins import HubMixin
from .utils import assert_view_basic_protected

from typing import TYPE_CHECKING


class TriggerViewSetTests(
    TriggerMixin, TelegramBotMixin, UserMixin, HubMixin, TestCase
):
    def setUp(self) -> None:
        super().setUp()

        self.factory = APIRequestFactory()

        self.list_true_url: str = reverse(
            'api:telegram-bots-hub:telegram-bot-trigger-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots-hub:telegram-bot-trigger-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots-hub:telegram-bot-trigger-detail',
            kwargs={
                'telegram_bot_id': self.telegram_bot.id,
                'id': self.trigger.id,
            },
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots-hub:telegram-bot-trigger-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.trigger.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots-hub:telegram-bot-trigger-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = TriggerViewSet.as_view({'get': 'list'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.list_true_url)
        assert_view_basic_protected(
            request, view, self.hub.service_token, telegram_bot_id=self.telegram_bot.id
        )

        request = self.factory.get(self.list_false_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.list_true_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self) -> None:
        view = TriggerViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)
        assert_view_basic_protected(
            request,
            view,
            self.hub.service_token,
            telegram_bot_id=self.telegram_bot.id,
            id=self.trigger.id,
        )

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.trigger.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.hub, self.hub.service_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.trigger.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
