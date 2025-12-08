from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from rest_framework import serializers

from ..models import (
    Message,
    MessageDocument,
    MessageImage,
    MessageKeyboard,
    MessageKeyboardButton,
    MessageSettings,
)
from ..models.base import AbstractMessageMedia
from .base import DiagramSerializer, MessageMediaSerializer
from .connection import ConnectionSerializer
from .mixins import TelegramBotMixin

from contextlib import suppress
from typing import Any, cast
import os


class MessageSettingsSerializer(serializers.ModelSerializer[MessageSettings]):
    class Meta:
        model = MessageSettings
        fields = ['reply_to_user_message', 'delete_user_message', 'send_as_new_message']


class MessageImageSerializer(MessageMediaSerializer[MessageImage]):
    class Meta(MessageMediaSerializer.Meta):
        model = MessageImage


class MessageDocumentSerializer(MessageMediaSerializer[MessageDocument]):
    class Meta(MessageMediaSerializer.Meta):
        model = MessageDocument


class MessageKeyboardButtonSerializer(
    serializers.ModelSerializer[MessageKeyboardButton]
):
    class Meta:
        model = MessageKeyboardButton
        fields = ['id', 'row', 'position', 'text', 'url']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MessageKeyboardSerializer(serializers.ModelSerializer[MessageKeyboard]):
    buttons = MessageKeyboardButtonSerializer(many=True)

    class Meta:
        model = MessageKeyboard
        fields = ['type', 'buttons']


