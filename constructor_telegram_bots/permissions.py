from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class ReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in SAFE_METHODS
