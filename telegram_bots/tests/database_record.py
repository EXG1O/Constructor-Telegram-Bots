from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import force_authenticate

from ..models import DatabaseRecord
from ..views import DatabaseRecordViewSet
from .base import BaseTestCase

from contextlib import suppress
from typing import TYPE_CHECKING, Any


class DatabaseRecordViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.database_record = self.telegram_bot.database_records.create(
            data={'key': 'value'}
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-database-record-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-database-record-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-database-record-detail',
            kwargs={
                'telegram_bot_id': self.telegram_bot.id,
                'id': self.database_record.id,
            },
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-database-record-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.database_record.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-database-record-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = DatabaseRecordViewSet.as_view({'get': 'list'})

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
        view = DatabaseRecordViewSet.as_view({'post': 'create'})

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

        old_database_record_count: int = self.telegram_bot.database_records.count()

        request = self.factory.post(
            self.list_true_url, {'data': {'key': 'value'}}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.telegram_bot.database_records.count(), old_database_record_count + 1
        )

    def test_retrieve(self) -> None:
        view = DatabaseRecordViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.database_record.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = DatabaseRecordViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.database_record.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.put(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        new_data: dict[str, Any] = {'new_key': 'new_value'}

        request = self.factory.put(
            self.detail_true_url, {'data': new_data}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.database_record.refresh_from_db()
        self.assertEqual(
            self.telegram_bot.database_records.get(data__contains=new_data).id,
            self.database_record.id,
        )

    def test_partial_update(self) -> None:
        view = DatabaseRecordViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.database_record.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_data: dict[str, Any] = {'new_key': 'new_value'}

        request = self.factory.patch(
            self.detail_true_url, {'data': new_data}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.database_record.refresh_from_db()
        self.assertEqual(
            self.telegram_bot.database_records.get(data__contains=new_data).id,
            self.database_record.id,
        )

    def test_destroy(self) -> None:
        view = DatabaseRecordViewSet.as_view({'delete': 'destroy'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.delete(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.delete(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.database_record.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.delete(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.database_record.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with suppress(DatabaseRecord.DoesNotExist):
            self.database_record.refresh_from_db()
            raise self.failureException(
                'Database record has not been deleted from database!'
            )
