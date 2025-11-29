from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import (
    Command,
    CommandDocument,
    CommandImage,
    CommandKeyboard,
    CommandKeyboardButton,
    CommandMessage,
    CommandSettings,
)
from ..models.base import AbstractCommandMedia
from .base import CommandMediaSerializer, DiagramSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from contextlib import suppress
from typing import Any
import os


class CommandSettingsSerializer(serializers.ModelSerializer[CommandSettings]):
    class Meta:
        model = CommandSettings
        fields = ['reply_to_user_message', 'delete_user_message', 'send_as_new_message']


class CommandImageSerializer(CommandMediaSerializer[CommandImage]):
    class Meta(CommandMediaSerializer.Meta):
        model = CommandImage


class CommandDocumentSerializer(CommandMediaSerializer[CommandDocument]):
    class Meta(CommandMediaSerializer.Meta):
        model = CommandDocument


class CommandMessageSerializer(serializers.ModelSerializer[CommandMessage]):
    class Meta:
        model = CommandMessage
        fields = ['text']


class CommandKeyboardButtonSerializer(
    serializers.ModelSerializer[CommandKeyboardButton]
):
    class Meta:
        model = CommandKeyboardButton
        fields = ['id', 'row', 'position', 'text', 'url']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class CommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
    buttons = CommandKeyboardButtonSerializer(many=True)

    class Meta:
        model = CommandKeyboard
        fields = ['type', 'buttons']


