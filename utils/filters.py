from django.template import defaultfilters as django_filters

from datetime import datetime as datetime_


def datetime(value: datetime_ | str | None) -> str:
	return f'{django_filters.date(value)} {django_filters.time(value)}'