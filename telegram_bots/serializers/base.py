from rest_framework import serializers

from ..models.base import AbstractBlock, AbstractMedia, AbstractMessageMedia
from .connection import ConnectionSerializer

from typing import Any, TypeVar
import os

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
    name = serializers.CharField(source='file.name', read_only=True, allow_null=True)
    size = serializers.IntegerField(source='file.size', read_only=True, allow_null=True)
    url = serializers.URLField(source='file.url', read_only=True, allow_null=True)

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

    def process_name(self, base_name: str) -> str:
        name, ext = os.path.splitext(os.path.basename(base_name))
        return '_'.join(name.split('_')[:-1]) + ext

    def to_representation(self, instance: AMT) -> dict[str, Any]:
        representation: dict[str, Any] = super().to_representation(instance)

        name: str | None = representation.get('name')

        if name:
            representation['name'] = self.process_name(name)

        return representation


class MessageMediaSerializer(MediaSerializer[AMMT]):
    class Meta(MediaSerializer.Meta):
        fields = MediaSerializer.Meta.fields + ['id', 'position']
