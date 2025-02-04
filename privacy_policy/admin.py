from django.contrib import admin
from django.db import models

from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import Section


@admin.register(Section)
class SectionAdmin(
    SortableAdminMixin,
    TranslationAdmin,  # FIXME: Need to add generics support
):
    list_display = ['title', 'position']
    fields = ['title', 'text']
    formfield_overrides = {models.TextField: {'widget': TinyMCE}}
