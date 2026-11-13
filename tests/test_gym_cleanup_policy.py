"""Gym cleanup policy: opt-in only, autonomous processes never stop gyms."""

from __future__ import annotations

import pytest


@pytest.fixture()
def no_payload(monkeypatch):
    import core.config as core_config

    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {})
    monkeypatch.delenv("LAZYOWN_AUTONOMOUS", raising=False)


def test_cleanup_disabled_by_default(no_payload):
    from modules.gym_cleanup import cleanup_enabled

    assert cleanup_enabled() is False


def test_cleanup_enabled_by_payload_opt_in(no_payload, monkeypatch):
    import core.config as core_config
    from modules.gym_cleanup import cleanup_enabled

    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {"gym_cleanup_on_exit": True})
    assert cleanup_enabled() is True

    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {"gym_cleanup_on_exit": "yes"})
    assert cleanup_enabled() is True

    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {"gym_cleanup_on_exit": False})
    assert cleanup_enabled() is False


def test_autonomous_process_never_cleans(no_payload, monkeypatch):
    import core.config as core_config
    from modules.gym_cleanup import cleanup_enabled

    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {"gym_cleanup_on_exit": True})
    monkeypatch.setenv("LAZYOWN_AUTONOMOUS", "1")
    assert cleanup_enabled() is False


def test_cleanup_skips_lab_runtime_when_disabled(no_payload, monkeypatch):
    from modules import gym_cleanup, lab_runtime

    def _boom(*a, **k):
        raise AssertionError("stop_all must not run when cleanup is disabled")

    monkeypatch.setattr(lab_runtime, "stop_all", _boom)
    monkeypatch.setattr(lab_runtime, "stop_ranges", _boom)
    outcome = gym_cleanup.cleanup_gym_machines(verbose=True)
    assert outcome["enabled"] is False


def test_cleanup_stops_machines_when_opted_in(no_payload, monkeypatch, capsys):
    import core.config as core_config
    from modules import gym_cleanup, lab_runtime

    monkeypatch.setattr(
        core_config, "load_payload", lambda *a, **k: {"gym_cleanup_on_exit": True}
    )
    monkeypatch.setattr(
        lab_runtime, "stop_all", lambda *a, **k: {"stopped": ["lazyown-lab-metasploitable"]}
    )
    monkeypatch.setattr(lab_runtime, "stop_ranges", lambda *a, **k: {"stopped": []})
    outcome = gym_cleanup.cleanup_gym_machines(verbose=True)
    assert outcome["enabled"] is True
    assert outcome["labs"]["stopped"] == ["lazyown-lab-metasploitable"]
    out = capsys.readouterr().out
    assert "gym cleanup: stopped 1 machine(s)" in out
