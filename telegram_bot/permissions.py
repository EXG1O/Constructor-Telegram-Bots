from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotVariable,
	TelegramBotUser,
)


class TelegramBotIsFound(BasePermission):
	message = _('Telegram бот не найден!')

	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot_id: int = view.kwargs.pop('telegram_bot_id', 0)

		try:
			setattr(request, 'telegram_bot', request.user.telegram_bots.get(id=telegram_bot_id)) # type: ignore [union-attr]
		except TelegramBot.DoesNotExist:
			return False

		return True

class TelegramBotCommandIsFound(BasePermission):
	message = _('Команда Telegram бота не найдена!')

	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot | None = getattr(request, 'telegram_bot', None)

		if not telegram_bot:
			return False

		telegram_bot_command_id: int = view.kwargs.pop('telegram_bot_command_id', 0)

		try:
			setattr(request, 'telegram_bot_command', telegram_bot.commands.get(id=telegram_bot_command_id))
		except TelegramBotCommand.DoesNotExist:
			return False

		return True

class TelegramBotVariableIsFound(BasePermission):
	message = _('Переменная Telegram бота не найдена!')

	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot | None = getattr(request, 'telegram_bot', None)

		if not telegram_bot:
			return False

		telegram_bot_variable_id: int = view.kwargs.pop('telegram_bot_variable_id', 0)

		try:
			setattr(request, 'telegram_bot_variable', telegram_bot.variables.get(id=telegram_bot_variable_id))
		except TelegramBotVariable.DoesNotExist:
			return False

		return True

class TelegramBotUserIsFound(BasePermission):
	message = _('Пользователь Telegram бота не найдена!')

	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot | None = getattr(request, 'telegram_bot', None)

		if not telegram_bot:
			return False

		telegram_bot_user_id: int = view.kwargs.pop('telegram_bot_user_id', 0)

		try:
			setattr(request, 'telegram_bot_user', telegram_bot.users.get(id=telegram_bot_user_id))
		except TelegramBotUser.DoesNotExist:
			return False

		return True