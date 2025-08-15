from django.core.management.base import BaseCommand

from ...models import TelegramBotsHub

from typing import Any
import secrets


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        url: str = input('Enter a microservice URL: ')

        service_token: str = secrets.token_hex(32)
        microservice_token: str = secrets.token_hex(32)

        hub = TelegramBotsHub(
            url=url,
            service_token=service_token,
            microservice_token=microservice_token,
        )
        hub.clean_fields()
        hub.save()

        self.stdout.write(f'Token for microservice authorization: {service_token}')
        self.stdout.write(f"{'Microservice token:':37} {microservice_token}")
