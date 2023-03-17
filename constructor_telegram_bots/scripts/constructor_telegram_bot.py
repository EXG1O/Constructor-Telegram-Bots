from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.update import Update

from user.models import User

from scripts.decorators import TelegramBotDecorators

class ConstructorTelegramBot:
	def __init__(self) -> None:
		self.commands = {
			'start': self.start_command,
			'auth': self.auth_command,
		}
		# self.callback = {
		# 	'delete_msg': self.delete_message,
		# }

	# @TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'callback_data',))
	# def handle_callback_query(self, update: Update, context: CallbackContext, callback_data: str):
	# 	callback_data: str = callback_data.split(':')[0]
	# 	if callback_data in self.callback:
	# 		self.callback[callback_data](update, context)
	
	# @Decorators.get_attributes(need_attributes=('message',))
	# def new_message(self, message: str):
	# 	print(message)

	@TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'username', 'message',))
	def start_command(self, update: Update, context: CallbackContext, user_id: int, username: str, message: str):
		if len(message.split()) > 1:
			if message.split()[1] == 'auth':
				self.auth_command(update, context)

	@TelegramBotDecorators.get_attributes(need_attributes=('update', 'context', 'user_id', 'username',))
	def auth_command(self, update: Update, context: CallbackContext, user_id: int, username: str):
		if User.objects.filter(id=user_id).exists() == False:
			User.objects.create_user(user_id=user_id, username=username)

		keyboard = InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton(text='Авторизация', url=User.objects.get_auth_url(user_id=user_id)),
				],
			]
		)

		context.bot.send_message(chat_id=user_id, text='Нажмите на кнопку ниже, чтобы авторизоваться на сайте.', reply_markup=keyboard)

	def start(self):
		with open('./data/constructor_telegram_bot.token', 'r') as constructor_telegram_bot_token_file:
			constructor_telegram_bot_token = constructor_telegram_bot_token_file.read()

		self.updater = Updater(token=constructor_telegram_bot_token)
		self.dispatcher = self.updater.dispatcher

		# self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback_query))

		# new_message_handler = MessageHandler(Filters.text & (~Filters.command), self.new_message)
		# self.dispatcher.add_handler(new_message_handler)

		for command in self.commands:
			handler = CommandHandler(command, self.commands[command])
			self.dispatcher.add_handler(handler)

		self.updater.start_polling()

	def stop(self) -> None:
		self.updater.stop()