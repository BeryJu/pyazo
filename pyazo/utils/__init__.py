"""pyazo utils"""
import socket

from django.http import HttpRequest


def get_remote_ip(request: HttpRequest) -> str:
    """Return the remote's IP"""
    if not request:
        return "0.0.0.0"
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR")
    return request.META.get("REMOTE_ADDR")


def get_reverse_dns(ipaddress: str) -> str:
    """Does a reverse DNS lookup and returns the first IP"""
    try:
        rev = socket.gethostbyaddr(ipaddress)
        if rev:
            return rev[0]
        return ""  # noqa
    except (socket.herror, socket.gaierror, TypeError, IndexError):
        return ""
