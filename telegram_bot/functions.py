from django.conf import settings

import requests


def is_valid_telegram_bot_api_token(api_token: str) -> bool:
	if settings.TEST:
		return True
	else:
		return requests.get(f'https://api.telegram.org/bot{api_token}/getMe').status_code == 200