from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool

from requests import PreparedRequest
from requests.adapters import HTTPAdapter
from requests.compat import unquote, urlparse

from collections.abc import Mapping
from socket import AF_UNIX, SOCK_STREAM, socket


class UnixHTTPConnection(HTTPConnection):
	def __init__(self, socket_path: str) -> None:
		super().__init__('localhost')
		self.socket_path = socket_path

	def connect(self) -> None:
		self.sock = socket(AF_UNIX, SOCK_STREAM)
		self.sock.connect(self.socket_path)


class UnixHTTPConnectionPool(HTTPConnectionPool):
	def __init__(self, socket_path: str) -> None:
		super().__init__('localhost')
		self.socket_path = socket_path

	def _new_conn(self) -> UnixHTTPConnection:
		return UnixHTTPConnection(self.socket_path)


class UnixHTTPAdapter(HTTPAdapter):
	def get_connection_with_tls_context(
		self,
		request: PreparedRequest,
		verify: bool | str | None,
		proxies: Mapping[str, str] | None = None,
		cert: tuple[str, str] | str | None = None,
	) -> UnixHTTPConnectionPool:
		return UnixHTTPConnectionPool(unquote(urlparse(request.url).netloc))

	def request_url(self, request: PreparedRequest, proxies: Mapping[str, str]) -> str:
		return request.path_url
