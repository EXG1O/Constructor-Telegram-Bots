from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ParseError
from rest_framework.parsers import DataAndFiles, MultiPartParser

from itertools import chain
from json import JSONDecodeError
from typing import Any
import json
import re


class MultiPartJSONParser(MultiPartParser):
	"""Parser for JSON data in multipart form data with support for files and their extra data."""

	error_detail = _("Не удалось проанализировать JSON данные для ключа '%(key)s'.")

	def parse_json(self, json_string: str, key: str) -> dict[str, Any]:
		try:
			return json.loads(json_string)
		except JSONDecodeError:
			raise ParseError(self.error_detail % {'key': key})

	def parse(self, *args: Any, **kwargs: Any) -> dict[str, Any]:  # type: ignore [override]
		parsed: DataAndFiles = super().parse(*args, **kwargs)  # type: ignore [type-arg]

		data: dict[str, Any] = self.parse_json(parsed.data.get('data', '{}'), 'data')
		data.update({'images': [], 'files': []})

		for key, value in chain(parsed.data.items(), parsed.files.items()):
			if not re.fullmatch(r'^(image|file):\d+$', key, re.IGNORECASE):
				continue

			name, index = key.split(':')

			extra_data_key: str = f'{name}:{index}:extra_data'
			extra_data: dict[str, Any] = self.parse_json(
				parsed.data.get(extra_data_key, '{}'), extra_data_key
			)

			if isinstance(value, UploadedFile):
				data[f'{name}s'].append({name: value, **extra_data})
			elif isinstance(value, str):
				if value.isdigit():
					data[f'{name}s'].append({'id': int(value), **extra_data})
				else:
					data[f'{name}s'].append({'url': value, **extra_data})

		return data
