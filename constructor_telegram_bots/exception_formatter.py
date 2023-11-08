from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse, Error

from typing import TypedDict


class FormatErrorResponse(TypedDict):
	code: str
	name: str | None
	message: str
	level: str

class CustomExceptionFormatter(ExceptionFormatter):
	def format_error_response(self, error_response: ErrorResponse) -> FormatErrorResponse:
		error: Error = error_response.errors[0]

		return {
			'code': error.code,
			'name': error.attr,
			'message': error.detail,
			'level': 'danger',
		}
