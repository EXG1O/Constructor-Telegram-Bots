from .api_request import APIRequestViewSetTests
from .background_task import BackgroundTaskViewSetTests
from .condition import ConditionViewSetTests
from .database_operation import DatabaseOperationViewSetTests
from .database_record import DatabaseRecordViewSetTests
from .message import MessageKeyboardButtonViewSetTests, MessageViewSetTests
from .telegram_bot import TelegramBotViewSetTests
from .trigger import TriggerViewSetTests
from .user import UserViewSetTests
from .variable import VariableViewSetTests

__all__ = [
    'TelegramBotViewSetTests',
    'MessageViewSetTests',
    'MessageKeyboardButtonViewSetTests',
    'ConditionViewSetTests',
    'BackgroundTaskViewSetTests',
    'APIRequestViewSetTests',
    'DatabaseOperationViewSetTests',
    'TriggerViewSetTests',
    'VariableViewSetTests',
    'UserViewSetTests',
    'DatabaseRecordViewSetTests',
]
