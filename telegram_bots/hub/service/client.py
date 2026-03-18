from requests_unixsocket import Session
from yarl import URL

from requests import RequestException, Response
import requests

from http import HTTPMethod
from typing import Any


class ServiceClient:
    def __init__(self, url: str, access_token: str) -> None:
        self.url = URL(url)
        self.headers = {'X-API-KEY': access_token}
        self.session = Session()

    def _request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Any | None = None,
    ) -> Response | None:
        try:
            response: Response = requests.request(
                method,
                str(self.url / endpoint),
                headers=self.headers,
                json=data,
            )
            response.raise_for_status()
        except RequestException:
            return None

        return response

    def get_telegram_bot_ids(self) -> list[int]:
        response: Response | None = self._request(HTTPMethod.GET, 'bots/')
        return response.json() if response and response.ok else []

    def start_telegram_bot(self, bot_id: int, bot_token: str) -> bool:
        return (
            self._request(
                HTTPMethod.POST, f'bots/{bot_id}/start/', data={'bot_token': bot_token}
            )
            is not None
        )

    def restart_telegram_bot(self, bot_id: int) -> bool:
        return self._request(HTTPMethod.POST, f'bots/{bot_id}/restart/') is not None

    def stop_telegram_bot(self, bot_id: int) -> bool:
        return self._request(HTTPMethod.POST, f'bots/{bot_id}/stop/') is not None
