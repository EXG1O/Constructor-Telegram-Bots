from rest_framework import serializers

from ...models import Variable


class VariableSerializer(serializers.ModelSerializer[Variable]):
    class Meta:
        model = Variable
        fields = ['id', 'name', 'value']
