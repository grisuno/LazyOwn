"""Tests for the auto_loop C2 autostart wiring in modules.lazy_runner.

Covers:
    - Endpoint resolution (bind address, wildcards, port fallback)
    - Spawn skipped when the C2 endpoint is already listening
    - Spawn + wait path with a scripted liveness probe
    - Timeout path warning without raising
    - Pytest guard keeps the helper inert during tests
"""

from __future__ import annotations

import subprocess

import pytest


@pytest.fixture
def runner():
    from modules import lazy_runner

    return lazy_runner


def _allow_pytest_call(monkeypatch) -> None:
    """Drop the pytest marker so the call-time guard sees a plain process.

    pytest re-sets ``PYTEST_CURRENT_TEST`` when entering the call phase,
    after fixtures run, so the deletion must happen inside the test body.

    Args:
        monkeypatch: Active pytest monkeypatch handle.
    """
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)


class TestEndpoint:
    def test_bind_address_wins(self, runner):
        host, port = runner._c2_endpoint({"c2_bind_address": "10.9.9.9", "lhost": "10.0.0.1", "c2_port": 8443})
        assert (host, port) == ("10.9.9.9", 8443)

    def test_wildcard_maps_to_loopback(self, runner):
        host, _ = runner._c2_endpoint({"c2_bind_address": "0.0.0.0", "lhost": "10.0.0.1"})
        assert host == "127.0.0.1"

    def test_port_fallback(self, runner):
        host, port = runner._c2_endpoint({"lhost": "10.0.0.1"})
        assert host == "10.0.0.1"
        assert port == runner.C2_PORT_FALLBACK

    def test_bad_port_falls_back(self, runner):
        _, port = runner._c2_endpoint({"lhost": "10.0.0.1", "c2_port": "abc"})
        assert port == runner.C2_PORT_FALLBACK


class TestMaybeStartC2:
    def test_flag_off_is_noop(self, runner, monkeypatch):
        calls = []

        _allow_pytest_call(monkeypatch)
        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: calls.append((host, port)) or True)
        assert runner._maybe_start_c2({}) is False
        assert calls == []

    def test_already_listening_skips_spawn(self, runner, monkeypatch):
        spawned = []

        _allow_pytest_call(monkeypatch)
        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: True)
        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawned.append(a))
        assert runner._maybe_start_c2({"loop_c2_autostart": True, "lhost": "10.0.0.1"}) is True
        assert spawned == []

    def test_spawn_and_wait_success(self, runner, monkeypatch):
        spawned = []
        probes = {"n": 0}

        _allow_pytest_call(monkeypatch)

        def fake_alive(host, port):
            probes["n"] += 1
            return probes["n"] > 1

        monkeypatch.setattr(runner, "_c2_port_alive", fake_alive)
        monkeypatch.setattr(runner.time, "sleep", lambda *_: None)
        monkeypatch.setattr(
            subprocess,
            "Popen",
            lambda argv, **kw: spawned.append(argv) or type("P", (), {"pid": 1})(),
        )
        params = {"loop_c2_autostart": True, "c2_port": 4444, "c2_user": "operator_dgrmylup", "c2_pass": "secret"}
        assert runner._maybe_start_c2(params) is True
        assert len(spawned) == 1
        assert spawned[0][1] == "-u"
        assert spawned[0][2] == "lazyc2.py"
        assert spawned[0][3] == "4444"
        assert spawned[0][4] == "operator_dgrmylup"
        assert spawned[0][5] == "secret"
        assert "python" in spawned[0][0]

    def test_spawn_never_listening_warns(self, runner, monkeypatch):
        spawned = []
        warnings = []

        _allow_pytest_call(monkeypatch)
        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: False)
        monotonic_calls: list[float] = []
        real_monotonic = runner.time.monotonic

        def _fast_deadline() -> float:
            monotonic_calls.append(real_monotonic())
            return monotonic_calls[-1] if len(monotonic_calls) == 1 else monotonic_calls[0] + 3600.0

        monkeypatch.setattr(runner.time, "monotonic", _fast_deadline)
        monkeypatch.setattr(runner.time, "sleep", lambda *_: None)
        monkeypatch.setattr(runner, "print_warn", lambda text: warnings.append(text))
        monkeypatch.setattr(runner, "print_msg", lambda *_: None)

        def _fake_popen(argv, **kwargs):
            if isinstance(argv, (list, tuple)) and any("lazyc2.py" in str(part) for part in argv):
                spawned.append(argv)
            return type("P", (), {"pid": 1})()

        monkeypatch.setattr(subprocess, "Popen", _fake_popen)
        params = {"loop_c2_autostart": True, "lhost": "10.0.0.1", "c2_autostart_timeout": 1}
        assert runner._maybe_start_c2(params) is False
        assert len(spawned) == 1
        assert any("not listening" in text for text in warnings)

    def test_pytest_guard_blocks_spawn(self, runner, monkeypatch):
        spawned = []

        monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: spawned.append(a))
        assert runner._maybe_start_c2({"loop_c2_autostart": True, "lhost": "10.0.0.1"}) is False
        assert spawned == []

    def test_never_raises_on_spawn_failure(self, runner, monkeypatch):
        _allow_pytest_call(monkeypatch)

        def raising(*args, **kwargs):
            raise OSError("boom")

        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: False)
        monkeypatch.setattr(subprocess, "Popen", raising)
        assert runner._maybe_start_c2({"loop_c2_autostart": True, "lhost": "10.0.0.1"}) is False

    def test_tip_when_handoff_off(self, runner, monkeypatch):
        messages = []

        _allow_pytest_call(monkeypatch)
        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: True)
        monkeypatch.setattr(runner, "print_msg", lambda text: messages.append(text))
        params = {"loop_c2_autostart": True, "lhost": "10.0.0.1"}
        assert runner._maybe_start_c2(params) is True
        assert any("loop_beacon_handoff" in text for text in messages)

    def test_no_tip_when_handoff_on(self, runner, monkeypatch):
        messages = []

        _allow_pytest_call(monkeypatch)
        monkeypatch.setattr(runner, "_c2_port_alive", lambda host, port: True)
        monkeypatch.setattr(runner, "print_msg", lambda text: messages.append(text))
        params = {"loop_c2_autostart": True, "lhost": "10.0.0.1", "loop_beacon_handoff": True}
        assert runner._maybe_start_c2(params) is True
        assert any("already listening" in text for text in messages)
        assert not any("loop_beacon_handoff" in text for text in messages)
