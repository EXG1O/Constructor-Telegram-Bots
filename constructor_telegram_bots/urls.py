from django.urls import path, include
from django.contrib import admin
from django.conf import settings

import sys


urlpatterns = [
	path('admin/', admin.site.urls),
	path('i18n/', include('django.conf.urls.i18n')),

	path('tinymce/', include('tinymce.urls')),

	path('user/', include('user.urls')),
	path('', include('home.urls')),
	path('team/', include('team.urls')),
	path('updates/', include('updates.urls')),
	path('instruction/', include('instruction.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),
	path('telegram-bot-menu/', include('telegram_bot_menu.urls')),
	path('telegram-bots/', include('telegram_bot.urls')),
	path('plugins/', include('plugin.urls')),
	path('privacy-policy/', include('privacy_policy.urls')),
]


if settings.DEBUG:
	from django.conf.urls.static import static

	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if sys.platform == 'win32':
	match sys.argv:
		case ['manage.py', 'runserver', *extra_options]:
			from telegram_bot.tasks import start_all_telegram_bots as celery_start_all_telegram_bots

			celery_start_all_telegram_bots()
