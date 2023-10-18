import random


def generate_random_string(length: int, chars: str) -> str:
	return ''.join([random.choice(chars) for _ in range(length)])
