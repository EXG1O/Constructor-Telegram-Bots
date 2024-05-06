from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
	date_hierarchy = 'joined_date'
	actions = ['generate_confirm_code_action']
	search_fields = ['telegram_id', 'first_name', 'last_name']
	list_filter = ['is_staff', 'last_login', 'joined_date']
	list_display = [
		'id',
		'telegram_id',
		'first_name',
		'last_name',
		'telegram_bots_count',
		'is_staff',
		'last_login',
		'joined_date',
	]
	fields = [
		'id',
		'telegram_id',
		'first_name',
		'last_name',
		'confirm_code',
		'confirm_code_generation_date',
		'telegram_bots_count',
		'groups',
		'is_staff',
		'last_login',
		'joined_date',
	]
	readonly_fields = [
		'id',
		'telegram_id',
		'first_name',
		'last_name',
		'confirm_code',
		'confirm_code_generation_date',
		'telegram_bots_count',
		'last_login',
		'joined_date',
	]

	def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
		return (
			super()
			.get_queryset(request)
			.annotate(telegram_bots_count=Count('telegram_bots'))
		)

	@admin.display(description=_('Telegram ботов'), ordering='telegram_bots_count')
	def telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()

	@admin.action(
		description=_('Сгенерировать код подтверждения'),
		permissions=['add', 'change', 'delete'],
	)
	def generate_confirm_code_action(
		self, request: HttpRequest, users: QuerySet[User]
	) -> None:
		for user in users:
			user.generate_confirm_code()

		messages.success(
			request,
			_(
				'Успешная генерация кодов подтверждения '
				'для %(users_count)s пользователей.'
			)
			% {'users_count': users.count()},
		)
