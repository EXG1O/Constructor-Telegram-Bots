from modeltranslation.translator import register, TranslationOptions

from .models import Section, Button


@register(Section)
class SectionTranslationOptions(TranslationOptions):
	fields = ('title', 'text')


@register(Button)
class ButtonTranslationOptions(TranslationOptions):
	fields = ('text',)
