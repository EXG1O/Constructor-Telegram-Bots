from django.template import defaultfilters as django_filters

from datetime import datetime as _datetime


def datetime(value: _datetime | str | None) -> str:
	return f'{django_filters.date(value)} {django_filters.time(value)}'