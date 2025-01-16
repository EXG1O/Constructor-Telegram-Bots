from rest_framework import serializers

from .models import Update


class UpdateSerializer(serializers.ModelSerializer[Update]):
	class Meta:
		model = Update
		fields = ['id', 'version', 'description', 'added_date']
