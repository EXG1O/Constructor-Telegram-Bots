from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from utils.admin import format_html_url

from .models import Donation, DonationSection, DonationButton


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin[Donation]):
	date_hierarchy = 'date'
	list_display = ('sum_', 'telegram_url_', 'date')

	fields = ('sum', 'telegram_url', 'date')

	@admin.display(description=_('Сумма'), ordering='sum')
	def sum_(self, donation: Donation) -> str:
		return f'{donation.sum}€'

	@admin.display(description=_('Telegram'), ordering='telegram_url')
	def telegram_url_(self, donation: Donation) -> str:
		return format_html_url(donation.telegram_url)

@admin.register(DonationSection)
class DonationSectionAdmin(TranslationAdmin):
	list_display = ('title', 'position')

	fields = ('title', 'text', 'position')
	formfield_overrides = {models.TextField: {'widget': TinyMCE}}

@admin.register(DonationButton)
class DonationButtonAdmin(TranslationAdmin):
	list_display = ('text', 'url_', 'position')

	fields = ('text', 'url', 'position')

	@admin.display(description=_('Ссылка'), ordering='url')
	def url_(self, donation_button: DonationButton) -> str:
		return format_html_url(donation_button.url)