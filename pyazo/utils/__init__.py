"""http helpers"""
import socket
from typing import Any, Dict, Optional

from django.http import HttpRequest


def _get_client_ip_from_meta(meta: Dict[str, Any]) -> str:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    headers = (
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_REAL_IP",
        "REMOTE_ADDR",
    )
    address = None
    for _header in headers:
        if _header in meta:
            address = meta.get(_header)
    if address:
        if "," in address:
            return address.split(",")[0]
        return address
    return ""


def get_client_ip(request: HttpRequest) -> str:
    """Attempt to get the client's IP by checking common HTTP Headers.
    Returns none if no IP Could be found"""
    if not request:
        raise ValueError("Missing request")
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
