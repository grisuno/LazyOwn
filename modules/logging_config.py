"""Centralized logging configuration for the LazyOwn framework.

Provides a single point of logging configuration to replace the 61+
scattered `logging.basicConfig()` calls across the codebase.

Usage:
    from modules.logging_config import configure, get_logger

    configure(level=logging.INFO, log_dir="sessions/logs", console=True, file=True)
    logger = get_logger(__name__)
    logger.info("Framework started")
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional


LOG_FORMAT_CONSOLE = '%(asctime)s [%(levelname)-7s] %(name)-20s %(message)s'
LOG_FORMAT_FILE = '%(asctime)s [%(levelname)-7s] %(name)-20s %(filename)s:%(lineno)d %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

_CONSOLE_COLORS: dict[int, str] = {
    logging.DEBUG: "\033[36m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[35m",
}
_CONSOLE_RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """ANSI-colored console formatter matching core.console.py style."""

    def format(self, record: logging.LogRecord) -> str:
        color = _CONSOLE_COLORS.get(record.levelno, "")
        prefix_map = {
            logging.DEBUG: "[.]",
            logging.INFO: "[+]",
            logging.WARNING: "[~]",
            logging.ERROR: "[-]",
            logging.CRITICAL: "[!]",
        }
        prefix = prefix_map.get(record.levelno, "[ ]")
        msg = super().format(record)
        return f"    {color}{prefix} {msg}{_CONSOLE_RESET}"


_logger_cache: dict = {}
_initialized: bool = False
_root_level: int = logging.INFO
_log_dir: Optional[str] = None


def configure(
    level: int = logging.INFO,
    log_dir: Optional[str] = None,
    console: bool = True,
    file: bool = True,
    format_console: str = LOG_FORMAT_CONSOLE,
    format_file: str = LOG_FORMAT_FILE,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    module_levels: Optional[dict] = None,
) -> None:
    """Configure LazyOwn's centralized logging system.

    Args:
        level: Default log level for all loggers.
        log_dir: Directory for log files. Defaults to sessions/.
        console: Enable console logging.
        file: Enable file logging.
        format_console: Format string for console output.
        format_file: Format string for file output.
        max_bytes: Maximum log file size before rotation.
        backup_count: Number of rotated log files to keep.
        module_levels: Dict mapping module names to specific log levels.
    """
    global _initialized, _root_level, _log_dir

    if _initialized:
        return

    _root_level = level
    _log_dir = log_dir or os.path.join(os.getcwd(), 'sessions', 'logs')
    os.makedirs(_log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        fmt = format_console or LOG_FORMAT_CONSOLE
        console_handler.setFormatter(ColoredFormatter(fmt, LOG_DATE_FORMAT))
        root_logger.addHandler(console_handler)

    if file:
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(_log_dir, f'lazyown_{date_str}.log')
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_file, LOG_DATE_FORMAT))
        root_logger.addHandler(file_handler)

        logging.getLogger('lazyown.init').info(f'Log file: {log_file}')

    if module_levels:
        for module_name, module_level in module_levels.items():
            logging.getLogger(module_name).setLevel(module_level)

    _initialized = True


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Get a logger with the given name.

    Ensures all loggers use the centralized configuration without
    needing individual basicConfig calls.

    Args:
        name: Logger name (e.g., module path).
        level: Optional override log level.

    Returns:
        Configured logger instance.
    """
    if name in _logger_cache:
        return _logger_cache[name]

    logger = logging.getLogger(name)

    if level is not None:
        logger.setLevel(level)
    elif not _initialized:
        logger.setLevel(_root_level)

    logger.propagate = True
    _logger_cache[name] = logger

    return logger


def set_level(name: str, level: int) -> None:
    """Set the log level for a specific logger.

    Args:
        name: Logger name.
        level: Log level constant.
    """
    logging.getLogger(name).setLevel(level)


def set_quiet() -> None:
    """Silence all logging below WARNING level."""
    for handler in logging.getLogger().handlers:
        handler.setLevel(logging.WARNING)


def set_verbose() -> None:
    """Enable DEBUG level logging."""
    for handler in logging.getLogger().handlers:
        handler.setLevel(logging.DEBUG)


def silence_module(name: str) -> None:
    """Completely silence a noisy module.

    Args:
        name: Module name pattern (e.g., 'urllib3').
    """
    logging.getLogger(name).setLevel(logging.CRITICAL + 1)


def reset() -> None:
    """Reset the logging system to defaults."""
    global _initialized, _logger_cache
    _logger_cache.clear()
    _initialized = False
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
