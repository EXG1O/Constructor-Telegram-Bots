from rest_framework import serializers

from ...models import TemporaryVariable


class TemporaryVariableSerializer(serializers.ModelSerializer[TemporaryVariable]):
    class Meta:
        model = TemporaryVariable
        fields = ['id', 'name', 'value']
