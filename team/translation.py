from modeltranslation.translator import register, TranslationOptions

from .models import Member


@register(Member)
class MemberTranslationOptions(TranslationOptions):
    fields = ('speciality',)