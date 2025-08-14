from yarl import URL

from .adapters import UnixHTTPAdapter
from .schemas import StartTelegramBot

from requests import RequestException, Response, Session
import requests

from typing import Any, Literal


class API:
    def __init__(self, url: str, access_token: str) -> None:
        self.url = URL(url)
        self.headers = {'X-API-KEY': access_token}

        self.session = Session()
        self.session.mount('http+unix://', UnixHTTPAdapter())

    def _request(
        self,
        method: Literal['get', 'post', 'patch', 'put', 'delete'],
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

            return response
        except RequestException:
            return None

    def get_telegram_bot_ids(self) -> list[int]:
        response: Response | None = self._request('get', 'bots/')
        return response.json() if response else []

    def start_telegram_bot(self, telegram_bot_id: int, data: StartTelegramBot) -> bool:
        return (
            self._request('post', f'bots/{telegram_bot_id}/start/', data=data)
            is not None
        )

    def restart_telegram_bot(self, telegram_bot_id: int) -> bool:
        return self._request('post', f'bots/{telegram_bot_id}/restart/') is not None

    def stop_telegram_bot(self, telegram_bot_id: int) -> bool:
        return self._request('post', f'bots/{telegram_bot_id}/stop/') is not None
