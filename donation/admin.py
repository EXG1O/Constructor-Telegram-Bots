from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from utils.html import format_html_link

from .models import Button, Donation, Section


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin[Donation]):
	date_hierarchy = 'date'
	list_display = ['sum_display', 'contact_link_display', 'date']
	fields = ['sum', 'contact_link', 'date']

	@admin.display(description=_('Сумма'), ordering='sum')
	def sum_display(self, donation: Donation) -> str:
		return f'{donation.sum}€'

	@admin.display(description=_('Контактная ссылка'), ordering='contact_link')
	def contact_link_display(self, donation: Donation) -> str:
		return format_html_link(donation.contact_link)


@admin.register(Section)
class SectionAdmin(TranslationAdmin):  # FIXME: Need to add generics support
	list_display = ['title', 'position']
	fields = ['title', 'text', 'position']
	formfield_overrides = {models.TextField: {'widget': TinyMCE}}


@admin.register(Button)
class ButtonAdmin(TranslationAdmin):  # FIXME: Need to add generics support
	list_display = ['text', 'url_display', 'position']
	fields = ['text', 'url', 'position']

	@admin.display(description=_('Ссылка'), ordering='url')
	def url_display(self, button: Button) -> str:
		return format_html_link(button.url)
