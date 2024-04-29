from django.contrib import admin
from django.db import models

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):  # FIXME: Need to add generics support
	date_hierarchy = 'added_date'
	list_display = ['version', 'added_date']
	fields = ['version', 'description', 'added_date']
	readonly_fields = ['added_date']
	formfield_overrides = {models.TextField: {'widget': TinyMCE}}
