from django.contrib import admin
from django.db import models

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import PrivacyPolicySection


@admin.register(PrivacyPolicySection)
class PrivacyPolicySectionAdmin(TranslationAdmin):
	list_display = ('title', 'position', 'last_update_date')

	fields = ('title', 'text', 'position')
	formfield_overrides = {models.TextField: {'widget': TinyMCE}}