from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Update
from .serializers import UpdateModelSerializer, GetUpdatesSerializer


class UpdatesAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request: Request) -> Response:
		serializer = GetUpdatesSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		validated_data: dict = serializer.validated_data
		offset: int | None = validated_data['offset']
		limit: int | None = validated_data['limit']

		return Response(
			UpdateModelSerializer(
				Update.objects.all()[offset:limit],
				many=True,
			).data
		)