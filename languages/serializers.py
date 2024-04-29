from django.conf import settings

from rest_framework import serializers

from typing import Any


class SetLanguageSerializer(serializers.Serializer[Any]):
	lang_code = serializers.ChoiceField(settings.LANGUAGES)

	class Meta:
		fields = ['lang_code']
