from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):  # FIXME: Need to add generics support
    date_hierarchy = 'added_date'
    list_display = ['version', 'added_date']
    fields = ['version', 'description', 'added_date']
    readonly_fields = ['added_date']
