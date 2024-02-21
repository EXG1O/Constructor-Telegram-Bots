from rest_framework import serializers

from .models import InstructionSection


class InstructionSectionSerializer(serializers.ModelSerializer[InstructionSection]):
	class Meta:
		model = InstructionSection
		fields = ('id', 'title', 'text')