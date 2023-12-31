from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from constructor_telegram_bots.authentication import CookiesTokenAuthentication
from utils.drf import CustomResponse

from .models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboardButton,
	TelegramBotUser,
)
from .permissions import (
	TelegramBotIsFound,
	TelegramBotCommandIsFound,
	TelegramBotUserIsFound,
)
from .serializers import (
	TelegramBotSerializer,
	TelegramBotCommandModelSerializer,
	TelegramBotCommandDiagramSerializer,
	TelegramBotUserSerializer,
	CreateTelegramBotSerializer,
	UpdateTelegramBotSerializer,
	CreateTelegramBotCommandSerializer,
	UpdateTelegramBotCommandSerializer,
	ConnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer,
	UpdateTelegramBotCommandDiagramPositionSerializer,
)
from .tasks import start_telegram_bot

from typing import Any


class TelegramBotsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request: Request) -> Response:
		return Response(
			TelegramBotSerializer(
				request.user.telegram_bots.all(), # type: ignore [union-attr]
				many=True,
			).data
		)

	def post(self, request: Request) -> CustomResponse:
		serializer = CreateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = TelegramBot.objects.create(owner=request.user, **serializer.validated_data) # type: ignore [misc]

		return CustomResponse(
			_('Вы успешно добавили Telegram бота.'),
			data={'telegram_bot': TelegramBotSerializer(telegram_bot).data},
		)

class TelegramBotAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(TelegramBotSerializer(telegram_bot).data)

	def patch(self, request: Request) -> CustomResponse:
		serializer = UpdateTelegramBotSerializer(data=request.data, context={'user': request.user})
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		validated_data: dict[str, Any] = serializer.validated_data
		api_token: str | None = validated_data['api_token']
		is_private: bool | None = validated_data['is_private']

		if api_token is not None:
			telegram_bot.api_token = api_token
			telegram_bot.is_running = False
			telegram_bot.update_username()
			telegram_bot.save()

			return CustomResponse(
				_('Вы успешно изменили API-токен Telegram бота.'),
				data={'telegram_bot': TelegramBotSerializer(telegram_bot).data},
			)
		elif is_private is not None:
			telegram_bot.is_private = is_private
			telegram_bot.save()

			return CustomResponse(
				_('Вы успешно сделали Telegram бота%(status)s приватным.') % {'status': ('' if is_private else ' не')},
				data={'telegram_bot': TelegramBotSerializer(telegram_bot).data},
			)
		else:
			return CustomResponse(_('На стороне сайта произошла непредвиденная ошибка, попробуйте ещё раз позже!'), status=500)

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
		telegram_bot.delete()

		return CustomResponse(_('Вы успешно удалили Telegram бота.'))

@api_view(['POST'])
@authentication_classes([CookiesTokenAuthentication])
@permission_classes([IsAuthenticated & TelegramBotIsFound])
def start_or_stop_telegram_bot_api_view(request: Request) -> CustomResponse:
	if not settings.TEST:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		if not telegram_bot.is_running and telegram_bot.is_stopped:
			start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)
		elif telegram_bot.is_running and not telegram_bot.is_stopped:
			telegram_bot.stop()

	return CustomResponse()

class TelegramBotCommandsAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotCommandModelSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

	def post(self, request: Request) -> CustomResponse:
		serializer = CreateTelegramBotCommandSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		TelegramBotCommand.objects.create(telegram_bot=telegram_bot, **serializer.validated_data)

		return CustomResponse(_('Вы успешно добавили команду Telegram боту.'))

class TelegramBotCommandAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		return Response(TelegramBotCommandModelSerializer(telegram_bot_command).data)

	def patch(self, request: Request) -> CustomResponse:
		serializer = UpdateTelegramBotCommandSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')
		telegram_bot_command.update(**serializer.validated_data)

		return CustomResponse(_('Вы успешно изменили команду Telegram бота.'))

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')
		telegram_bot_command.delete()

		return CustomResponse(_('Вы успешно удалили команду Telegram бота.'))

class TelegramBotCommandsDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotCommandDiagramSerializer(
				telegram_bot.commands.all(),
				many=True,
			).data
		)

class TelegramBotCommandDiagramAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotCommandIsFound]

	def post(self, request: Request) -> CustomResponse:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		serializer = ConnectTelegramBotCommandDiagramKeyboardButtonSerializer(
			data=request.data,
			context={
				'telegram_bot': telegram_bot,
				'telegram_bot_command': telegram_bot_command,
			},
		)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		telegram_bot_command_keyboard_button_id: int = validated_data['telegram_bot_command_keyboard_button_id']
		telegram_bot_command_id: int = validated_data['telegram_bot_command_id']
		start_diagram_connector: str = validated_data['start_diagram_connector']
		end_diagram_connector: str = validated_data['end_diagram_connector']

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = telegram_bot_command.keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id)
		telegram_bot_command_keyboard_button.telegram_bot_command = telegram_bot.commands.get(id=telegram_bot_command_id)
		telegram_bot_command_keyboard_button.start_diagram_connector = start_diagram_connector
		telegram_bot_command_keyboard_button.end_diagram_connector = end_diagram_connector
		telegram_bot_command_keyboard_button.save()

		return CustomResponse(_('Вы успешно подключили кнопку клавиатуры к другой команде'))

	def patch(self, request: Request) -> Response:
		serializer = UpdateTelegramBotCommandDiagramPositionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		validated_data: dict[str, Any] = serializer.validated_data
		x: int = validated_data['x']
		y: int = validated_data['y']

		telegram_bot_command.x = x
		telegram_bot_command.y = y
		telegram_bot_command.save()

		return Response({})

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		serializer = DisconnectTelegramBotCommandDiagramKeyboardButtonSerializer(
			data=request.data,
			context={'telegram_bot_command': telegram_bot_command},
		)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		telegram_bot_command_keyboard_button_id: int = validated_data['telegram_bot_command_keyboard_button_id']

		telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = telegram_bot_command.keyboard.buttons.get(id=telegram_bot_command_keyboard_button_id)
		telegram_bot_command_keyboard_button.telegram_bot_command = None
		telegram_bot_command_keyboard_button.start_diagram_connector = None
		telegram_bot_command_keyboard_button.end_diagram_connector = None
		telegram_bot_command_keyboard_button.save()

		return CustomResponse(_('Вы успешно отсоединили кнопку клавиатуры от другой команды'))

class TelegramBotUsersAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot: TelegramBot = getattr(request, 'telegram_bot')

		return Response(
			TelegramBotUserSerializer(
				telegram_bot.users.all(),
				many=True,
			).data
		)

class TelegramBotUserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotIsFound & TelegramBotUserIsFound]

	def get(self, request: Request) -> Response:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')

		return Response(TelegramBotUserSerializer(telegram_bot_user).data)

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.delete()

		return CustomResponse(_('Вы успешно удалили пользователя Telegram бота.'))

class TelegramBotAllowedUserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotUserIsFound]

	def post(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.is_allowed = True
		telegram_bot_user.save()

		return CustomResponse(_('Вы успешно добавили пользователя в список разрешённых пользователей Telegram бота.'))

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.is_allowed = False
		telegram_bot_user.save()

		return CustomResponse(_('Вы успешно удалили пользователя из списка разрешённых пользователей Telegram бота.'))