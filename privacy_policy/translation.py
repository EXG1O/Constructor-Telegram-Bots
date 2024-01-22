from modeltranslation.translator import register, TranslationOptions

from .models import PrivacyPolicySection


@register(PrivacyPolicySection)
class PrivacyPolicySectionTranslationOptions(TranslationOptions):
    fields = ('title', 'text')