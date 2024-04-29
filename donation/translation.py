from modeltranslation.translator import TranslationOptions, register

from .models import Button, Section


@register(Section)
class SectionTranslationOptions(TranslationOptions):
	fields = ['title', 'text']


@register(Button)
class ButtonTranslationOptions(TranslationOptions):
	fields = ['text']
