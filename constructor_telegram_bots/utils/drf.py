from rest_framework.response import Response
from rest_framework.status import is_success, is_informational

from typing import Literal, Any


class CustomResponse(Response):
	def __init__(
		self,
		message: str | None = None,
		level: Literal['success', 'primary', 'danger'] | None = None,
		data: dict[str, Any] = {},
		status: int = 200,
		headers: dict[str, Any] | None = None,
	) -> None:
		if level is None:
			if is_success(status):
				level = 'success'
			elif is_informational(status):
				level = 'primary'
			else:
				level = 'danger'

		data['message'] = message
		data['level'] = level

		super().__init__(data, status, headers=headers)
