from rest_framework.pagination import LimitOffsetPagination as BaseLimitOffsetPagination
from rest_framework.response import Response

from typing import Any


class LimitOffsetPagination(BaseLimitOffsetPagination):
	def get_paginated_response(self, data: list[dict[str, Any]]) -> Response:
		return Response({'count': self.count, 'results': data})
