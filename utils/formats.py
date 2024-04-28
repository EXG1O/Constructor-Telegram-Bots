from django.utils.formats import date_format, time_format

from datetime import datetime


def date_time_format(value: datetime | str) -> str:
	return f'{date_format(value)} {time_format(value)}'
