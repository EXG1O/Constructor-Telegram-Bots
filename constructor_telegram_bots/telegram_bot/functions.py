from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.request import Request

import requests


def check_telegram_bot_api_token(api_token: str) -> str | None:
	if settings.TEST:
		return f"{api_token.split(':')[0]}_test_telegram_bot"

	responce: requests.Response = requests.get(f'https://api.telegram.org/bot{api_token}/getMe')

	if responce.status_code == 200:
		return responce.json()['result']['username']
	else:
		return None

def get_image_from_request(request: Request) -> InMemoryUploadedFile | str | None:
	if 'image' in request.FILES:
		return request.FILES['image']
	elif 'image' in request.POST:
		return request.POST['image']
	else:
		return None
