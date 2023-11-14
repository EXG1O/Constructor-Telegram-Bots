from django.utils.translation import gettext as _

from constructor_telegram_bots.utils.drf import CustomResponse

from ..models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboard,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser,
)

from functools import wraps


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

def check_telegram_bot_command_keyboard_button_id(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		telegram_bot_command: TelegramBotCommand = kwargs['telegram_bot_command']
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.keyboard
		telegram_bot_command_keyboard_button_id: int = kwargs.pop('telegram_bot_command_keyboard_button_id', 0)

		try:
			kwargs['telegram_bot_command_keyboard_button'] = telegram_bot_command_keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id)
		except TelegramBotCommandKeyboardButton.DoesNotExist:
			return CustomResponse(_('Кнопка клавиатуры команды Telegram бота не найдена!'), status=404)

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
