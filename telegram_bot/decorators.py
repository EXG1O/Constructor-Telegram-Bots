from django.utils.translation import gettext as _

from rest_framework.request import Request

from utils.drf import CustomResponse

from .models import TelegramBot, TelegramBotCommand, TelegramBotUser

from functools import wraps


def check_telegram_bot_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request: Request = args[-1]
		telegram_bot_id: int = kwargs.pop('telegram_bot_id', 0)

		try:
			kwargs['telegram_bot'] = request.user.telegram_bots.get(id=telegram_bot_id)
		except TelegramBot.DoesNotExist:
			return CustomResponse(_('Telegram бот не найден!'), status=404)

		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_command_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_command_id: int = kwargs.pop('telegram_bot_command_id', 0)

		try:
			kwargs['telegram_bot_command'] = telegram_bot.commands.get(id=telegram_bot_command_id)
		except TelegramBotCommand.DoesNotExist:
			return CustomResponse(_('Команда Telegram бота не найдена!'), status=404)

		return func(*args, **kwargs)
	return wrapper

def check_telegram_bot_user_id(func):
	def wrapper(*args, **kwargs):
		telegram_bot: TelegramBot = kwargs['telegram_bot']
		telegram_bot_user_id: int = kwargs.pop('telegram_bot_user_id', 0)

		try:
			kwargs['telegram_bot_user'] = telegram_bot.users.get(id=telegram_bot_user_id)
		except TelegramBotUser.DoesNotExist:
			return CustomResponse(_('Пользователь Telegram бота не найдена!'), status=404)

		return func(*args, **kwargs)
	return wrapper