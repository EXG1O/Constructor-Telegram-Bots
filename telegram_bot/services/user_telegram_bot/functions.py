from typing import Any


async def replace_string_variables(text: str, variables: dict[str, Any]) -> str:
	return text