"""Non-blocking stdio hardening: logging must never crash the shell."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import core.console as console  # noqa: E402
from core.console import (  # noqa: E402
    ensure_blocking_stdio,
    print_error,
    write_stdout,
)


class _FailOnce:
    """Stdout double failing the first write with BlockingIOError."""

    def __init__(self) -> None:
        self.calls = 0
        self.text = ""

    def write(self, data: str) -> int:
        """Raise once, then accept."""
        self.calls += 1
        if self.calls == 1:
            raise BlockingIOError(11, "write could not complete without blocking")
        self.text += data
        return len(data)

    def flush(self) -> None:
        """No-op flush."""

    def fileno(self) -> int:
        """Invalid fd so fd-level repair is skipped."""
        raise ValueError("no fileno")


class _AlwaysFail:
    """Stdout/stderr double that always fails."""

    def write(self, data: str) -> int:
        """Always raise."""
        raise BlockingIOError(11, "write could not complete without blocking")

    def flush(self) -> None:
        """No-op flush."""

    def fileno(self) -> int:
        """Invalid fd so fd-level repair is skipped."""
        raise ValueError("no fileno")


def test_write_stdout_normal_path(capsys) -> None:
    """Healthy stdout writes through and reports success."""
    assert write_stdout("hello\n") is True
    assert capsys.readouterr().out == "hello\n"


def test_write_stdout_recovers_after_blocking_error(monkeypatch) -> None:
    """One BlockingIOError is absorbed; the retry delivers the text."""
    fake = _FailOnce()
    monkeypatch.setattr(sys, "stdout", fake)
    assert write_stdout("retry me\n") is True
    assert "retry me" in fake.text


def test_write_stdout_never_raises(monkeypatch) -> None:
    """Total stdio failure degrades silently instead of killing the op."""
    monkeypatch.setattr(sys, "stdout", _AlwaysFail())
    monkeypatch.setattr(sys, "stderr", _AlwaysFail())
    assert write_stdout("dropped\n") is False


def test_print_error_survives_broken_stdout(monkeypatch, capsys) -> None:
    """The error path from the reported crash no longer double-faults."""
    monkeypatch.setattr(sys, "stdout", _AlwaysFail())
    print_error("Error executing command for scan.nmap.xml: boom")
    captured = capsys.readouterr()
    assert "boom" in captured.err or captured.out == ""


def test_ensure_blocking_stdio_never_raises() -> None:
    """Fd repair is best-effort on any stdio shape."""
    ensure_blocking_stdio()
    assert console is not None
