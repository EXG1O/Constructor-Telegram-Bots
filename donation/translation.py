from modeltranslation.translator import register, TranslationOptions

from .models import DonationSection, DonationButton


@register(DonationSection)
class DonationSectionTranslationOptions(TranslationOptions):
	fields = ('title', 'text')

@register(DonationButton)
class DonationButtonTranslationOptions(TranslationOptions):
	fields = ('text',)
