from rest_framework import serializers

from .models import InstructionSection


class InstructionSectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = InstructionSection
		fields = ('id', 'title', 'text')