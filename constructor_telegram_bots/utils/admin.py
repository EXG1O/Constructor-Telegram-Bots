from django.utils.html import format_html


def format_html_url(url: str, text: str | None = None) -> str:
	if text is None:
		text = url

	return format_html(f'<a href="{url}" target="_blank" style="font-weight: 600;">{text}</a>')
