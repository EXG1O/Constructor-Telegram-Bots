from django.conf import settings

from aiogram.types import Chat

import requests


def get_user_info(telegram_id: int) -> Chat | None:
	response: requests.Response = requests.get(f'https://api.telegram.org/bot{settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN}/getChat?chat_id={telegram_id}')

	if response.status_code == 200:
		return Chat(**response.json()['result'])
	else:
		return None