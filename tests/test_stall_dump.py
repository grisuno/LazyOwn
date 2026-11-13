"""Tests for the stall watchdog dump showing the last executed commands."""

from __future__ import annotations

import pytest


@pytest.fixture()
def traffic_task(temp_sessions):
    task_id = "stalltask"
    from modules.lazy_loop import TrafficLog

    log = TrafficLog(task_id)
    log.record("bash", "lazynmap 10.10.11.5", "scan output")
    log.record("bash", "linpeas 10.10.11.5", "post-exp output")
    return task_id


def test_last_task_commands_returns_recent_commands(traffic_task, temp_sessions):
    from modules.lazy_runner import _last_task_commands

    lines = _last_task_commands(traffic_task)
    assert any("lazynmap 10.10.11.5" in line for line in lines)
    assert any("linpeas" in line for line in lines)


def test_last_task_commands_empty_without_task():
    from modules.lazy_runner import _last_task_commands

    assert _last_task_commands("") == []


def test_dump_thread_stacks_prints_last_commands(traffic_task, temp_sessions):
    from modules.lazy_runner import _dump_thread_stacks

    chunks: list[str] = []

    class _Capture:
        def write(self, text):
            chunks.append(str(text))

        def flush(self):
            pass

    _dump_thread_stacks(traffic_task, target=_Capture())
    output = "".join(chunks)
    assert "no loop activity" in output
    assert any("lazynmap 10.10.11.5" in line for line in output.splitlines() if line.startswith("[stall] last command"))


@pytest.fixture()
def temp_sessions(tmp_path, monkeypatch):
    """Redirect the loop store into an isolated directory."""
    import modules.lazy_loop as lazy_loop

    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    monkeypatch.setattr(lazy_loop, "SESSIONS_DIR", sessions_dir)
    if hasattr(lazy_loop, "_STORE_PATH"):
        monkeypatch.setattr(lazy_loop, "_STORE_PATH", lambda name: sessions_dir / name)
    return sessions_dir
