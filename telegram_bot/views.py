from django.utils.translation import gettext as _
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.views import APIView
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
import json


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

	def post(self, request: Request) -> Response:
		if not settings.TEST:
			telegram_bot: TelegramBot = getattr(request, 'telegram_bot')
			action: str | None = request.query_params.get('action')

			if action == 'start':
				start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)
			elif action == 'stop':
				telegram_bot.stop()

		return CustomResponse()

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
		images: list[InMemoryUploadedFile] = []
		files: list[InMemoryUploadedFile] = []

		for key in request.FILES:
			if key.split(':')[0] == 'image':
				images.append(request.FILES[key])
			elif key.split(':')[0] == 'file':
				files.append(request.FILES[key])

		data: dict[str, Any] = json.loads(request.data.get('data', '{}'))
		data['images'] = images
		data['files'] = files

		serializer = CreateTelegramBotCommandSerializer(data=data)
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
		images: list[InMemoryUploadedFile] = []
		images_id: list[int] = []

		files: list[InMemoryUploadedFile] = []
		files_id: list[int] = []

		for key in request.data:
			if key.split(':')[0] == 'image':
				image: InMemoryUploadedFile | str = request.data[key]

				if isinstance(image, InMemoryUploadedFile):
					images.append(image)
				elif image.isdigit():
					images_id.append(int(image))
			elif key.split(':')[0] == 'file':
				file: InMemoryUploadedFile | str = request.data[key]

				if isinstance(file, InMemoryUploadedFile):
					files.append(file)
				elif file.isdigit():
					files_id.append(int(file))

		data: dict[str, Any] = json.loads(request.data.get('data', '{}'))
		data['images'] = images
		data['files'] = files

		serializer = UpdateTelegramBotCommandSerializer(data=data)
		serializer.is_valid(raise_exception=True)

		validated_data: dict[str, Any] = serializer.validated_data
		validated_data['images_id'] = images_id
		validated_data['files_id'] = files_id

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')
		telegram_bot_command.update(**validated_data)

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

	def patch(self, request: Request) -> CustomResponse:
		serializer = UpdateTelegramBotCommandDiagramPositionSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		telegram_bot_command: TelegramBotCommand = getattr(request, 'telegram_bot_command')

		validated_data: dict[str, Any] = serializer.validated_data
		x: int = validated_data['x']
		y: int = validated_data['y']

		telegram_bot_command.x = x
		telegram_bot_command.y = y
		telegram_bot_command.save()

		return CustomResponse()

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

class TelegramBotBlockedUserAPIView(APIView):
	authentication_classes = [CookiesTokenAuthentication]
	permission_classes = [IsAuthenticated & TelegramBotUserIsFound]

	def post(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.is_blocked = True
		telegram_bot_user.save()

		return CustomResponse(_('Вы успешно добавили пользователя в список заблокированных пользователей Telegram бота.'))

	def delete(self, request: Request) -> CustomResponse:
		telegram_bot_user: TelegramBotUser = getattr(request, 'telegram_bot_user')
		telegram_bot_user.is_blocked = False
		telegram_bot_user.save()

		return CustomResponse(_('Вы успешно удалили пользователя из списка заблокированных пользователей Telegram бота.'))