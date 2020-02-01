"""http helpers"""
import socket
from typing import Any, Dict, Optional

from django.http import HttpRequest


def _get_client_ip_from_meta(meta: Dict[str, Any]) -> Optional[str]:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    headers = (
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_REAL_IP",
        "REMOTE_ADDR",
    )
    for _header in headers:
        if _header in meta:
            return meta.get(_header)
    return None


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    if not request:
        return None
    return _get_client_ip_from_meta(request.META)


def get_reverse_dns(ip_address: str) -> str:
    """Does a reverse DNS lookup and returns the first IP"""
    try:
        rev = socket.gethostbyaddr(ip_address)
        if rev:
            return rev[0]
        return ""  # noqa
    except (socket.herror, socket.gaierror, TypeError, IndexError):
        return ""
