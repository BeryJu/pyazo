"""pyazo sentry integration"""
from structlog import get_logger

LOGGER = get_logger()


def before_send(event, hint):
    """Check if error is database error, and ignore if so"""
    from billiard.exceptions import WorkerLostError
    from django.core.exceptions import DisallowedHost
    from django.db import InternalError, OperationalError
    from django_redis.exceptions import ConnectionInterrupted
    from rest_framework.exceptions import APIException

    ignored_classes = (
        OperationalError,
        ConnectionInterrupted,
        APIException,
        InternalError,
        ConnectionResetError,
        WorkerLostError,
        DisallowedHost,
        ConnectionResetError,
        KeyboardInterrupt,
        OSError,
    )
    if "exc_info" in hint:
        _exc_type, exc_value, _ = hint["exc_info"]
        if isinstance(exc_value, ignored_classes):
            LOGGER.info("Supressing error %r", exc_value)
            return None
    return event
