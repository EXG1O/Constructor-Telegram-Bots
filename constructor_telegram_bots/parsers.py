from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ParseError
from rest_framework.parsers import DataAndFiles, MultiPartParser

from collections import defaultdict
from itertools import chain
from json import JSONDecodeError
from typing import Any
import json
import re


class MultiPartJSONParser(MultiPartParser):
	"""Parser for JSON data in multipart form data with support for files and their extra data."""

	error_detail = _("Не удалось проанализировать JSON данные для ключа '%(key)s'.")

	def parse_json(self, key: str, data: str) -> dict[str, Any]:
		try:
			return json.loads(data)
		except JSONDecodeError as error:
			raise ParseError(self.error_detail % {'key': key}) from error

	def parse(self, *args: Any, **kwargs: Any) -> dict[str, Any]:  # type: ignore [override]
		parsed: DataAndFiles[dict[str, Any], MultiValueDict[str, UploadedFile]] = (
			super().parse(*args, **kwargs)  # type: ignore [assignment]
		)

		data: dict[str, Any] = (
			self.parse_json('data', raw_data)
			if (raw_data := parsed.data.get('data'))
			else {}
		)
		tmp_data: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)

		for key, value in chain(parsed.data.items(), parsed.files.items()):
			result: re.Match[str] | None = re.fullmatch(
				r'^(?P<name>\w+):(?P<index>\d+)$', key, re.IGNORECASE
			)

			if not result:
				continue

			name, index = result.group('name', 'index')

			extra_data_key: str = f'{name}:{index}:extra_data'
			extra_data: dict[str, Any] = (
				self.parse_json(extra_data_key, raw_extra_data)
				if (raw_extra_data := parsed.data.get(extra_data_key))
				else {}
			)

			if isinstance(value, UploadedFile):
				tmp_data[name].append({name: value, **extra_data})
			elif isinstance(value, str):
				if value.isdigit():
					tmp_data[name].append({'id': int(value), **extra_data})
				else:
					tmp_data[name].append({'url': value, **extra_data})

		for key, items in tmp_data.items():
			if len(items) > 1:
				data.update({f'{key}s': items})
			else:
				data.update({key: items[0]})

		return data
