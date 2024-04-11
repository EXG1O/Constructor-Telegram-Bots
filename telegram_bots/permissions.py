from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import (
	TelegramBot,
	Connection,
	Command,
	Condition,
	BackgroundTask,
	Variable,
	User,
	DatabaseRecord,
)

from typing import Any


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
	telegram_bot: Any = view.kwargs.get('telegram_bot')

	if not isinstance(telegram_bot, TelegramBot):
		raise PermissionError('The permission can use only after TelegramBotIsFound permission!')

	return telegram_bot

class ConnectionIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		connection_id: int = view.kwargs.pop('connection_id', 0)

		try:
			view.kwargs['connection'] = telegram_bot.connections.get(id=connection_id)
		except Connection.DoesNotExist:
			return False

		return True

class CommandIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		command_id: int = view.kwargs.pop('command_id', 0)

		try:
			view.kwargs['command'] = telegram_bot.commands.get(id=command_id)
		except Command.DoesNotExist:
			return False

		return True

class ConditionIsIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		condition_id: int = view.kwargs.pop('condition_id', 0)

		try:
			view.kwargs['condition'] = telegram_bot.conditions.get(id=condition_id)
		except Condition.DoesNotExist:
			return False

		return True

class BackgroundTaskIsIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		background_task_id: int = view.kwargs.pop('background_task_id', 0)

		try:
			view.kwargs['background_task'] = telegram_bot.background_tasks.get(id=background_task_id)
		except BackgroundTask.DoesNotExist:
			return False

		return True

class VariableIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		variable_id: int = view.kwargs.pop('variable_id', 0)

		try:
			view.kwargs['variable'] = telegram_bot.variables.get(id=variable_id)
		except Variable.DoesNotExist:
			return False

		return True

class UserIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		user_id: int = view.kwargs.pop('user_id', 0)

		try:
			view.kwargs['user'] = telegram_bot.users.get(id=user_id)
		except User.DoesNotExist:
			return False

		return True

class DatabaseRecordIsFound(BasePermission):
	def has_permission(self, request: Request, view: APIView) -> bool:
		telegram_bot: TelegramBot = get_telegram_bot(view)
		database_record_id: int = view.kwargs.pop('database_record_id', 0)

		try:
			view.kwargs['database_record'] = telegram_bot.database_records.get(id=database_record_id)
		except DatabaseRecord.DoesNotExist:
			return False

		return True