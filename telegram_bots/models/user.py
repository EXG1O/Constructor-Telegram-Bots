from django.db import models
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta


class User(models.Model):
    telegram_bot = models.ForeignKey(
        'TelegramBot',
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_('Telegram бот'),
    )
    telegram_id = models.PositiveBigIntegerField('Telegram ID')
    full_name = models.CharField(_('Имя и фамилия'), max_length=129)
    is_allowed = models.BooleanField(_('Разрешён'), default=False)
    is_blocked = models.BooleanField(_('Заблокирован'), default=False)
    last_activity_date = models.DateTimeField(
        _('Дата последней активности'), auto_now_add=True
    )
    activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

    class Meta(TypedModelMeta):
        db_table = 'telegram_bot_user'
        verbose_name = _('Пользователя')
        verbose_name_plural = _('Пользователи')

    def __str__(self) -> str:
        return self.full_name
