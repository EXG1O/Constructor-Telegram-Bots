from django.urls import path, re_path, include
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.views.generic import TemplateView
from django.conf import settings


urlpatterns = [
	path('admin/', admin.site.urls),
	path('tinymce/', include('tinymce.urls')),

	path('i18n/', include('django.conf.urls.i18n')),
	path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

	path('api/', include([
		path('', include('user.urls')),
		path('telegram-bots/', include('telegram_bot.urls')),
		path('team/', include('team.urls')),
		path('updates/', include('updates.urls')),
		path('donations/', include('donation.urls')),
		path('instruction/', include('instruction.urls')),
	])),
]

if settings.DEBUG:
	from django.conf.urls.static import static

	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='frontend/index.html'))]