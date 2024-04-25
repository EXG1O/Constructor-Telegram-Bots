from modeltranslation.translator import register, TranslationOptions

from .models import Section


@register(Section)
class SectionTranslationOptions(TranslationOptions):
	fields = ('title', 'text')
