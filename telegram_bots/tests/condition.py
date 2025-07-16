from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import force_authenticate

from ..models import Condition
from ..views import ConditionViewSet, DiagramConditionViewSet
from .base import BaseTestCase

from contextlib import suppress
from typing import TYPE_CHECKING


class ConditionViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.condition: Condition = self.telegram_bot.conditions.create(
            name='Test name'
        )
        self.condition.parts.create(
            type='+',
            first_value='first_value',
            operator='==',
            second_value='second_value',
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-condition-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-condition-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-condition-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.condition.id},
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-condition-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.condition.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-condition-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = ConditionViewSet.as_view({'get': 'list'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.list_true_url)

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get(self.list_false_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.list_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self) -> None:
        view = ConditionViewSet.as_view({'post': 'create'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.post(self.list_true_url)

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.post(self.list_false_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.post(self.list_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.post(
            self.list_true_url,
            {
                'name': 'Test name',
                'parts': [
                    {
                        'type': '+',
                        'first_value': 'first_value',
                        'operator': '==',
                        'second_value': 'second_value',
                    }
                ],
            },
            format='json',
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        old_condition_count: int = self.telegram_bot.conditions.count()

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.telegram_bot.conditions.count(), old_condition_count + 1)

    def test_retrieve(self) -> None:
        view = ConditionViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = ConditionViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        new_name: str = 'Test name 2'

        request = self.factory.put(
            self.detail_true_url,
            {
                'name': new_name,
                'parts': [
                    {
                        'type': '+',
                        'first_value': 'first_value',
                        'operator': '==',
                        'second_value': 'second_value',
                    }
                ],
            },
            format='json',
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.condition.refresh_from_db()
        self.assertEqual(self.condition.name, new_name)

    def test_partial_update(self) -> None:
        view = ConditionViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_name: str = 'Test name 2'

        request = self.factory.patch(
            self.detail_true_url, {'name': new_name}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.condition.refresh_from_db()
        self.assertEqual(self.condition.name, new_name)

    def test_destroy(self) -> None:
        view = ConditionViewSet.as_view({'delete': 'destroy'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.delete(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.delete(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.delete(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with suppress(Condition.DoesNotExist):
            self.condition.refresh_from_db()
            raise self.failureException('Condition has not been deleted from database!')


class DiagramConditionViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.condition: Condition = self.telegram_bot.conditions.create(
            name='Test name'
        )
        self.condition.parts.create(
            type='+',
            first_value='first_value',
            operator='==',
            second_value='second_value',
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-condition-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-condition-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-condition-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.condition.id},
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-condition-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.condition.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-condition-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = DiagramConditionViewSet.as_view({'get': 'list'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.list_true_url)

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.get(self.list_false_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.list_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self) -> None:
        view = DiagramConditionViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = DiagramConditionViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.put(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_x: int = 150

        request = self.factory.put(
            self.detail_true_url, {'x': new_x, 'y': 200}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.condition.refresh_from_db()
        self.assertEqual(self.condition.x, new_x)

    def test_partial_update(self) -> None:
        view = DiagramConditionViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.condition.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_x: int = 150

        request = self.factory.patch(self.detail_true_url, {'x': new_x}, format='json')
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.condition.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.condition.refresh_from_db()
        self.assertEqual(self.condition.x, new_x)
