from rest_framework.response import Response
from rest_framework.status import  is_success, is_informational

from typing import Any


class MessageResponse(Response):
	def __init__(
		self,
		message: str | None = None,
		data: dict[str, Any] = {},
		status: int = 200,
	) -> None:
		if is_success(status):
			level = 'success'
		elif is_informational(status):
			level = 'info'
		else:
			level = 'error'

		data['message'] = message
		data['level'] = level

		super().__init__(data, status)