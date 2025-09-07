from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from typing import Any, Final
import re

TEXT_VARIABLE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r'\{\{((?:\s|&nbsp;)*)(\w+(?:(?:\.|(?:\s|&nbsp;)+)\w+)*)((?:\s|&nbsp;)*)\}\}',
    re.IGNORECASE,
)
SYSTEM_TEXT_VARIABLES: Final[set[str]] = {
    'BOT_NAME',
    'BOT_USERNAME',
    'USER_ID',
    'USER_USERNAME',
    'USER_FIRST_NAME',
    'USER_LAST_NAME',
    'USER_FULL_NAME',
    'USER_LANGUAGE_CODE',
    'USER_MESSAGE_ID',
    'USER_MESSAGE_TEXT',
    'USER_MESSAGE_DATE',
}


def _text_variable_replacer(match: re.Match[str]) -> str:
    key: str = match.group(2)

    if '.' in key:
        return match.group()

    leading_spaces, trailing_spaces = match.group(1), match.group(3)
    prefix: str = 'SYSTEM' if key in SYSTEM_TEXT_VARIABLES else 'USER'

    return f'{{{{{leading_spaces}{prefix}.{key}{trailing_spaces}}}}}'


def _update_text_variables(text: str) -> str:
    return TEXT_VARIABLE_PATTERN.sub(_text_variable_replacer, text)


def _process_field_value(value: Any) -> Any:
    if isinstance(value, str):
        return _update_text_variables(value)
    elif isinstance(value, dict):
        return {
            _process_field_value(key): _process_field_value(item)
            for key, item in value.items()
        }
    elif isinstance(value, list):
        return [_process_field_value(item) for item in value]

    return value


def migrate_text_variables(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    migration_model_fields: list[tuple[type[models.Model], list[str]]] = [
        (apps.get_model('telegram_bots', 'TriggerMessage'), ['text']),
        (apps.get_model('telegram_bots', 'CommandMessage'), ['text']),
        (apps.get_model('telegram_bots', 'APIRequest'), ['body']),
        (apps.get_model('telegram_bots', 'DatabaseCreateOperation'), ['data']),
        (
            apps.get_model('telegram_bots', 'DatabaseUpdateOperation'),
            ['lookup_field_name', 'lookup_field_value', 'new_data'],
        ),
    ]

    for model, fields in migration_model_fields:
        update_instances: list[models.Model] = []

        for instance in model.objects.iterator():
            for field in fields:
                field_value: Any | None = getattr(instance, field, None)

                if not field_value:
                    continue

                new_field_value: Any = _process_field_value(field_value)

                if new_field_value != field_value:
                    setattr(instance, field, new_field_value)

            update_instances.append(instance)

        model.objects.bulk_update(update_instances, fields=fields)


class Migration(migrations.Migration):
    dependencies = [
        (
            'telegram_bots',
            '0009_alter_apirequest_body_alter_apirequest_headers_and_more',
        )
    ]
    operations = [
        migrations.RunPython(
            migrate_text_variables, reverse_code=migrations.RunPython.noop
        )
    ]
