from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class APIRequestMethod(TextChoices):
    GET = 'get', 'GET'
    POST = 'post', 'POST'
    PUT = 'put', 'PUT'
    PATCH = 'patch', 'PATCH'
    DELETE = 'delete', 'DELETE'


class ConnectionHandlePosition(TextChoices):
    LEFT = 'left', _('Слева')
    RIGHT = 'right', _('Справа')


class ConnectionObjectType(TextChoices):
    TRIGGER = 'trigger', _('Триггер')
    COMMAND = 'command', _('Команда')
    COMMAND_KEYBOARD_BUTTON = 'command_keyboard_button', _('Кнопка клавиатуры')
    CONDITION = 'condition', _('Условие')
    BACKGROUND_TASK = 'background_task', _('Фоновая задача')
    API_REQUEST = 'api_request', _('API-запрос')
    DATABASE_OPERATION = 'database_operation', _('Операция базы данных')

    @staticmethod
    def source_choices() -> list[tuple[str, str]]:
        return [
            (item.value, item.label)
            for item in [
                ConnectionObjectType.TRIGGER,
                ConnectionObjectType.COMMAND,
                ConnectionObjectType.COMMAND_KEYBOARD_BUTTON,
                ConnectionObjectType.CONDITION,
                ConnectionObjectType.BACKGROUND_TASK,
                ConnectionObjectType.API_REQUEST,
                ConnectionObjectType.DATABASE_OPERATION,
            ]
        ]

    @staticmethod
    def target_choices() -> list[tuple[str, str]]:
        return [
            (item.value, item.label)
            for item in [
                ConnectionObjectType.TRIGGER,
                ConnectionObjectType.COMMAND,
                ConnectionObjectType.CONDITION,
                ConnectionObjectType.API_REQUEST,
                ConnectionObjectType.DATABASE_OPERATION,
            ]
        ]


class KeyboardType(TextChoices):
    DEFAULT = 'default', _('Обычный')
    INLINE = 'inline', _('Встроенный')
    PAYMENT = 'payment', _('Платёжный')


class ConditionPartType(TextChoices):
    POSITIVE = '+', _('Положительный')
    NEGATIVE = '-', _('Отрицательный')


class ConditionPartOperatorType(TextChoices):
    EQUAL = '==', _('Равно')
    NOT_EQUAL = '!=', _('Не равно')
    GREATER = '>', _('Больше')
    GREATER_OR_EQUAL = '>=', _('Больше или равно')
    LESS = '<', _('Меньше')
    LESS_OR_EQUAL = '<=', _('Меньше или равно')


class ConditionPartNextPartOperator(TextChoices):
    AND = '&&', _('И')
    OR = '||', _('ИЛИ')


class BackgroundTaskInterval(IntegerChoices):
    DAY_1 = 1, _('1 день')
    DAYS_3 = 3, _('3 дня')
    DAYS_7 = 7, _('7 дней')
    DAYS_14 = 14, _('14 дней')
    DAYS_28 = 28, _('28 дней')
