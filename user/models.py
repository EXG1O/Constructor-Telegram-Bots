from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from aiogram.types import Chat

from utils.shortcuts import generate_random_string

from .utils import get_user_info

from typing import Any
import string


class UserManager(BaseUserManager):
	def create_superuser(self, **fields: Any) -> 'User':
		return self.create(is_staff=True, is_superuser=True, **fields) # type: ignore [return-value]

class User(AbstractBaseUser, PermissionsMixin):
	telegram_id = models.BigIntegerField('Telegram ID', unique=True)
	first_name = models.CharField(_('Имя'), max_length=64, null=True)
	last_name = models.CharField(_('Фамилия'), max_length=64, null=True, default=None)
	confirm_code = models.CharField(max_length=25, null=True)
	password = None # type: ignore [assignment]
	is_staff = models.BooleanField(_('Сотрудник'), default=False)
	joined_date = models.DateTimeField(_('Присоединился'), auto_now_add=True)

	USERNAME_FIELD = 'telegram_id'

	objects = UserManager()

	class Meta:
		db_table = 'user'

		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	@property
	def login_url(self) -> str:
		if not self.confirm_code:
			self.confirm_code = generate_random_string(length=25, chars=string.ascii_letters + string.digits)
			self.save()

		return settings.SITE_DOMAIN + f'/login/{self.id}/{self.confirm_code}/' # type: ignore [misc]

	def update_first_name(self, save: bool = False) -> None:
		user_info: Chat | None = get_user_info(self.telegram_id)

		if user_info and user_info.first_name and user_info.first_name != self.first_name:
			self.first_name = user_info.first_name

			if save:
				self.save()

	def update_last_name(self, save: bool = False) -> None:
		user_info: Chat | None = get_user_info(self.telegram_id)

		if user_info and user_info.last_name and user_info.last_name != self.last_name:
			self.last_name = user_info.last_name

			if save:
				self.save()

	def __str__(self) -> str:
		return self.first_name if self.first_name else str(self.telegram_id)