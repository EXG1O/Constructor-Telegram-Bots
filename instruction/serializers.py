from rest_framework import serializers

from .models import InstructionSection


class InstructionSectionModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstructionSection
		fields = ['id', 'title', 'text']