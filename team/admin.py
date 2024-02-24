from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import Member


@admin.register(Member)
class MemberAdmin(TranslationAdmin): # FIXME: Need to add generics support
	search_fields = ('username',)
	date_hierarchy = 'joined_date'
	list_filter = ('speciality', 'joined_date')
	list_display = ('username_display', 'speciality', 'joined_date')
	fields = ('image', 'username', 'speciality', 'joined_date')

	@admin.display(description='@username', ordering='username')
	def username_display(self, member: Member) -> str:
		return f'@{member.username}'