class MessageSerializer(TelegramBotMixin, serializers.ModelSerializer[Message]):
    settings = MessageSettingsSerializer()
    images = MessageImageSerializer(many=True, required=False, allow_null=True)
    documents = MessageDocumentSerializer(many=True, required=False, allow_null=True)
    keyboard = MessageKeyboardSerializer(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'name',
            'text',
            'settings',
            'images',
            'documents',
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
            if not isinstance(self.instance, Message) or not self.partial
            else self.instance.keyboard.buttons.count()
            + sum('id' not in button for button in buttons)
        ) > settings.TELEGRAM_BOT_MAX_MESSAGE_KEYBOARD_BUTTONS:
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s кнопок для клавиатуры сообщения.')
                % {'max': settings.TELEGRAM_BOT_MAX_MESSAGE_KEYBOARD_BUTTONS},
                code='max_limit',
            )

        return keyboard

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        message = cast(Message | None, self.instance)

        has_text: bool = bool(data.get('text', message.text if message else None))
        has_images: bool = bool(
            data.get('images', message.images.count() if message else None)
        )
        has_documents: bool = bool(
            data.get('documents', message.documents.count() if message else None)
        )
        has_keyboard: bool = 'keyboard' in data

        if message and not has_keyboard:
            with suppress(MessageKeyboard.DoesNotExist):
                has_keyboard = bool(message.keyboard)

        if not any([has_text, has_images, has_documents, has_keyboard]):
            raise serializers.ValidationError(
                _(
                    "Необходимо указать минимум одно из полей: 'text', 'images', "
                    "'documents' или 'keyboard'."
                ),
                code='required',
            )

        if has_keyboard and not has_text:
            raise serializers.ValidationError(
                _(
                    "Необходимо указать поле 'text', если указано значение для "
                    "поля 'keyboard'."
                ),
                code='required',
            )

        images: list[dict[str, Any]] | None = data.get('images')
        documents: list[dict[str, Any]] | None = data.get('documents')

        if images or documents:
            extra_size: int = 0

            for media in (images or []) + (documents or []):
                file: Any | None = media.get('file')

                if isinstance(file, UploadedFile):
                    extra_size += file.size or 0

            if extra_size and self.telegram_bot.remaining_storage_size - extra_size < 0:
                raise serializers.ValidationError(
                    _('Превышен лимит хранилища.'), code='max_storage_size_limit'
                )

        if (
            not self.instance
            and self.telegram_bot.messages.count() + 1
            > settings.TELEGRAM_BOT_MAX_MESSAGES
        ):
            raise serializers.ValidationError(
                _('Нельзя добавлять больше %(max)s сообщений.')
                % {'max': settings.TELEGRAM_BOT_MAX_MESSAGES},
                code='max_limit',
            )

        return data

    def create_settings(self, message: Message, settings_data: dict[str, Any]) -> None:
        MessageSettings.objects.create(message=message, **settings_data)

    def create_images(
        self, message: Message, images_data: list[dict[str, Any]] | None
    ) -> None:
        if not images_data:
            return

        MessageImage.objects.bulk_create(
            MessageImage(message=message, **image_data) for image_data in images_data
        )

    def create_documents(
        self, message: Message, documents_data: list[dict[str, Any]] | None
    ) -> None:
        if not documents_data:
            return

        MessageDocument.objects.bulk_create(
            MessageDocument(message=message, **document_data)
            for document_data in documents_data
        )

    def create_keyboard(
        self, message: Message, keyboard_data: dict[str, Any] | None
    ) -> None:
        if not keyboard_data or 'buttons' not in keyboard_data:
            return

        buttons_data: list[dict[str, Any]] = keyboard_data.pop('buttons')

        keyboard: MessageKeyboard = MessageKeyboard.objects.create(
            message=message, **keyboard_data
        )

        MessageKeyboardButton.objects.bulk_create(
            MessageKeyboardButton(keyboard=keyboard, **button_data)
            for button_data in buttons_data
        )

    def create(self, validated_data: dict[str, Any]) -> Message:
        settings: dict[str, Any] = validated_data.pop('settings')
        images: list[dict[str, Any]] | None = validated_data.pop('images', None)
        documents: list[dict[str, Any]] | None = validated_data.pop('documents', None)
        keyboard: dict[str, Any] | None = validated_data.pop('keyboard', None)

        message: Message = self.telegram_bot.messages.create(**validated_data)

        self.create_settings(message, settings)
        self.create_images(message, images)
        self.create_documents(message, documents)
        self.create_keyboard(message, keyboard)

        return message

    def update_settings(
        self, message: Message, settings_data: dict[str, Any] | None
    ) -> None:
        if not settings_data:
            return

        message.settings.reply_to_user_message = settings_data.get(
            'reply_to_user_message', message.settings.reply_to_user_message
        )
        message.settings.delete_user_message = settings_data.get(
            'delete_user_message', message.settings.delete_user_message
        )
        message.settings.send_as_new_message = settings_data.get(
            'send_as_new_message', message.settings.send_as_new_message
        )
        message.settings.save(
            update_fields=[
                'reply_to_user_message',
                'delete_user_message',
                'send_as_new_message',
            ]
        )

    def _delete_media_files(self, queryset: QuerySet[AbstractMessageMedia]) -> None:
        for file_path in queryset.exclude(file=None).values_list('file', flat=True):  # type: ignore [misc]
            with suppress(OSError):
                os.remove(settings.MEDIA_ROOT / file_path)

    def update_media(
        self,
        message: Message,
        media_model_class: type[AbstractMessageMedia],
        media_data: list[dict[str, Any]] | None,
    ) -> None:
        queryset: QuerySet[AbstractMessageMedia] = getattr(
            message, media_model_class.related_name
        )

        if media_data:
            create_media: list[AbstractMessageMedia] = []
            update_media: list[AbstractMessageMedia] = []

            for item in media_data:
                file: UploadedFile | None = item.get('file')
                from_url: str | None = item.get('from_url')

                try:
                    media: AbstractMessageMedia = queryset.get(id=item['id'])
                    media.position = item.get('position', media.position)

                    if file or from_url:
                        if media.file:
                            media.file.delete()

                        media.file = file
                        media.from_url = from_url

                    update_media.append(media)
                except (KeyError, media_model_class.DoesNotExist):
                    create_media.append(media_model_class(message=message, **item))  # type: ignore [misc]

            new_media: list[AbstractMessageMedia] = (
                media_model_class.objects.bulk_create(  # type: ignore [attr-defined]
                    create_media
                )
            )
            media_model_class.objects.bulk_update(  # type: ignore [attr-defined]
                update_media, fields=['file', 'from_url', 'position']
            )

            if not self.partial:
                new_queryset: QuerySet[AbstractMessageMedia] = queryset.exclude(
                    id__in=[media.id for media in new_media + update_media]  # type: ignore [attr-defined]
                )

                self._delete_media_files(new_queryset)
                new_queryset.delete()
        elif not self.partial:
            self._delete_media_files(queryset)
            queryset.all().delete()

    def update_images(
        self, message: Message, images_data: list[dict[str, Any]] | None
    ) -> None:
        self.update_media(message, MessageImage, images_data)

    def update_documents(
        self, message: Message, documents_data: list[dict[str, Any]] | None
    ) -> None:
        self.update_media(message, MessageDocument, documents_data)

    def update_keyboard(
        self, message: Message, keyboard_data: dict[str, Any] | None
    ) -> None:
        if keyboard_data:
            try:
                keyboard_type: str = keyboard_data.get('type', message.keyboard.type)

                message.keyboard.type = keyboard_type
                message.keyboard.save(update_fields=['type'])

                create_buttons: list[MessageKeyboardButton] = []
                update_buttons: list[MessageKeyboardButton] = []

                for button_data in keyboard_data.get('buttons', []):
                    try:
                        button: MessageKeyboardButton = message.keyboard.buttons.get(
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
                    except (KeyError, MessageKeyboardButton.DoesNotExist):
                        if keyboard_type != 'default':
                            button_data['url'] = None

                        create_buttons.append(
                            MessageKeyboardButton(
                                keyboard=message.keyboard, **button_data
                            )
                        )

                new_buttons: list[MessageKeyboardButton] = (
                    MessageKeyboardButton.objects.bulk_create(create_buttons)
                )
                MessageKeyboardButton.objects.bulk_update(
                    update_buttons, fields=['row', 'position', 'text', 'url']
                )

                if not self.partial:
                    message.keyboard.buttons.exclude(
                        id__in=[button.id for button in new_buttons + update_buttons]
                    ).delete()
            except MessageKeyboard.DoesNotExist:
                self.create_keyboard(message, keyboard_data)
        elif not self.partial:
            with suppress(MessageKeyboard.DoesNotExist):
                message.keyboard.delete()

    def update(self, message: Message, validated_data: dict[str, Any]) -> Message:
        message.name = validated_data.get('name', message.name)
        message.text = validated_data.get('text', message.text)
        message.save(update_fields=['name', 'text'])

        self.update_settings(message, validated_data.get('settings'))
        self.update_images(message, validated_data.get('images'))
        self.update_documents(message, validated_data.get('documents'))
        self.update_keyboard(message, validated_data.get('keyboard'))

        message.refresh_from_db(fields=['keyboard'])

        return message


class DiagramMessageKeyboardButtonSerializer(
    serializers.ModelSerializer[MessageKeyboardButton]
):
    source_connections = ConnectionSerializer(many=True)

    class Meta:
        model = MessageKeyboardButton
        fields = ['id', 'row', 'position', 'text', 'url', 'source_connections']


class DiagramMessageKeyboardSerializer(serializers.ModelSerializer[MessageKeyboard]):
    buttons = DiagramMessageKeyboardButtonSerializer(many=True)

    class Meta:
        model = MessageKeyboard
        fields = ['type', 'buttons']


class DiagramMessageSerializer(DiagramSerializer[Message]):
    keyboard = DiagramMessageKeyboardSerializer(allow_null=True, read_only=True)
    source_connections = ConnectionSerializer(many=True, read_only=True)
    target_connections = ConnectionSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'name',
            'text',
            'keyboard',
            'source_connections',
            'target_connections',
        ] + DiagramSerializer.Meta.fields
        read_only_fields = ['name', 'text']
