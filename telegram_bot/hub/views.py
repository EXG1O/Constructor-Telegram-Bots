from django.db.models.query import QuerySet

from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .authentication import TokenAuthentication
from ..permissions import (
	TelegramBotIsFound,
	TelegramBotCommandIsFound,
)
from ..models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotVariable,
	TelegramBotUser,
)
from .serializers import (
	TelegramBotSerializer,
	TelegramBotCommandSerializer,
	TelegramBotVariableSerializer,
	TelegramBotUserSerializer,
)

from typing import Any


class TelegramBotAPIView(RetrieveUpdateAPIView[TelegramBot]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotSerializer

	def get_object(self) -> TelegramBot:
		return self.kwargs['telegram_bot']

class TelegramBotCommandsAPIView(ListAPIView[TelegramBotCommand]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotCommandSerializer

	def get_queryset(self) -> QuerySet[TelegramBotCommand]:
		return self.kwargs['telegram_bot'].commands.all()

class TelegramBotCommandAPIView(RetrieveAPIView[TelegramBotCommand]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]
	serializer_class = TelegramBotCommandSerializer

	def get_object(self) -> TelegramBotCommand:
		return self.kwargs['telegram_bot_command']

class TelegramBotVariablesAPIView(ListAPIView[TelegramBotVariable]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotVariableSerializer

	def get_queryset(self) -> QuerySet[TelegramBotVariable]:
		return self.kwargs['telegram_bot'].variables.all()

class TelegramBotUsersAPIView(CreateAPIView[TelegramBotUser]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotUserSerializer

	def get_serializer_context(self) -> dict[str, Any]:
		context: dict[str, Any] = super().get_serializer_context()
		context['telegram_bot'] = self.kwargs['telegram_bot']

		return context