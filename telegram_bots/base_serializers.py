from rest_framework import serializers

from .base_models import AbstractBlock, AbstractCommandMedia

from typing import TYPE_CHECKING, Any, TypeVar
import os

ABT = TypeVar('ABT', bound=AbstractBlock)
ACMT = TypeVar('ACMT', bound=AbstractCommandMedia)


class DiagramSerializer(serializers.ModelSerializer[ABT]):
	class Meta:
		fields = ['x', 'y']

	def update(self, instance: ABT, validated_data: dict[str, Any]) -> ABT:
		instance.x = validated_data.get('x', instance.x)
		instance.y = validated_data.get('y', instance.y)
		instance.save()

		return instance


class CommandMediaSerializerMetaclass(serializers.SerializerMetaclass):
	def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> Any:
		if name != 'CommandMediaSerializer':
			file_field_name: str | None = attrs.get('file_field_name')

			if not file_field_name:
				raise AssertionError(
					"Child class must define the 'file_field_name' attribute"
				)

			meta: type[serializers.ModelSerializer.Meta] | None = attrs.get('Meta')

			if not meta:
				raise AssertionError("Child class must define a 'Meta' class")

			attrs['name'] = serializers.CharField(
				source=f'{file_field_name}.name', read_only=True, allow_null=True
			)
			attrs['size'] = serializers.IntegerField(
				source=f'{file_field_name}.size', read_only=True, allow_null=True
			)
			attrs['url'] = serializers.URLField(
				source=f'{file_field_name}.url', read_only=True, allow_null=True
			)

			meta_fields: list[str] = getattr(meta, 'fields', [])
			meta_fields += [
				'id',
				'position',
				file_field_name,
				'name',
				'size',
				'url',
				'from_url',
			]

			meta_extra_kwargs: dict[str, dict[str, Any]] = getattr(
				meta, 'extra_kwargs', {}
			)
			meta_extra_kwargs.setdefault('id', {}).update(
				{
					'read_only': False,
					'required': False,
				}
			)
			meta_extra_kwargs.setdefault(file_field_name, {}).update(
				{
					'write_only': True,
					'required': False,
					'allow_null': True,
				}
			)

			meta.fields = meta_fields
			meta.extra_kwargs = meta_extra_kwargs

		return super().__new__(cls, name, bases, attrs)


class CommandMediaSerializer(
	serializers.ModelSerializer[ACMT], metaclass=CommandMediaSerializerMetaclass
):
	if TYPE_CHECKING:
		file_field_name: str

	def process_name(self, base_name: str) -> str:
		name, ext = os.path.splitext(os.path.basename(base_name))
		return '_'.join(name.split('_')[:-1]) + ext

	def to_representation(self, instance: ACMT) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)

		name: str | None = representation.get('name')

		if name:
			representation['name'] = self.process_name(name)

		return representation
