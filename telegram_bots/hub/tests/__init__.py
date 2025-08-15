from .api_request import APIRequestViewSetTests
from .background_task import BackgroundTaskViewSetTests
from .command import CommandKeyboardButtonViewSetTests, CommandViewSetTests
from .condition import ConditionViewSetTests
from .database_operation import DatabaseOperationViewSetTests
from .database_record import DatabaseRecordViewSetTests
from .telegram_bot import TelegramBotViewSetTests
from .trigger import TriggerViewSetTests
from .user import UserViewSetTests
from .variable import VariableViewSetTests

__all__ = [
    'TelegramBotViewSetTests',
    'CommandViewSetTests',
    'CommandKeyboardButtonViewSetTests',
    'ConditionViewSetTests',
    'BackgroundTaskViewSetTests',
    'APIRequestViewSetTests',
    'DatabaseOperationViewSetTests',
    'TriggerViewSetTests',
    'VariableViewSetTests',
    'UserViewSetTests',
    'DatabaseRecordViewSetTests',
]
