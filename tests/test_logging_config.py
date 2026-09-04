"""Tests for ``modules.logging_config`` — resilient file logging."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _make_logger(handler):
    logger = logging.getLogger(f"test_resilient_{id(handler)}")
    logger.handlers = [handler]
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger


class TestResilientRotatingFileHandler:
    def test_writes_normally_when_dir_writable(self, tmp_path):
        from modules.logging_config import ResilientRotatingFileHandler

        logfile = tmp_path / "app.log"
        handler = ResilientRotatingFileHandler(str(logfile), delay=True)
        logger = _make_logger(handler)
        logger.info("hello world")
        assert "hello world" in logfile.read_text(encoding="utf-8")
        assert not getattr(handler, "_detached", False)

    def test_detaches_silently_when_file_unwritable(self, tmp_path, capsys):
        from modules.logging_config import ResilientRotatingFileHandler

        missing = tmp_path / "missing" / "app.log"
        handler = ResilientRotatingFileHandler(str(missing), delay=True)
        logger = _make_logger(handler)

        for _ in range(3):
            logger.info("should not spam a traceback")

        captured = capsys.readouterr()
        assert getattr(handler, "_detached", False) is True
        assert "Traceback" not in captured.err
        assert "file logging disabled" in captured.err

    def test_rotating_file_is_exposed(self):
        import logging.handlers

        from modules.logging_config import ResilientRotatingFileHandler

        assert issubclass(ResilientRotatingFileHandler, logging.handlers.RotatingFileHandler)
