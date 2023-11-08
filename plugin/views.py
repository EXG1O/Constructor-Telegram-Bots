from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from telegram_bot.models import TelegramBot
from telegram_bot.decorators import check_telegram_bot_id

from .models import Plugin, PluginLog
from .decorators import check_plugin_id
from .serializers import (
	PluginModelSerializer,
	PluginLogModelSerializer,
	CreatePluginSerializer,
	UpdatePluginSerializer,
	AddPluginLogSerializer,
)

from constructor_telegram_bots.environment import delete_plugin as env_delete_plugin


class PluginsView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_telegram_bot_id
	def post(self, request: Request, telegram_bot: TelegramBot) -> Response:
		serializer = CreatePluginSerializer(data=request.data, context={'telegram_bot': telegram_bot})
		serializer.is_valid(raise_exception=True)

		plugin: Plugin = Plugin.objects.create(
			user=request.user,
			telegram_bot=telegram_bot,
			**serializer.validated_data
		)

		return Response({
			'message': _('Вы успешно добавили плагин вашему Telegram боту.'),
			'level': 'success',

			'plugin': PluginModelSerializer(plugin).data,
		})

	@check_telegram_bot_id
	def get(self, request: Request, telegram_bot: TelegramBot) -> Response:
		return Response(PluginModelSerializer(telegram_bot.plugins.all(), many=True).data)

class PluginView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	@check_plugin_id
	def patch(self, request: Request, plugin: Plugin) -> Response:
		serializer = UpdatePluginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		plugin.is_checked = False
		plugin.code = serializer.validated_data['code']
		plugin.save()

		env_delete_plugin(plugin)

		return Response({
			'message': _('Вы успешно обновили плагин вашего Telegram бота.'),
			'level': 'success',

			'plugin': PluginModelSerializer(plugin).data,
		})

	@check_plugin_id
	def delete(self, request: Request, plugin: Plugin) -> Response:
		plugin.delete()

		return Response({
			'message': _('Вы успешно удалили плагин вашего Telegram бота.'),
			'level': 'success',
		})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_telegram_bot_id
def get_plugins_logs_view(request: Request, telegram_bot: TelegramBot) -> Response:
	return Response(PluginLogModelSerializer([plugin_log for plugin in telegram_bot.plugins.all() for plugin_log in plugin.logs.all()], many=True).data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@check_plugin_id
def add_plugin_log_view(request: Request, plugin: Plugin) -> Response:
	serializer = AddPluginLogSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)

	PluginLog.objects.create(
		user=request.user,
		telegram_bot=plugin.telegram_bot,
		plugin=plugin,
		**serializer.validated_data
	)

	return Response({
		'message': None,
		'level': 'success',
	})
