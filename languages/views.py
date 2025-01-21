from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SetLanguageSerializer


class LanguagesAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @method_decorator(cache_page(3600))
    def get(self, request: Request) -> Response:
        return Response({language[0]: language[1] for language in settings.LANGUAGES})

    def post(self, request: Request) -> Response:
        serializer = SetLanguageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Response()
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            serializer.validated_data['lang_code'],
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )

        return response
