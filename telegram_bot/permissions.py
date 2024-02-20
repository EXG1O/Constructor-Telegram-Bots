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
	def has_permission(self, request: Request, view: APIView) -> bool:
		if not request.user and not request.user.is_authenticated:
			raise PermissionError('The permission can use only after IsAuthenticated permission!')

		telegram_bot_id: int = view.kwargs.pop('telegram_bot_id', 0)

		try:
			view.kwargs['telegram_bot'] = request.user.telegram_bots.get(id=telegram_bot_id) # type: ignore [union-attr]
		except TelegramBot.DoesNotExist:
			return False

		return True

def get_telegram_bot(view: APIView) -> TelegramBot:
	telegram_bot: TelegramBot | None = view.kwargs.get('telegram_bot')

	if not isinstance(telegram_bot, TelegramBot):
		raise PermissionError('The permission can use only after TelegramBotIsFound permission!')

	return telegram_bot

class TelegramBotCommandIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		telegram_bot_command_id: int = view.kwargs.pop('telegram_bot_command_id', 0)

		try:
			view.kwargs['telegram_bot_command'] = telegram_bot.commands.get(id=telegram_bot_command_id)
		except TelegramBotCommand.DoesNotExist:
			return False

		return True

class TelegramBotVariableIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		telegram_bot_variable_id: int = view.kwargs.pop('telegram_bot_variable_id', 0)

		try:
			view.kwargs['telegram_bot_variable'] = telegram_bot.variables.get(id=telegram_bot_variable_id)
		except TelegramBotVariable.DoesNotExist:
			return False

		return True

class TelegramBotUserIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		telegram_bot_user_id: int = view.kwargs.pop('telegram_bot_user_id', 0)

		try:
			view.kwargs['telegram_bot_user'] = telegram_bot.users.get(id=telegram_bot_user_id)
		except TelegramBotUser.DoesNotExist:
			return False

		return True