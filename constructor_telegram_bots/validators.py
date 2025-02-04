from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.deconstruct import deconstructible

from collections.abc import Callable
from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    ip_address,
    ip_network,
)
from urllib.parse import urlparse


@deconstructible
class PublicURLValidator:
    validate_url: Callable[[str | None], None] = URLValidator()
    private_networks: list[IPv4Network | IPv6Network] = [
        ip_network('127.0.0.0/8'),
        ip_network('10.0.0.0/8'),
        ip_network('172.16.0.0/12'),
        ip_network('192.168.0.0/16'),
        ip_network('169.254.0.0/16'),
        ip_network('::1/128'),
        ip_network('fc00::/7'),
        ip_network('fe80::/10'),
    ]

    def __call__(self, url: str | None) -> None:
        self.validate_url(url)
        assert url

        hostname: str | None = urlparse(url).hostname
        assert hostname

        try:
            ip: IPv4Address | IPv6Address = ip_address(hostname)
        except ValueError:
            return

        for network in self.private_networks:
            if ip in network:
                raise ValidationError(
                    URLValidator.message, code=URLValidator.code, params={'value': url}
                )
