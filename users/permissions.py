from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import User


class IsTermsAccepted(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user: User | None = request.user  # type: ignore [assignment]
        return bool(user and user.accepted_terms)
