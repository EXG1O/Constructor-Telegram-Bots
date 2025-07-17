from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from ..models import Variable
from ..views import VariableViewSet
from .mixins import TelegramBotMixin, UserMixin

from contextlib import suppress
from typing import TYPE_CHECKING


class VariableViewSetTests(TelegramBotMixin, UserMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.factory = APIRequestFactory()

        self.variable: Variable = self.telegram_bot.variables.create(
            name='Test name', value='The test value :)', description='The test variable'
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-variable-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-variable-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-variable-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.variable.id},
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-variable-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.variable.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-variable-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = VariableViewSet.as_view({'get': 'list'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.list_true_url)

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get(self.list_false_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.list_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self) -> None:
        view = VariableViewSet.as_view({'post': 'create'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.post(self.list_true_url)

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.post(self.list_false_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.post(self.list_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        old_variable_count: int = self.telegram_bot.variables.count()

        request = self.factory.post(
            self.list_true_url,
            {
                'name': 'Test name',
                'value': 'The test value :)',
                'description': 'The test variable',
            },
        )
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.telegram_bot.variables.count(), old_variable_count + 1)

    def test_retrieve(self) -> None:
        view = VariableViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.variable.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = VariableViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.variable.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.put(self.detail_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_name: str = 'Test name 2'

        request = self.factory.put(
            self.detail_true_url,
            {
                'name': new_name,
                'value': 'The test value :)',
                'description': 'The test variable',
            },
            format='json',
        )
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.variable.refresh_from_db()
        self.assertEqual(self.variable.name, new_name)

    def test_partial_update(self) -> None:
        view = VariableViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.variable.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_name: str = 'Test name 2'

        request = self.factory.patch(
            self.detail_true_url, {'name': new_name}, format='json'
        )
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.variable.refresh_from_db()
        self.assertEqual(self.variable.name, new_name)

    def test_destroy(self) -> None:
        view = VariableViewSet.as_view({'delete': 'destroy'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.delete(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.delete(url)
            force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.variable.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.delete(self.detail_true_url)
        force_authenticate(request, self.user, self.user_access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.variable.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with suppress(Variable.DoesNotExist):
            self.variable.refresh_from_db()
            raise self.failureException('Variable has not been deleted from database!')
