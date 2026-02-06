from __future__ import annotations

"""
Lightweight logging helper for Project Chimera.

- Uses Python's standard `logging` module.
- Configurable via a YAML-derived config mapping. Expected keys (optional):
    logging:
      level: INFO
      file: logs/tenx_chimera.log
      max_bytes: 10_485_760
      backup_count: 5
- Emits to console and to a rotating file handler.
- Injects a request / correlation id into each record via `set_request_id`.
- Reusable across agents (call `get_logger(__name__, config)` in modules).

No business logic is implemented here. Designed for Python 3.11.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
from contextvars import ContextVar
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Optional
import uuid

__all__ = [
    "get_logger",
    "set_request_id",
    "clear_request_id",
    "get_request_id",
    "ConfigurableRequestIdFilter",
    "ConfigError",
]

# Context var for request/correlation id (per async/task/thread context)
_request_id_var: ContextVar[Optional[str]] = ContextVar("_request_id", default=None)


class ConfigError(RuntimeError):
    """Raised for configuration/initialization problems in logging setup."""


class ConfigurableRequestIdFilter(logging.Filter):
    """
    Logging filter that injects `request_id` into LogRecord.

    - If a request id is set via `set_request_id(...)`, that value is used.
    - Otherwise `-` is used as placeholder.
    """

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - trivial
        rid = _request_id_var.get()
        record.request_id = rid if (rid is not None and str(rid)) else "-"
        return True


def set_request_id(request_id: Optional[str] = None) -> str:
    """
    Set the current request/correlation id in context.

    If `request_id` is None, a new UUID4 string will be generated and returned.
    """
    if request_id is None:
        request_id = uuid.uuid4().hex
    _request_id_var.set(request_id)
    return request_id


def clear_request_id() -> None:
    """Clear the current request id from context."""
    _request_id_var.set(None)


def get_request_id() -> Optional[str]:
    """Return the current request id or None."""
    return _request_id_var.get()


def _resolve_level(level: Any, default: int = logging.INFO) -> int:
    """
    Resolve various representations of a log level into a logging module level int.

    Accepts numeric levels or strings like "INFO", "debug", etc.
    """
    if isinstance(level, int):
        return level
    if isinstance(level, str):
        name = level.strip().upper()
        resolved = logging.getLevelName(name)
        if isinstance(resolved, int):
            return resolved
    return default


def _ensure_log_dir(path: Path) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as exc:  # pragma: no cover - filesystem problems
        raise ConfigError(f"Unable to create log directory {path.parent!s}: {exc}") from exc


def _make_formatter() -> logging.Formatter:
    # ISO-like timestamp with timezone offset
    fmt = "%(asctime)s %(levelname)s [%(request_id)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S%z"
    return logging.Formatter(fmt=fmt, datefmt=datefmt)


# Keep track of configured loggers to avoid adding handlers multiple times.
_configured_loggers: set[str] = set()


def get_logger(name: str, config: Mapping[str, Any] | None = None, *, default_level: str = "INFO") -> logging.Logger:
    """
    Return a configured `logging.Logger` instance for `name`.

    Parameters
    - name: logger name (usually __name__ of caller module)
    - config: optional mapping produced by YAML loader. Expected top-level key "logging".
      Example:
        logging:
          level: INFO
          file: logs/app.log
          max_bytes: 10485760
          backup_count: 5
    - default_level: fallback log level name or numeric.

    The returned logger will have console and rotating file handlers (if file provided).
    """
    logger = logging.getLogger(name)

    # Avoid reconfiguring the same logger multiple times
    if name in _configured_loggers:
        return logger

    # Determine logging configuration
    log_cfg: MutableMapping[str, Any] = {}
    if config is not None and isinstance(config, Mapping):
        raw = config.get("logging", {})
        if isinstance(raw, Mapping):
            log_cfg.update(raw)

    # Level resolution
    level = _resolve_level(log_cfg.get("level", default_level), default=logging.INFO)
    logger.setLevel(level)
    logger.propagate = False  # let this logger handle propagation explicitly

    # Add request id filter to logger
    req_filter = ConfigurableRequestIdFilter()
    logger.addFilter(req_filter)

    formatter = _make_formatter()

    # Console handler (StreamHandler to stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (RotatingFileHandler) if configured
    log_file = log_cfg.get("file")
    if log_file:
        file_path = Path(log_file)
        _ensure_log_dir(file_path)
        max_bytes = int(log_cfg.get("max_bytes", 10_485_760))  # default 10 MB
        backup_count = int(log_cfg.get("backup_count", 5))
        try:
            fh = logging.handlers.RotatingFileHandler(
                filename=str(file_path),
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        except Exception as exc:  # pragma: no cover - OS/file errors
            raise ConfigError(f"Unable to configure file logging at {file_path!s}: {exc}") from exc

    # Mark as configured to prevent double handlers
    _configured_loggers.add(name)

    return logger
