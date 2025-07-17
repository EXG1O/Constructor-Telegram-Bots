from .background_task import (
    BackgroundTaskViewSetTests,
    DiagramBackgroundTaskViewSetTests,
)
from .command import CommandViewSetTests, DiagramCommandViewSetTests
from .condition import ConditionViewSetTests, DiagramConditionViewSetTests
from .connection import ConnectionViewSetTests
from .database_record import DatabaseRecordViewSetTests
from .stats import StatsAPIViewTests
from .telegram_bot import TelegramBotViewSetTests
from .user import UserViewSetTests
from .variable import VariableViewSetTests

__all__ = [
    'StatsAPIViewTests',
    'TelegramBotViewSetTests',
    'ConnectionViewSetTests',
    'CommandViewSetTests',
    'DiagramCommandViewSetTests',
    'ConditionViewSetTests',
    'DiagramConditionViewSetTests',
    'BackgroundTaskViewSetTests',
    'DiagramBackgroundTaskViewSetTests',
    'VariableViewSetTests',
    'UserViewSetTests',
    'DatabaseRecordViewSetTests',
]
