from django.db.models import QuerySet, Model

from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response

from typing import TypeVar, Union, Any


T = TypeVar('T', bound=Model)


class PaginationMixin:
	pagination_class: type[BasePagination]

	@property
	def paginator(self) -> BasePagination:
		if not hasattr(self, '_paginator'):
			if not hasattr(self, 'pagination_class'):
				raise AttributeError("You are planning to use pagination, but you don't set pagination_class attribute!")

			self._paginator = self.pagination_class()

		return self._paginator

	def paginate_queryset(self, request: Request, queryset: Union[list[T], QuerySet[T]]) -> list[T] | None:
		return self.paginator.paginate_queryset(queryset, request, view=self) # type: ignore [arg-type]

	def get_paginated_response(self, data: dict[str, Any]) -> Response:
		return self.paginator.get_paginated_response(data)