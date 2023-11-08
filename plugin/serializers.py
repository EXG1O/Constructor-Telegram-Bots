from django.template import defaultfilters as filters
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from telegram_bot.models import TelegramBot

from .models import Plugin, PluginLog

from typing import Any
import re


class ModelSerializer(serializers.ModelSerializer):
	def to_representation(self, instance: Plugin | PluginLog) -> dict[str, Any]:
		representation: dict[str, Any] = super().to_representation(instance)
		representation['added_date'] = f'{filters.date(instance.added_date)} {filters.time(instance.added_date)}'

		return representation

class PluginModelSerializer(ModelSerializer):
	class Meta:
		model = Plugin
		fields = ['id', 'name', 'code', 'is_checked']

class PluginLogModelSerializer(ModelSerializer):
	plugin_name = serializers.CharField(max_length=255, source='plugin.name')

	class Meta:
		model = PluginLog
		fields = ['id', 'plugin_name', 'message', 'level']

class CreatePluginSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите название плагина!'),
		'max_length': _('Название плагина должно содержать не более 255 символов!'),
	})
	code = serializers.CharField()

	def validate_name(self, name: str) -> str:
		telegram_bot: TelegramBot = self.context['telegram_bot']

		if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is None:
			raise serializers.ValidationError(_('Название плагина содержит запрещенные символы!'))

		if telegram_bot.plugins.filter(name=name).exists():
			raise serializers.ValidationError(_('У вас уже добавлен плагин с таким названием!'))

		return name

class UpdatePluginSerializer(serializers.Serializer):
	code = serializers.CharField()

class AddPluginLogSerializer(serializers.Serializer):
	message = serializers.CharField()
	level = serializers.ChoiceField(choices=['info', 'success', 'danger'])
