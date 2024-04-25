from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.parsers import MultiPartParser, DataAndFiles
from rest_framework.exceptions import ParseError

import json
from json import JSONDecodeError

from typing import Any


class CommandMultiPartParser(MultiPartParser):
	def parse(self, *args: Any, **kwargs: Any) -> dict[str, Any]: # type: ignore [override]
		parsed: DataAndFiles = super().parse(*args, **kwargs)

		try:
			data: dict[str, Any] = json.loads(parsed.data['data'])
		except (KeyError, JSONDecodeError):
			raise ParseError()

		sorted_files: dict[str, list[InMemoryUploadedFile | int]] = {
			'images': [],
			'images_id': [],
			'files': [],
			'files_id': [],
		}

		for key, value in parsed.files:
			name: str = key.split(':')[0] + 's'

			if name in sorted_files:
				if isinstance(value, InMemoryUploadedFile):
					sorted_files[name].append(value)
				elif isinstance(value, str) and value.isdigit():
					sorted_files[f'{name}_id'].append(int(value))

		data.update(sorted_files)

		return data