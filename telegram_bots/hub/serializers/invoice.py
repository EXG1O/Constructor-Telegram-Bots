from rest_framework import serializers

from ...models import Invoice, InvoiceImage, InvoicePrice
from ...serializers.base import MediaSerializer
from .connection import ConnectionSerializer


class InvoiceImageSerializer(MediaSerializer[InvoiceImage]):
    class Meta(MediaSerializer.Meta):
        model = InvoiceImage


class InvoicePriceSerializer(serializers.ModelSerializer[InvoicePrice]):
    class Meta:
        model = InvoicePrice
        fields = ['id', 'label', 'amount']


class InvoiceSerializer(serializers.ModelSerializer[Invoice]):
    image = InvoiceImageSerializer()
    prices = InvoicePriceSerializer(many=True)
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'title', 'description', 'image', 'prices', 'source_connections']