class CommandSerializer(TelegramBotMixin, serializers.ModelSerializer[Command]):
    settings = CommandSettingsSerializer()
    images = CommandImageSerializer(many=True, required=False, allow_null=True)
    documents = CommandDocumentSerializer(many=True, required=False, allow_null=True)
    message = CommandMessageSerializer()
    keyboard = CommandKeyboardSerializer(required=False, allow_null=True)

    class Meta:
        model = Command
        fields = [
            'id',
            'name',
            'settings',
            'images',
            'documents',
            'message',
            'keyboard',
        ]

    def _validate_media(self, media: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for data in media:
            if 'id' not in data and ('file' in data) is ('from_url' in data):
                raise serializers.ValidationError(
                    _("Необходимо указать только одно из полей 'file' или 'from_url'."),
                    code='required',
                )

        return media

    def validate_images(self, images: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self._validate_media(images)

    def validate_documents(
        self, documents: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return self._validate_media(documents)

    def validate_keyboard(
        self, keyboard: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if not keyboard:
            return None

        buttons: list[dict[str, Any]] | None = keyboard.get('buttons')

        if not buttons:
            return None

        if (
            len(buttons)
            if not isinstance(self.instance, Command) or not self.partial
            else self.instance.keyboard.buttons.count()
            + sum('id' not in button for button in buttons)
        ) > settings.TELEGRAM_BOT_MAX_COMMAND_KEYBOARD_BUTTONS:
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s кнопок для клавиатуры команды.')
                % {'max': settings.TELEGRAM_BOT_MAX_COMMAND_KEYBOARD_BUTTONS},
                code='max_limit',
            )

        return keyboard

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        images: list[dict[str, Any]] = data.get('images', [])
        documents: list[dict[str, Any]] = data.get('documents', [])

        if images or documents:
            extra_size: int = 0

            for media in images + documents:
                file: Any | None = media.get('file')

                if isinstance(file, UploadedFile):
                    extra_size += file.size or 0

            if extra_size and self.telegram_bot.remaining_storage_size - extra_size < 0:
                raise serializers.ValidationError(
                    _('Превышен лимит хранилища.'), code='max_storage_size_limit'
                )

        if (
            not self.instance
            and self.telegram_bot.commands.count() + 1
            > settings.TELEGRAM_BOT_MAX_COMMANDS
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s команд.')
                % {'max': settings.TELEGRAM_BOT_MAX_COMMANDS},
                code='max_limit',
            )

        return data

    def create_settings(self, command: Command, settings_data: dict[str, Any]) -> None:
        CommandSettings.objects.create(command=command, **settings_data)

    def create_images(
        self, command: Command, images_data: list[dict[str, Any]] | None
    ) -> None:
        if not images_data:
            return

        CommandImage.objects.bulk_create(
            CommandImage(command=command, **image_data) for image_data in images_data
        )

    def create_documents(
        self, command: Command, documents_data: list[dict[str, Any]] | None
    ) -> None:
        if not documents_data:
            return

        CommandDocument.objects.bulk_create(
            CommandDocument(command=command, **document_data)
            for document_data in documents_data
        )

    def create_message(self, command: Command, message_data: dict[str, Any]) -> None:
        CommandMessage.objects.create(command=command, **message_data)

    def create_keyboard(
        self, command: Command, keyboard_data: dict[str, Any] | None
    ) -> None:
        if not keyboard_data or 'buttons' not in keyboard_data:
            return

        buttons_data: list[dict[str, Any]] = keyboard_data.pop('buttons')

        keyboard: CommandKeyboard = CommandKeyboard.objects.create(
            command=command, **keyboard_data
        )

        CommandKeyboardButton.objects.bulk_create(
            CommandKeyboardButton(keyboard=keyboard, **button_data)
            for button_data in buttons_data
        )

    def create(self, validated_data: dict[str, Any]) -> Command:
        settings: dict[str, Any] = validated_data.pop('settings')
        images: list[dict[str, Any]] | None = validated_data.pop('images', None)
        documents: list[dict[str, Any]] | None = validated_data.pop('documents', None)
        message: dict[str, Any] = validated_data.pop('message')
        keyboard: dict[str, Any] | None = validated_data.pop('keyboard', None)

        command: Command = self.telegram_bot.commands.create(**validated_data)

        self.create_settings(command, settings)
        self.create_images(command, images)
        self.create_documents(command, documents)
        self.create_message(command, message)
        self.create_keyboard(command, keyboard)

        return command

    def update_settings(
        self, command: Command, settings_data: dict[str, Any] | None
    ) -> None:
        if not settings_data:
            return

        command.settings.reply_to_user_message = settings_data.get(
            'reply_to_user_message', command.settings.reply_to_user_message
        )
        command.settings.delete_user_message = settings_data.get(
            'delete_user_message', command.settings.delete_user_message
        )
        command.settings.send_as_new_message = settings_data.get(
            'send_as_new_message', command.settings.send_as_new_message
        )
        command.settings.save(
            update_fields=[
                'reply_to_user_message',
                'delete_user_message',
                'send_as_new_message',
            ]
        )

    def _delete_media_files(self, queryset: QuerySet[AbstractCommandMedia]) -> None:
        for file_path in queryset.exclude(file=None).values_list('file', flat=True):  # type: ignore [misc]
            with suppress(OSError):
                os.remove(settings.MEDIA_ROOT / file_path)

    def update_media(
        self,
        command: Command,
        media_model_class: type[AbstractCommandMedia],
        media_data: list[dict[str, Any]] | None,
    ) -> None:
        queryset: QuerySet[AbstractCommandMedia] = getattr(
            command, media_model_class.related_name
        )

        if media_data:
            create_media: list[AbstractCommandMedia] = []
            update_media: list[AbstractCommandMedia] = []

            for item in media_data:
                file: UploadedFile | None = item.get('file')
                from_url: str | None = item.get('from_url')

                try:
                    media: AbstractCommandMedia = queryset.get(id=item['id'])
                    media.position = item.get('position', media.position)

                    if file or from_url:
                        if media.file:
                            media.file.delete()

                        media.file = file
                        media.from_url = from_url

                    update_media.append(media)
                except (KeyError, media_model_class.DoesNotExist):
                    create_media.append(media_model_class(command=command, **item))  # type: ignore [misc]

            new_media: list[AbstractCommandMedia] = (
                media_model_class.objects.bulk_create(  # type: ignore [attr-defined]
                    create_media
                )
            )
            media_model_class.objects.bulk_update(  # type: ignore [attr-defined]
                update_media, fields=['file', 'from_url', 'position']
            )

            if not self.partial:
                new_queryset: QuerySet[AbstractCommandMedia] = queryset.exclude(
                    id__in=[media.id for media in new_media + update_media]  # type: ignore [attr-defined]
                )

                self._delete_media_files(new_queryset)
                new_queryset.delete()
        elif not self.partial:
            self._delete_media_files(queryset)
            queryset.all().delete()

    def update_images(
        self, command: Command, images_data: list[dict[str, Any]] | None
    ) -> None:
        self.update_media(command, CommandImage, images_data)

    def update_documents(
        self, command: Command, documents_data: list[dict[str, Any]] | None
    ) -> None:
        self.update_media(command, CommandDocument, documents_data)

    def update_message(
        self, command: Command, message_data: dict[str, Any] | None
    ) -> None:
        if not message_data:
            return

        command.message.text = message_data.get('text', command.message.text)
        command.message.save(update_fields=['text'])

    def update_keyboard(
        self, command: Command, keyboard_data: dict[str, Any] | None
    ) -> None:
        if keyboard_data:
            try:
                keyboard_type: str = keyboard_data.get('type', command.keyboard.type)

                command.keyboard.type = keyboard_type
                command.keyboard.save(update_fields=['type'])

                create_buttons: list[CommandKeyboardButton] = []
                update_buttons: list[CommandKeyboardButton] = []

                for button_data in keyboard_data.get('buttons', []):
                    try:
                        button: CommandKeyboardButton = command.keyboard.buttons.get(
                            id=button_data['id']
                        )
                        button.row = button_data.get('row', button.row)
                        button.position = button_data.get('position', button.position)
                        button.text = button_data.get('text', button.text)
                        button.url = (
                            button_data.get('url', button.url)
                            if keyboard_type != 'default'
                            else None
                        )

                        update_buttons.append(button)
                    except (KeyError, CommandKeyboardButton.DoesNotExist):
                        if keyboard_type != 'default':
                            button_data['url'] = None

                        create_buttons.append(
                            CommandKeyboardButton(
                                keyboard=command.keyboard, **button_data
                            )
                        )

                new_buttons: list[CommandKeyboardButton] = (
                    CommandKeyboardButton.objects.bulk_create(create_buttons)
                )
                CommandKeyboardButton.objects.bulk_update(
                    update_buttons, fields=['row', 'position', 'text', 'url']
                )

                if not self.partial:
                    command.keyboard.buttons.exclude(
                        id__in=[button.id for button in new_buttons + update_buttons]
                    ).delete()
            except CommandKeyboard.DoesNotExist:
                self.create_keyboard(command, keyboard_data)
        elif not self.partial:
            with suppress(CommandKeyboard.DoesNotExist):
                command.keyboard.delete()

    def update(self, command: Command, validated_data: dict[str, Any]) -> Command:
        command.name = validated_data.get('name', command.name)
        command.save(update_fields=['name'])

        self.update_settings(command, validated_data.get('settings'))
        self.update_images(command, validated_data.get('images'))
        self.update_documents(command, validated_data.get('documents'))
        self.update_message(command, validated_data.get('message'))
        self.update_keyboard(command, validated_data.get('keyboard'))

        command.refresh_from_db(fields=['keyboard'])

        return command


class DiagramCommandKeyboardButtonSerializer(
    serializers.ModelSerializer[CommandKeyboardButton]
):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = CommandKeyboardButton
        fields = ['id', 'row', 'position', 'text', 'url', 'source_connections']


class DiagramCommandKeyboardSerializer(serializers.ModelSerializer[CommandKeyboard]):
    buttons = DiagramCommandKeyboardButtonSerializer(many=True)

    class Meta:
        model = CommandKeyboard
        fields = ['type', 'buttons']


class DiagramCommandSerializer(DiagramSerializer[Command]):
    message = CommandMessageSerializer(read_only=True)
    keyboard = DiagramCommandKeyboardSerializer(allow_null=True, read_only=True)
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Command
        fields = [
            'id',
            'name',
            'message',
            'keyboard',
            'source_connections',
            'target_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name']
