from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, re_path
from django.views.generic import TemplateView

import django_stubs_ext

from rest_framework.generics import GenericAPIView

django_stubs_ext.monkeypatch(extra_classes=[GenericAPIView])


urlpatterns: list[URLPattern | URLResolver] = [
	path('admin/', admin.site.urls),
	path('tinymce/', include('tinymce.urls')),
	path(
		'api/',
		include(
			(
				[
					path('languages/', include('languages.urls')),
					path('users/', include('users.urls')),
					path('telegram-bots/', include('telegram_bots.urls')),
					path(
						'telegram-bots-hub/telegram-bots/',
						include('telegram_bots.hub.urls'),
					),
					path('updates/', include('updates.urls')),
					path('donation/', include('donation.urls')),
					path('instruction/', include('instruction.urls')),
					path('privacy-policy/', include('privacy_policy.urls')),
				],
				'api',
			)
		),
	),
]

if not settings.TEST and settings.DEBUG:
	from django.conf.urls.static import static

	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

	urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))

urlpatterns.append(
	re_path(r'^.*', TemplateView.as_view(template_name='frontend/index.html'))
)
