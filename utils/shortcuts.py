import random


def generate_random_string(chars: str, length: int) -> str:
	return ''.join(random.choices(chars, k=length))
