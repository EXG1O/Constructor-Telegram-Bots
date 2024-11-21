from modeltranslation.translator import TranslationOptions, register

from .models import Method, Section


@register(Section)
class SectionTranslationOptions(TranslationOptions):
	fields = ['title', 'text']


@register(Method)
class MethodTranslationOptions(TranslationOptions):
	fields = ['text']
