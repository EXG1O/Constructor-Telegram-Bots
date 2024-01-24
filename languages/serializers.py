from django.conf import settings

from rest_framework import serializers


class SetLanguageSerializer(serializers.Serializer):
	lang_code = serializers.ChoiceField(settings.LANGUAGES)

	class Meta:
		fields = ('lang_code',)