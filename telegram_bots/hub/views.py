from django.db.models.query import QuerySet

from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Command, TelegramBot, User, Variable
from ..permissions import CommandIsFound, TelegramBotIsFound
from .authentication import TokenAuthentication
from .serializers import (
	CommandSerializer,
	TelegramBotSerializer,
	UserSerializer,
	VariableSerializer,
)

from typing import Any


class TelegramBotAPIView(RetrieveUpdateAPIView[TelegramBot]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = TelegramBotSerializer

	def get_object(self) -> TelegramBot:
		return self.kwargs['telegram_bot']


class CommandsAPIView(ListAPIView[Command]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = CommandSerializer

	def get_queryset(self) -> QuerySet[Command]:
		return self.kwargs['telegram_bot'].commands.all()


class CommandAPIView(RetrieveAPIView[Command]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & CommandIsFound]
	serializer_class = CommandSerializer

	def get_object(self) -> Command:
		return self.kwargs['telegram_bot_command']


class VariablesAPIView(ListAPIView[Variable]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = VariableSerializer

	def get_queryset(self) -> QuerySet[Variable]:
		return self.kwargs['telegram_bot'].variables.all()


class UsersAPIView(CreateAPIView[User]):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]
	serializer_class = UserSerializer

	def get_serializer_context(self) -> dict[str, Any]:
		context: dict[str, Any] = super().get_serializer_context()
		context['telegram_bot'] = self.kwargs['telegram_bot']

		return context
