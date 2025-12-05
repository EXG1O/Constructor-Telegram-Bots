from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .authentication import JWTAuthentication
from .backends import TelegramBackend
from .models import User
from .serializers import UserLoginSerializer, UserSerializer, UserTokenRefreshSerializer
from .tokens import RefreshToken
from .utils import login as user_login
from .utils import logout as user_logout
from .utils import logout_all as user_logout_all

from typing import Any


class StatsAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(cache_page(3600))
    def get(self, request: Request) -> Response:
        return Response({'total': User.objects.count()})


class UserViewSet(RetrieveModelMixin, GenericViewSet[User]):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user  # type: ignore [return-value]

    @action(
        detail=False, methods=['POST'], authentication_classes=[], permission_classes=[]
    )
    def login(self, request: Request) -> Response:
        data: dict[str, Any] = request.data.copy()

        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user: User = TelegramBackend().authenticate(
            request, hash=data.pop('hash'), raise_exception=True, **data
        )
        refresh_token: RefreshToken = user_login(request, user)

        return Response(
            {
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token),
            }
        )

    @action(detail=True, methods=['POST'])
    def logout(self, request: Request, pk: str | None = None) -> Response:
        user_logout(request, request.auth)  # type: ignore[arg-type]
        return Response()

    @action(detail=True, url_path='logout-all', methods=['POST'])
    def logout_all(self, request: Request, pk: str | None = None) -> Response:
        user_logout_all(request, request.user)  # type: ignore[arg-type]
        return Response()

    @action(
        detail=True,
        url_path='token-refresh',
        methods=['POST'],
        authentication_classes=[],
        permission_classes=[],
    )
    def token_refresh(self, request: Request, pk: str | None = None) -> Response:
        serializer = UserTokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token: RefreshToken = serializer.validated_data['refresh_token']

        return Response({'access_token': str(refresh_token.access_token)})

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        user: User = request.user  # type: ignore [assignment]

        user_logout_all(request, user)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
