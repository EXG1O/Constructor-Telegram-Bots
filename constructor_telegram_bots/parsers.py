from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.exceptions import ParseError
from rest_framework.parsers import DataAndFiles, MultiPartParser

from itertools import chain
from json import JSONDecodeError
from typing import Any
import json


class MultiPartJSONParser(MultiPartParser):
	"""Parser for JSON data in multipart form data with support for files."""

	def parse(self, *args: Any, **kwargs: Any) -> dict[str, Any]:  # type: ignore [override]
		parsed: DataAndFiles = super().parse(*args, **kwargs)  # type: ignore [type-arg]

		try:
			data: dict[str, Any] = json.loads(parsed.data['data'])
		except (KeyError, JSONDecodeError):
			raise ParseError()

		data.update({'images': [], 'images_id': [], 'files': [], 'files_id': []})

		for key, value in chain(parsed.data.items(), parsed.files.items()):
			try:
				name: str = key.split(':')[0]
			except IndexError:
				continue

			if name in ['image', 'file']:
				if isinstance(value, InMemoryUploadedFile):
					data[f'{name}s'].append(value)
				elif isinstance(value, str) and value.isdigit():
					data[f'{name}s_id'].append(int(value))

		return data
