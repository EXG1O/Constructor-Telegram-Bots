from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import Invoice, InvoiceImage, InvoicePrice
from .base import DiagramSerializer, MediaSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from contextlib import suppress
from typing import Any


class InvoiceImageSerializer(MediaSerializer[InvoiceImage]):
    class Meta(MediaSerializer.Meta):
        model = InvoiceImage


class InvoicePriceSerializer(serializers.ModelSerializer[InvoicePrice]):
    class Meta:
        model = InvoicePrice
        fields = ['id', 'label', 'amount']


class InvoiceSerializer(TelegramBotMixin, serializers.ModelSerializer[Invoice]):
    image = InvoiceImageSerializer(required=False, allow_null=True)
    prices = InvoicePriceSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'name', 'title', 'description', 'image', 'prices']

    def validate_image(self, data: dict[str, Any] | None) -> dict[str, Any] | None:
        if not data:
            return data

        file: UploadedFile | None = data.get('file')

        if isinstance(self.instance, Invoice):
            has_file: bool = bool(file)
            has_from_url: bool = bool(data.get('from_url'))

            with suppress(InvoiceImage.DoesNotExist):
                invoice_image = self.instance.image

                if not has_file:
                    has_file = bool(invoice_image.file)
                if not has_from_url:
                    has_from_url = bool(invoice_image.from_url)

            if has_file is has_from_url:
                raise serializers.ValidationError(
                    _("Необходимо указать только одно из полей 'file' или 'from_url'."),
                    code='required',
                )

        file_size: int | None = None

        if file:
            file_size = file.size

        if file_size and self.telegram_bot.remaining_storage_size - file_size < 0:
            raise serializers.ValidationError(
                _('Превышен лимит хранилища.'), code='max_storage_size_limit'
            )

        return data

    def validate_prices(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if (not self.instance or not self.partial) and not data:
            raise serializers.ValidationError(
                _('Счёт должен содержать хотя бы одну цену.'), code='empty'
            )

        if (
            len(data)
            if not isinstance(self.instance, Invoice) or not self.partial
            else self.instance.prices.count()
            + sum('id' not in price_data for price_data in data)
        ) > settings.TELEGRAM_BOT_MAX_INVOICE_PRICES:
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s цен счёта.')
                % {'max': settings.TELEGRAM_BOT_MAX_INVOICE_PRICES},
                code='max_limit',
            )

        return data

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if (
            not self.instance
            and self.telegram_bot.invoices.count() + 1
            > settings.TELEGRAM_BOT_MAX_INVOICES
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s счетов.')
                % {'max': settings.TELEGRAM_BOT_MAX_INVOICES},
                code='max_limit',
            )

        return data

    def create_image(self, invoice: Invoice, data: dict[str, Any]) -> InvoiceImage:
        return InvoiceImage.objects.create(invoice=invoice, **data)

    def create_prices(
        self, invoice: Invoice, data: list[dict[str, Any]]
    ) -> list[InvoicePrice]:
        return InvoicePrice.objects.bulk_create(
            InvoicePrice(invoice=invoice, **item) for item in data
        )

    def create(self, validated_data: dict[str, Any]) -> Invoice:
        image_data: dict[str, Any] | None = validated_data.pop('image', None)
        prices_data: list[dict[str, Any]] | None = validated_data.pop('prices', None)

        invoice: Invoice = self.telegram_bot.invoices.create(**validated_data)

        if image_data:
            self.create_image(invoice, image_data)
        if prices_data:
            self.create_prices(invoice, prices_data)

        return invoice

    def update_image(
        self, invoice: Invoice, data: dict[str, Any] | None
    ) -> InvoiceImage | None:
        if not data:
            if not self.partial:
                with suppress(InvoiceImage.DoesNotExist):
                    invoice.image.delete()
            return None

        try:
            image: InvoiceImage = invoice.image

            file: UploadedFile | None = data.get('file')

            if file and image.file:
                image.file.delete()

            image.file = file
            image.from_url = data.get('from_url', image.from_url)
            image.save(update_fields=['file', 'from_url'])
            return image
        except InvoiceImage.DoesNotExist:
            return self.create_image(invoice, data)

    def update_prices(
        self, invoice: Invoice, data: list[dict[str, Any]] | None
    ) -> list[InvoicePrice] | None:
        if not data:
            if not self.partial:
                invoice.prices.all().delete()
            return None

        create_prices: list[InvoicePrice] = []
        update_prices: list[InvoicePrice] = []

        for item in data:
            try:
                price: InvoicePrice = invoice.prices.get(id=item['id'])
                price.label = item.get('label', price.label)
                price.amount = item.get('amount', price.amount)
                update_prices.append(price)
            except (KeyError, InvoicePrice.DoesNotExist):
                create_prices.append(InvoicePrice(invoice=invoice, **item))

        new_prices: list[InvoicePrice] = InvoicePrice.objects.bulk_create(create_prices)
        InvoicePrice.objects.bulk_update(update_prices, fields=['label', 'amount'])

        prices: list[InvoicePrice] = new_prices + update_prices

        if not self.partial:
            invoice.prices.exclude(id__in=[price.id for price in prices]).delete()

        return prices

    def update(self, invoice: Invoice, validated_data: dict[str, Any]) -> Invoice:
        image_data: dict[str, Any] | None = validated_data.get('image')
        prices_data: list[dict[str, Any]] | None = validated_data.get('prices')

        invoice.name = validated_data.get('name', invoice.name)
        invoice.title = validated_data.get('title', invoice.title)
        invoice.description = validated_data.get('description', invoice.description)
        invoice.save(update_fields=['name', 'title', 'description'])

        self.update_image(invoice, image_data)
        self.update_prices(invoice, prices_data)

        return invoice


class DiagramInvoiceSerializer(DiagramSerializer[Invoice]):
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'name',
            'source_connections',
            'target_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name']
