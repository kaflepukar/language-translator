import datetime
import logging
from contextvars import ContextVar
from typing import Any, Dict, Union

from pythonjsonlogger.json import JsonFormatter

from settings import settings

request_id_ctx_var: ContextVar[Union[str, None]] = ContextVar(
    "request_id_ctx_var", default=None
)

__logger: logging.Logger | None = None


class CustomJsonFormatter(JsonFormatter):
    """Custom JSON formatter for logging with additional fields."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        log_record["timestamp"] = datetime.datetime.fromtimestamp(
            record.created, tz=datetime.timezone.utc
        ).isoformat()
        log_record["pathname"] = record.pathname
        log_record["line"] = record.lineno
        log_record["severity"] = record.levelname
        log_record["request_id"] = request_id_ctx_var.get()
        super().add_fields(log_record, record, message_dict)


def get_logger() -> logging.Logger:
    """Logger factory function to create a logger with JSON formatting."""

    global __logger
    if __logger:
        return __logger

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler: logging.FileHandler | logging.StreamHandler = logging.StreamHandler()
    if settings.ENV != "local":
        handler = logging.FileHandler("translator_service.log")
    handler.setFormatter(CustomJsonFormatter())
    logger.addHandler(handler)
    __logger = logger
    return logger
