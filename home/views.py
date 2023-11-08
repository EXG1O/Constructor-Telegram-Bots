from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from user.models import User
from telegram_bot.models import TelegramBot
from updates.models import Update
from donation.models import Donation


def home_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'home.html', {
		'users': User.objects.all(),
		'telegram_bots': TelegramBot.objects.all(),
		'updates': Update.objects.all(),
		'donations': Donation.objects.all(),
	})
