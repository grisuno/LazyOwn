"""Structured JSON-lines logging for the LazyOwn framework.

Replaces the historical ``print_msg`` / ``print_warn`` / ``print_error``
pattern with a unified JSON-lines logger that preserves ANSI-coloured
console output AND writes machine-parseable entries to disk.

Contracts
---------
* ``StructuredLogConfig``: every tunable — log level, output path, JSON
  vs plaintext, field redaction — lives here; no magic strings elsewhere.
* ``StructuredLogger``: drop-in replacement for ``core.console`` helpers.
  Accepts ``extra`` kwargs that become top-level JSON fields.
* ``get_logger(name)``: factory with lazy initialisation matching Python's
  ``logging.getLogger`` semantics.
* ``install_json_handler``: one-time wiring that adds a rotating JSON-lines
  file handler without disturbing existing console handlers.

Usage::

    from core.logging import StructuredLogConfig, get_logger

    _log = get_logger("lazyc2.api")

    # Human-readable console + JSON-lines audit entry
    _log.info("Beacon checked in", extra={"client_id": "abc", "rhost": "10.0.0.5"})
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


@dataclass
class StructuredLogConfig:
    """Configuration contract for structured logging.

    All log-related settings are centralized here. The framework reads
    these from ``payload.json`` keys prefixed with ``log_``.
    """

    level: int = logging.INFO
    json_output: bool = True
    log_dir: str = "sessions"
    log_filename: str = "lazyown.log"
    max_bytes: int = 10 * 1024 * 1024
    backup_count: int = 5
    console_enabled: bool = True
    file_enabled: bool = True
    redacted_fields: frozenset[str] = frozenset({
        "password", "pass", "secret", "token", "api_key", "aes_key",
    })
    default_component: str = "lazyown"
    trace_id_provider: Any = None


class _JsonLineFormatter(logging.Formatter):
    """Format a log record as a single JSON line."""

    def __init__(self, redacted_fields: frozenset[str] | None = None):
        super().__init__()
        self._redact = redacted_fields or frozenset()

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for attr in (
            "component", "phase", "tenant_id", "rhost", "lhost",
            "command", "client_id", "trace_id", "user", "duration_ms",
        ):
            val = getattr(record, attr, None)
            if val is not None:
                entry[attr] = val

        for key, value in record.__dict__.items():
            if key.startswith("_extra_"):
                clean_key = key[len("_extra_"):]
                if clean_key in self._redact:
                    entry[clean_key] = "[REDACTED]"
                elif isinstance(value, (str, int, float, bool, type(None), list, dict)):
                    entry[clean_key] = value

        if record.exc_info and record.exc_info[0]:
            import traceback
            entry["exception"] = traceback.format_exception(
                record.exc_info[0],
                record.exc_info[1],
                record.exc_info[2],
            )

        return json.dumps(entry, default=str, ensure_ascii=False)


class _ConsoleFormatter(logging.Formatter):
    """ANSI-coloured console formatter matching ``core.console`` style."""

    PREFIXES = {
        logging.DEBUG: "\033[36m[?]\033[0m",     # cyan
        logging.INFO: "\033[32m[+]\033[0m",      # green
        logging.WARNING: "\033[35m[~]\033[0m",   # magenta
        logging.ERROR: "\033[31m[-]\033[0m",     # red
        logging.CRITICAL: "\033[91m[!]\033[0m",  # bright red
    }

    def format(self, record: logging.LogRecord) -> str:
        prefix = self.PREFIXES.get(record.levelno, "[ ]")
        component = getattr(record, "component", "") or ""
        tag = f"[{component}] " if component else ""
        return f"    {prefix} {tag}{record.getMessage()}"


class StructuredLogger(logging.Logger):
    """Logger subclass that accepts ``extra`` kwargs as structured fields.

    Every keyword in ``extra`` is stored on the record and appears as a
    top-level key in the JSON-lines output. Sensitive fields matching
    ``StructuredLogConfig.redacted_fields`` are replaced with ``[REDACTED]``
    before serialization.
    """

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: Any,
        exc_info: Any,
        func: str | None = None,
        extra: dict[str, Any] | None = None,
        sinfo: bool = False,
    ) -> logging.LogRecord:
        record = super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo,
        )
        if extra:
            for key, value in extra.items():
                setattr(record, f"_extra_{key}", value)
                setattr(record, key, value)
        return record


def _log_factory(
    name: str,
    config: StructuredLogConfig | None = None,
) -> StructuredLogger:
    """Create or retrieve a :class:`StructuredLogger` instance.

    Args:
        name: The logger name (typically ``__name__``).
        config: Optional configuration. When ``None``, defaults are used.

    Returns:
        A :class:`StructuredLogger` wired up with console + file handlers.
    """
    if config is None:
        config = StructuredLogConfig()

    logging.setLoggerClass(StructuredLogger)
    logger = logging.getLogger(name)
    logger.setLevel(config.level)
    logger.propagate = False
    logger.handlers.clear()

    if config.console_enabled:
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(config.level)
        console.setFormatter(_ConsoleFormatter())
        logger.addHandler(console)

    if config.file_enabled:
        Path(config.log_dir).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(config.log_dir, config.log_filename)
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=config.max_bytes,
            backupCount=config.backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(config.level)
        if config.json_output:
            file_handler.setFormatter(_JsonLineFormatter(config.redacted_fields))
        else:
            file_handler.setFormatter(_ConsoleFormatter())
        logger.addHandler(file_handler)

    return logger


_LOGGER_CACHE: dict[str, StructuredLogger] = {}
_CACHED_CONFIG: StructuredLogConfig | None = None


def get_logger(name: str = "lazyown") -> StructuredLogger:
    """Return a cached :class:`StructuredLogger` for *name*.

    On first call the default configuration is applied. Subsequent calls
    with the same *name* return the same logger instance.

    Args:
        name: The logger name. Defaults to ``"lazyown"``.

    Returns:
        A configured :class:`StructuredLogger`.
    """
    global _CACHED_CONFIG
    if name not in _LOGGER_CACHE:
        if _CACHED_CONFIG is None:
            _CACHED_CONFIG = StructuredLogConfig()
        _LOGGER_CACHE[name] = _log_factory(name, _CACHED_CONFIG)
    return _LOGGER_CACHE[name]


def install_json_handler(
    name: str = "lazyown",
    config: StructuredLogConfig | None = None,
) -> None:
    """Install a JSON-lines file handler on *name*, preserving existing handlers.

    When the logger already owns handlers (a custom console sink, a
    library-configured appender) they are left untouched and only the
    JSON file handler is appended. When the logger is cold it receives
    the standard console plus file wiring from :func:`_log_factory`.
    The operation is idempotent: a second call with the same name and
    configuration adds nothing.

    Args:
        name: The logger name to wire.
        config: Optional configuration override, cached for future
            :func:`get_logger` calls.
    """
    global _CACHED_CONFIG, _LOGGER_CACHE
    if config is not None:
        _CACHED_CONFIG = config
    cfg = _CACHED_CONFIG or StructuredLogConfig()
    if not cfg.file_enabled or not cfg.json_output:
        return
    logging.setLoggerClass(StructuredLogger)
    logger = logging.getLogger(name)
    if not logger.handlers:
        _LOGGER_CACHE[name] = _log_factory(name, cfg)
        return
    if any(
        isinstance(handler, RotatingFileHandler)
        and isinstance(handler.formatter, _JsonLineFormatter)
        for handler in logger.handlers
    ):
        return
    Path(cfg.log_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(cfg.log_dir, cfg.log_filename)
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=cfg.max_bytes,
        backupCount=cfg.backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(cfg.level)
    file_handler.setFormatter(_JsonLineFormatter(cfg.redacted_fields))
    logger.addHandler(file_handler)
    logger.setLevel(cfg.level)
    _LOGGER_CACHE[name] = logger


def reconfigure(config: StructuredLogConfig) -> None:
    """Replace the cached configuration globally.

    All future ``get_logger()`` calls will use *config*. Existing
    loggers in the cache are refreshed.

    Args:
        config: The new configuration to apply.
    """
    global _CACHED_CONFIG, _LOGGER_CACHE
    _CACHED_CONFIG = config
    stale = list(_LOGGER_CACHE.keys())
    _LOGGER_CACHE.clear()
    for name in stale:
        get_logger(name)
