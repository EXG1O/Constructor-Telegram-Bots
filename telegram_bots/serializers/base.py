from rest_framework import serializers

from ..models.base import AbstractBlock, AbstractMedia, AbstractMessageMedia
from .connection import ConnectionSerializer

from typing import Any, TypeVar

ABT = TypeVar('ABT', bound=AbstractBlock)
AMT = TypeVar('AMT', bound=AbstractMedia)
AMMT = TypeVar('AMMT', bound=AbstractMessageMedia)


class DiagramSerializer(serializers.ModelSerializer[ABT]):
    source_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'name', 'x', 'y', 'source_connections']
        read_only_fields = ['name']

    def update(
        self,
        instance: ABT,
        validated_data: dict[str, Any],
        update_fields: list[str] = [],  # noqa: B006
    ) -> ABT:
        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.save(update_fields=update_fields + ['x', 'y'])

        return instance


class MediaSerializer(serializers.ModelSerializer[AMT]):
    name = serializers.CharField(
        source='get_original_filename', read_only=True, allow_null=True
    )
    size = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        fields = ['file', 'name', 'size', 'url', 'from_url']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'file': {
                'write_only': True,
                'required': False,
                'allow_null': True,
            },
        }

    def get_size(self, media: AMT) -> int | None:
        return media.file and media.file.size

    def get_url(self, media: AMT) -> str | None:
        return media.file and media.file.url


class MessageMediaSerializer(MediaSerializer[AMMT]):
    class Meta(MediaSerializer.Meta):
        fields = MediaSerializer.Meta.fields + ['id', 'position']
