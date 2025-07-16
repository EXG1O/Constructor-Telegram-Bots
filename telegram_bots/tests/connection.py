from django.urls import reverse

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import force_authenticate

from ..enums import ConnectionHandlePosition
from ..models import Command, CommandKeyboard, CommandKeyboardButton, Connection
from ..views import ConnectionViewSet
from .base import BaseTestCase

from contextlib import suppress
from typing import TYPE_CHECKING


class ConnectionViewSetTests(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.command_1: Command = self.telegram_bot.commands.create(name='Test name 1')

        self.command_2: Command = self.telegram_bot.commands.create(name='Test name 2')
        self.command_2_keyboard: CommandKeyboard = CommandKeyboard.objects.create(
            command=self.command_2, type='default'
        )
        self.command_2_keyboard_button: CommandKeyboardButton = (
            self.command_2_keyboard.buttons.create(row=0, position=0, text='Button')
        )

        self.connection: Connection = self.telegram_bot.connections.create(
            source_object=self.command_2_keyboard_button, target_object=self.command_1
        )

        self.list_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-connection-list',
            kwargs={'telegram_bot_id': self.telegram_bot.id},
        )
        self.list_false_url: str = reverse(
            'api:telegram-bots:telegram-bot-connection-list',
            kwargs={'telegram_bot_id': 0},
        )
        self.detail_true_url: str = reverse(
            'api:telegram-bots:telegram-bot-connection-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': self.connection.id},
        )
        self.detail_false_url_1: str = reverse(
            'api:telegram-bots:telegram-bot-connection-detail',
            kwargs={'telegram_bot_id': 0, 'id': self.connection.id},
        )
        self.detail_false_url_2: str = reverse(
            'api:telegram-bots:telegram-bot-connection-detail',
            kwargs={'telegram_bot_id': self.telegram_bot.id, 'id': 0},
        )

    def test_create(self) -> None:
        view = ConnectionViewSet.as_view({'post': 'create'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.post(
            self.list_true_url, telegram_bot_id=self.telegram_bot.id
        )

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = self.factory.post(self.list_false_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(request, telegram_bot_id=0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.post(
            self.list_true_url,
            {
                'source_object_type': 'command_keyboard_button',
                'source_object_id': self.command_2_keyboard_button.id,
                'source_handle_position': ConnectionHandlePosition.RIGHT,
                'target_object_type': 'command',
                'target_object_id': self.command_1.id,
                'target_handle_position': ConnectionHandlePosition.LEFT,
            },
            format='json',
        )
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        old_command_1_target_connection_count: int = (
            self.command_1.target_connections.count()
        )
        old_command_2_keyboard_button_source_connection_count: int = (
            self.command_2_keyboard_button.source_connections.count()
        )

        response = view(request, telegram_bot_id=self.telegram_bot.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.command_1.target_connections.count(),
            old_command_1_target_connection_count + 1,
        )
        self.assertEqual(
            self.command_2_keyboard_button.source_connections.count(),
            old_command_2_keyboard_button_source_connection_count + 1,
        )

    def test_destroy(self) -> None:
        view = ConnectionViewSet.as_view({'delete': 'destroy'})

        if TYPE_CHECKING:
            request: Request
            response: Response

        request = self.factory.delete(self.detail_true_url)

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.connection.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        for url in [self.detail_false_url_1, self.detail_false_url_2]:
            request = self.factory.delete(url)
            force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

            response = view(request, telegram_bot_id=self.telegram_bot.id, id=0)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        request = self.factory.delete(self.detail_true_url)
        force_authenticate(request, self.site_user, self.access_token)  # type: ignore [arg-type]

        response = view(
            request, telegram_bot_id=self.telegram_bot.id, id=self.connection.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with suppress(Connection.DoesNotExist):
            self.connection.refresh_from_db()
            raise self.failureException(
                'Connection has not been deleted from database!'
            )
