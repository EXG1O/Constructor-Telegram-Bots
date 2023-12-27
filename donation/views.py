from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Donation, DonationSection, DonationButton
from .serializers import (
	DonationModelSerializer,
	DonationSectionModelSerializer,
	DonationButtonModelSerializer,
	GetDonationsSerializer,
)

from typing import Any


class DonationsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request: Request) -> Response:
		serializer = GetDonationsSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		offset: int | None = validated_data['offset']
		limit: int | None = validated_data['limit']

		return Response(
			DonationModelSerializer(
				Donation.objects.all()[offset:limit],
				many=True,
			).data
		)

class DonationSectionsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response(
			DonationSectionModelSerializer(
				DonationSection.objects.all(),
				many=True,
			).data
		)

class DonationButtonsAPIView(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request: Request) -> Response:
		return Response(
			DonationButtonModelSerializer(
				DonationButton.objects.all(),
				many=True,
			).data
		)