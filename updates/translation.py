from modeltranslation.translator import TranslationOptions, register

from .models import Update


@register(Update)
class UpdateTranslationOptions(TranslationOptions):
	fields = ['description']
