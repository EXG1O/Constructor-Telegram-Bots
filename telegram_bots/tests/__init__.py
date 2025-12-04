from .api_request import APIRequestViewSetTests, DiagramAPIRequestViewSetTests
from .background_task import (
    BackgroundTaskViewSetTests,
    DiagramBackgroundTaskViewSetTests,
)
from .condition import ConditionViewSetTests, DiagramConditionViewSetTests
from .connection import ConnectionViewSetTests
from .database_operation import (
    DatabaseOperationViewSetTests,
    DiagramDatabaseOperationViewSetTests,
)
from .database_record import DatabaseRecordViewSetTests
from .message import DiagramMessageViewSetTests, MessageViewSetTests
from .stats import StatsAPIViewTests
from .telegram_bot import TelegramBotViewSetTests
from .trigger import DiagramTriggerViewSetTests, TriggerViewSetTests
from .user import UserViewSetTests
from .variable import VariableViewSetTests

__all__ = [
    'StatsAPIViewTests',
    'TelegramBotViewSetTests',
    'ConnectionViewSetTests',
    'MessageViewSetTests',
    'DiagramMessageViewSetTests',
    'ConditionViewSetTests',
    'DiagramConditionViewSetTests',
    'BackgroundTaskViewSetTests',
    'DiagramBackgroundTaskViewSetTests',
    'APIRequestViewSetTests',
    'DiagramAPIRequestViewSetTests',
    'DatabaseOperationViewSetTests',
    'DiagramDatabaseOperationViewSetTests',
    'TriggerViewSetTests',
    'DiagramTriggerViewSetTests',
    'VariableViewSetTests',
    'UserViewSetTests',
    'DatabaseRecordViewSetTests',
]
