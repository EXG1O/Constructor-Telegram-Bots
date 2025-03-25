from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TranslationAdmin

from .models import Section


@admin.register(Section)
class SectionAdmin(
    SortableAdminMixin,
    TranslationAdmin,  # FIXME: Need to add generics support
):
    list_display = ['title', 'position']
    fields = ['title', 'text']
