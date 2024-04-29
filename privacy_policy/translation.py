from modeltranslation.translator import TranslationOptions, register

from .models import Section


@register(Section)
class SectionTranslationOptions(TranslationOptions):
	fields = ['title', 'text']
