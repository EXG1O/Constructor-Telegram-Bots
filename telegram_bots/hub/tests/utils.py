from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import force_authenticate

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rest_framework.views import AsView
else:
    from typing import Generic, TypeVar

    T = TypeVar('T')

    class AsView(Generic[T]): ...


def assert_view_basic_protected(
    request: Request, view: AsView[Any], token: Any, **view_kwargs: Any
) -> None:
    if TYPE_CHECKING:
        response: Response

    force_authenticate(request, None, None)

    response = view(request, **view_kwargs)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    force_authenticate(request, None, token)

    response = view(request, **view_kwargs)
    assert response.status_code == status.HTTP_403_FORBIDDEN
