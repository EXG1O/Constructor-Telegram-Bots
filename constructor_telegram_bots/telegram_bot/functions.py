from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.request import Request

import requests


def is_valid_telegram_bot_api_token(api_token: str) -> bool:
	if settings.TEST:
		return True
	else:
		return requests.get(f'https://api.telegram.org/bot{api_token}/getMe').status_code == 200

def get_image_from_request(request: Request) -> InMemoryUploadedFile | str | None:
	if 'image' in request.FILES:
		return request.FILES['image']
	elif 'image' in request.POST:
		return request.POST['image']
