from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin[User]):
    date_hierarchy = 'joined_date'
    search_fields = ['telegram_id', 'first_name', 'last_name']
    list_filter = [
        'accepted_terms',
        'terms_accepted_date',
        'is_staff',
        'last_login',
        'joined_date',
    ]
    list_display = [
        'id',
        'telegram_id',
        'first_name',
        'last_name',
        'telegram_bot_count',
        'accepted_terms',
        'terms_accepted_date',
        'is_staff',
        'last_login',
        'joined_date',
    ]
    fields = [
        'id',
        'telegram_id',
        'first_name',
        'last_name',
        'telegram_bot_count',
        'groups',
        'accepted_terms',
        'terms_accepted_date',
        'is_staff',
        'last_login',
        'joined_date',
    ]
    readonly_fields = [
        'id',
        'telegram_id',
        'first_name',
        'last_name',
        'telegram_bot_count',
        'accepted_terms',
        'terms_accepted_date',
        'last_login',
        'joined_date',
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[User]:
        return (
            super()
            .get_queryset(request)
            .annotate(telegram_bot_count=Count('telegram_bots'))
        )

    @admin.display(description=_('Telegram ботов'), ordering='telegram_bot_count')
    def telegram_bot_count(self, user: User) -> int:
        return user.telegram_bots.count()
