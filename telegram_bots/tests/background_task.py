from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import force_authenticate

from ..models import BackgroundTask
from ..views import BackgroundTaskViewSet, DiagramBackgroundTaskViewSet
from .base import BaseTestCase

from contextlib import suppress
from typing import TYPE_CHECKING


class BackgroundTaskViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.background_task: BackgroundTask = (
            self.telegram_bot.background_tasks.create(name='Test name', interval=1)
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-background-task-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-background-task-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-background-task-detail',
            kwargs={
                'telegram_bot_id': self.telegram_bot.id,
                'id': self.background_task.id,
            },
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-background-task-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.background_task.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-background-task-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = BackgroundTaskViewSet.as_view({'get': 'list'})

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
        view = BackgroundTaskViewSet.as_view({'post': 'create'})

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
            {'name': 'Test name', 'interval': 1},
            format='json',
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        old_background_task_count: int = self.telegram_bot.background_tasks.count()

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.telegram_bot.background_tasks.count(), old_background_task_count + 1
        )

    def test_retrieve(self) -> None:
        view = BackgroundTaskViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = BackgroundTaskViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        new_name: str = 'Test name 2'

        request = self.factory.put(
            self.detail_true_url, {'name': new_name}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request = self.factory.put(
            self.detail_true_url,
            {'name': new_name, 'interval': 1},
            format='json',
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.background_task.refresh_from_db()
        self.assertEqual(self.background_task.name, new_name)

    def test_partial_update(self) -> None:
        view = BackgroundTaskViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_name: str = 'Test name 2'

        request = self.factory.patch(
            self.detail_true_url, {'name': new_name}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.background_task.refresh_from_db()
        self.assertEqual(self.background_task.name, new_name)

    def test_destroy(self) -> None:
        view = BackgroundTaskViewSet.as_view({'delete': 'destroy'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.delete(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.delete(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.delete(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with suppress(BackgroundTask.DoesNotExist):
            self.background_task.refresh_from_db()
            raise self.failureException(
                'Background task has not been deleted from database!'
            )


class DiagramBackgroundTaskViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.background_task: BackgroundTask = (
            self.telegram_bot.background_tasks.create(name='Test name', interval=1)
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-background-task-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-background-task-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-background-task-detail',
            kwargs={
                'telegram_bot_id': self.telegram_bot.id,
                'id': self.background_task.id,
            },
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-background-task-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.background_task.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-diagram-background-task-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_list(self) -> None:
        view = DiagramBackgroundTaskViewSet.as_view({'get': 'list'})

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
        view = DiagramBackgroundTaskViewSet.as_view({'get': 'retrieve'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.get(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.get(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.get(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self) -> None:
        view = DiagramBackgroundTaskViewSet.as_view({'put': 'update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.put(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.put(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.put(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_x: int = 150

        request = self.factory.put(
            self.detail_true_url, {'x': new_x, 'y': 200}, format='json'
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.background_task.refresh_from_db()
        self.assertEqual(self.background_task.x, new_x)

    def test_partial_update(self) -> None:
        view = DiagramBackgroundTaskViewSet.as_view({'patch': 'partial_update'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.patch(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.patch(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=0, id=self.background_task.id)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.patch(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_x: int = 150

        request = self.factory.patch(self.detail_true_url, {'x': new_x}, format='json')
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.background_task.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.background_task.refresh_from_db()
        self.assertEqual(self.background_task.x, new_x)
