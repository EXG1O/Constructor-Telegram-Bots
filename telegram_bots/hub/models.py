from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from django_stubs_ext.db.models import TypedModelMeta

from utils.shortcuts import generate_random_string

from ..models import TelegramBot

from requests import Response
from requests.exceptions import ConnectionError, HTTPError, Timeout
import requests

from collections.abc import Iterable
from typing import Any, Literal, Optional
import os
import signal
import socket
import string
import subprocess
import time


class TelegramBotsHubManager(models.Manager['TelegramBotsHub']):
	def get_free(self) -> 'TelegramBotsHub':
		for hub in TelegramBotsHub.objects.all():
			if hub.is_free:
				return hub

		return self.create()

	def get_telegram_bot_hub(self, **filters: Any) -> Optional['TelegramBotsHub']:
		if filters:
			for hub in TelegramBotsHub.objects.all():
				try:
					hub.telegram_bots.get(**filters)

					return hub
				except TelegramBot.DoesNotExist:
					pass

		return None


class TelegramBotsHub(models.Model):
	pid = models.PositiveIntegerField('PID')
	port = models.PositiveSmallIntegerField(_('Порт'))
	token = models.CharField(_('Токен'), max_length=25)

	objects = TelegramBotsHubManager()

	class Meta(TypedModelMeta):
		db_table = 'telegram_bots_hub'

	@property
	def url(self) -> str:
		return f'http://127.0.0.1:{self.port}'

	@property
	def telegram_bots(self) -> QuerySet[TelegramBot]:
		response: Response | None = self.make_api_request('get', '/bots/')

		if response:
			telegram_bot_ids: list[int] = response.json()

			return TelegramBot.objects.filter(id__in=telegram_bot_ids)

		return TelegramBot.objects.none()

	@property
	def is_authenticated(self) -> Literal[True]:
		"""Stub for Django Rest Framework"""

		return True

	def is_port_available(self, port: int) -> bool:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(3)

		try:
			sock.bind(('127.0.0.1', port))
		except OSError:
			return False
		finally:
			sock.close()

		return True

	@property
	def is_available(self) -> bool:
		response: Response | None = self.make_api_request(
			'get', '/', delete_on_exception=False
		)

		if response:
			data: dict[str, Any] = response.json()

			return data['token'] == self.token

		return False

	@property
	def is_free(self) -> bool:
		response: Response | None = self.make_api_request('get', '/')

		if response:
			data: dict[str, Any] = response.json()

			return data['max_bots_limit'] > data['bots_count']

		return False

	def make_api_request(
		self,
		method: Literal['get', 'post', 'patch', 'put', 'delete'],
		url: str,
		data: dict[str, Any] | list[Any] | None = None,
		delete_on_exception: bool = True,
	) -> Response | None:
		try:
			response: Response = requests.request(method, self.url + url, json=data)
			response.raise_for_status()

			return response
		except (ConnectionError, HTTPError, Timeout):
			if delete_on_exception and not self._state.adding:
				self.delete()

			return None

	def start_telegram_bot(self, telegram_bot: TelegramBot) -> None:
		self.make_api_request(
			'post',
			f'/bots/{telegram_bot.id}/start/',
			data={'bot_token': telegram_bot.api_token},
		)

	def restart_telegram_bot(self, telegram_bot: TelegramBot) -> None:
		self.make_api_request(
			'post',
			f'/bots/{telegram_bot.id}/restart/',
			data={'bot_token': telegram_bot.api_token},
		)

	def stop_telegram_bot(self, telegram_bot: TelegramBot) -> None:
		self.make_api_request('post', f'/bots/{telegram_bot.id}/stop/')

	def save(
		self,
		force_insert: bool | tuple[ModelBase, ...] = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if not self._state.adding:
			raise Exception('The model cannot be update after its creation!')

		self.token = generate_random_string(string.ascii_letters + string.digits, 25)

		for port in range(8000, 65536):
			if self.is_port_available(port):
				log_file = open(f'./logs/telegram_bots_hub.{port}.log', 'w')
				process = subprocess.Popen(
					[
						'./env/bin/python',
						'main.py',
						'--port',
						str(port),
						'--service-token',
						self.token,
					],
					stdout=log_file,
					stderr=log_file,
					cwd=settings.TELEGRAM_BOTS_HUB_PATH,
					text=True,
				)

				self.pid = process.pid
				self.port = port

				for _retry in range(10):
					if self.is_available:
						return super().save(
							force_insert, force_update, using, update_fields
						)

					time.sleep(6)
				try:
					os.kill(self.pid, signal.SIGTERM)
				except ProcessLookupError:
					pass

	def delete(
		self, using: str | None = None, keep_parents: bool = False
	) -> tuple[int, dict[str, int]]:
		if self.is_available:
			os.kill(self.pid, signal.SIGTERM)

		return super().delete(using, keep_parents)
