from rest_framework import serializers

from ...models import TelegramBot


class TelegramBotSerializer(serializers.ModelSerializer[TelegramBot]):
    class Meta:
        model = TelegramBot
        fields = ['id', 'is_private']
