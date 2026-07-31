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
_log_dir_fallback_used: bool = False


def _ensure_log_dir_writable(log_dir: str) -> str:
    """Return a writable log directory, fixing ownership when possible.

    When ``fast_run_as_r00t.sh`` runs before the regular user, the
    ``sessions/logs/`` directory can end up owned by root, blocking the
    owning user from creating log files. This helper attempts to:

    1. Create the directory with the current user's ownership.
    2. If it already exists but is owned by root, try to force ownership
       back via ``sudo chown`` (non-interactive, only works with NOPASSWD).
    3. If that fails, fall back to ``/tmp/lazyown_<uid>_logs/`` and emit a
       one-time warning so the operator knows to clean up.

    Returns the final (possibly fallback) log directory path.
    """
    global _log_dir_fallback_used
    uid = os.getuid()

    if uid == 0:
        os.makedirs(log_dir, mode=0o755, exist_ok=True)
        return log_dir

    parent = os.path.dirname(os.path.abspath(log_dir))
    try:
        os.makedirs(parent, mode=0o755, exist_ok=True)
    except OSError:
        pass

    try:
        os.makedirs(log_dir, mode=0o755, exist_ok=True)
    except PermissionError:
        pass

    try:
        st = os.stat(log_dir)
    except OSError:
        st = None

    if st is not None and st.st_uid != uid:
        try:
            os.chown(log_dir, uid, -1)
        except OSError:
            pass

    writable = False
    try:
        probe = os.path.join(log_dir, ".writetest")
        with open(probe, "w") as fh:
            fh.write("x")
        os.unlink(probe)
        writable = True
    except (OSError, PermissionError):
        pass

    if writable:
        if st is not None and st.st_uid != uid:
            for entry in os.listdir(log_dir):
                entry_path = os.path.join(log_dir, entry)
                if os.path.isfile(entry_path):
                    try:
                        entry_st = os.stat(entry_path)
                        if entry_st.st_uid != uid:
                            os.chown(entry_path, uid, -1)
                            os.chmod(entry_path, 0o644)
                    except OSError:
                        pass
        return log_dir

    fallback = os.path.join("/tmp", f"lazyown_{uid}_logs")
    os.makedirs(fallback, mode=0o755, exist_ok=True)
    if not _log_dir_fallback_used:
        _log_dir_fallback_used = True
        print(
            f"\n    [!] sessions/logs/ is owned by root — writing logs to {fallback}",
            flush=True,
        )
    return fallback


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
    _log_dir = _ensure_log_dir_writable(_log_dir)

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
        try:
            os.makedirs(os.path.dirname(log_file), mode=0o755, exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, delay=True,
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(format_file, LOG_DATE_FORMAT))
            root_logger.addHandler(file_handler)
            logging.getLogger('lazyown.init').info(f'Log file: {log_file}')
        except (OSError, PermissionError) as exc:
            print(
                f"\n    [!] Cannot write log file: {exc}",
                f"\n    [!] File logging disabled — output to console only.",
                flush=True,
            )

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
