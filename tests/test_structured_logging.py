"""Tests for ``core.logging`` — structured JSON-lines logger."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


class TestStructuredLogConfig:
    """Behaviour of StructuredLogConfig."""

    def test_defaults_are_production_ready(self):
        import logging

        from core.logging import StructuredLogConfig

        cfg = StructuredLogConfig()
        assert cfg.level == logging.INFO
        assert cfg.json_output is True
        assert cfg.console_enabled is True
        assert cfg.file_enabled is True
        assert "password" in cfg.redacted_fields
        assert "token" in cfg.redacted_fields

    def test_custom_override_preserves_other_defaults(self):
        import logging

        from core.logging import StructuredLogConfig

        cfg = StructuredLogConfig(
            level=logging.DEBUG,
            json_output=False,
            log_dir="/tmp/logs",
            max_bytes=1024,
        )
        assert cfg.level == logging.DEBUG
        assert cfg.json_output is False
        assert cfg.log_dir == "/tmp/logs"
        assert cfg.max_bytes == 1024
        assert cfg.file_enabled is True


class TestJsonLineFormatter:
    """Behaviour of _JsonLineFormatter."""

    def test_formats_record_as_valid_json_line(self):
        import logging

        from core.logging import _JsonLineFormatter

        fmt = _JsonLineFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname=__file__,
            lineno=1, msg="hello world", args=(), exc_info=None,
        )
        record.component = "test-component"
        record.rhost = "10.0.0.1"
        line = fmt.format(record)
        data = json.loads(line)
        assert data["message"] == "hello world"
        assert data["level"] == "INFO"
        assert data["component"] == "test-component"
        assert data["rhost"] == "10.0.0.1"

    def test_redacts_sensitive_extra_fields(self):
        import logging

        from core.logging import _JsonLineFormatter

        fmt = _JsonLineFormatter(redacted_fields={"password", "token"})
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname=__file__,
            lineno=1, msg="auth", args=(), exc_info=None,
        )
        setattr(record, "_extra_password", "s3cr3t")
        setattr(record, "_extra_token", "abc123")
        setattr(record, "_extra_public", "visible")
        line = fmt.format(record)
        data = json.loads(line)
        assert data.get("password") == "[REDACTED]"
        assert data.get("token") == "[REDACTED]"
        assert data.get("public") == "visible"

    def test_includes_exception_traceback_when_present(self):
        import logging

        from core.logging import _JsonLineFormatter

        fmt = _JsonLineFormatter()
        try:
            raise ValueError("boom")
        except ValueError:
            record = logging.LogRecord(
                name="test", level=logging.ERROR, pathname=__file__,
                lineno=1, msg="failure", args=(),
                exc_info=sys.exc_info(),
            )
        line = fmt.format(record)
        data = json.loads(line)
        assert "exception" in data
        assert any("ValueError" in e for e in data["exception"])


class TestStructuredLogger:
    """Behaviour of StructuredLogger."""

    def test_make_records_promote_extra_fields_onto_record(self):
        from core.logging import StructuredLogger

        logger = StructuredLogger("test", level=0)
        record = logger.makeRecord(
            "test", 20, __file__, 1, "msg", (), None,
            extra={"phase": "recon", "rhost": "10.0.0.5", "duration_ms": 150},
        )
        assert getattr(record, "phase", None) == "recon"
        assert getattr(record, "rhost", None) == "10.0.0.5"
        assert getattr(record, "duration_ms", None) == 150


class TestGetLogger:
    """Behaviour of get_logger and install_json_handler."""

    def test_first_call_creates_and_configures_logger(self):
        import logging

        from core.logging import get_logger

        log_a = get_logger("unit_test_a")
        assert isinstance(log_a, logging.Logger)
        assert log_a.level == logging.INFO

    def test_same_name_returns_cached_instance(self):
        from core.logging import _LOGGER_CACHE, get_logger

        _LOGGER_CACHE.clear()
        log_a = get_logger("unit_test_cc")
        assert "unit_test_cc" in _LOGGER_CACHE
        log_b = get_logger("unit_test_cc")
        assert log_a is log_b
        assert len(_LOGGER_CACHE) == 1

    def test_writes_json_lines_to_file(self, tmp_path):
        from core.logging import (
            StructuredLogConfig,
            get_logger,
            install_json_handler,
        )

        cfg = StructuredLogConfig(
            log_dir=str(tmp_path),
            log_filename="test.log",
            json_output=True,
            console_enabled=False,
        )
        install_json_handler("file_test", cfg)
        log = get_logger("file_test")
        log.info("entry_one", extra={"rhost": "10.0.0.1"})
        log.warning("entry_two", extra={"rhost": "10.0.0.2"})

        log_path = tmp_path / "test.log"
        assert log_path.exists()
        lines = log_path.read_text().strip().split("\n")
        assert len(lines) == 2
        entry = json.loads(lines[0])
        assert entry["message"] == "entry_one"
        assert entry["rhost"] == "10.0.0.1"


class TestReconfigure:
    """Behaviour of reconfigure."""

    def test_reconfigure_resets_cache_and_applies_new_config(self, tmp_path):
        import logging

        from core.logging import (
            StructuredLogConfig,
            get_logger,
            reconfigure,
        )

        log_a = get_logger("reconfig_test")
        first_level = log_a.level

        new_cfg = StructuredLogConfig(
            level=logging.DEBUG,
            log_dir=str(tmp_path),
            console_enabled=False,
        )
        reconfigure(new_cfg)

        log_b = get_logger("reconfig_test")
        assert log_b.level == logging.DEBUG
        assert log_b.level != first_level


class TestInstallJsonHandler:
    """Contract: install_json_handler preserves pre-existing handlers."""

    def test_cold_logger_gets_console_and_file_wiring(self, tmp_path):
        import logging

        from core.logging import (
            StructuredLogConfig,
            get_logger,
            install_json_handler,
        )

        cfg = StructuredLogConfig(log_dir=str(tmp_path), log_filename="cold.log")
        install_json_handler("cold_wire", cfg)
        log = get_logger("cold_wire")
        kinds = {type(h) for h in log.handlers}
        assert logging.StreamHandler in kinds
        from logging.handlers import RotatingFileHandler
        assert RotatingFileHandler in kinds

    def test_warm_logger_keeps_custom_handler_and_appends_json_file(self, tmp_path):
        import logging
        from logging.handlers import RotatingFileHandler

        from core.logging import (
            StructuredLogConfig,
            install_json_handler,
        )

        logger = logging.getLogger("warm_wire")
        custom = logging.StreamHandler()
        logger.handlers = [custom]

        cfg = StructuredLogConfig(log_dir=str(tmp_path), log_filename="warm.log")
        install_json_handler("warm_wire", cfg)

        assert custom in logger.handlers
        assert any(
            isinstance(h, RotatingFileHandler) for h in logger.handlers
        )

    def test_second_install_is_idempotent(self, tmp_path):
        from logging.handlers import RotatingFileHandler

        from core.logging import (
            StructuredLogConfig,
            install_json_handler,
        )

        cfg = StructuredLogConfig(log_dir=str(tmp_path), log_filename="once.log")
        install_json_handler("idem_wire", cfg)
        from core.logging import get_logger
        log = get_logger("idem_wire")
        before = sum(
            1 for h in log.handlers
            if isinstance(h, RotatingFileHandler)
        )
        install_json_handler("idem_wire", cfg)
        after = sum(
            1 for h in log.handlers
            if isinstance(h, RotatingFileHandler)
        )
        assert before == after == 1
