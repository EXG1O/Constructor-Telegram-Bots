from django.contrib import admin
from django.db import models

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import Section


@admin.register(Section)
class SectionAdmin(TranslationAdmin):  # FIXME: Need to add generics support
	list_display = ['title', 'position']
	fields = ['title', 'text', 'position']
	formfield_overrides = {models.TextField: {'widget': TinyMCE}}
