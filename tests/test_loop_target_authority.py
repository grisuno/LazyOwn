"""Target authority: --target rebinds payload rhost and scope.

Given auto_loop/lazy_loop is launched with an explicit target,
When the run starts,
Then the payload rhost becomes that target and the authorized scope is
replaced with exactly the run's targets, so offensive verbs and the
scope guard can only act against what the operator named. A stale rhost
or stale in-scope host can no longer divert the loop to another IP.
"""

from __future__ import annotations

from modules.lazy_runner import bind_target_authority


class _FakeShell:
    """Minimal shell exposing params and the canonical scope writer."""

    def __init__(self, params):
        self.params = params
        self.saved = []

    def _scope_save(self, entries=None, mode=None):
        if entries is not None:
            self.params["scope"] = entries
        if mode is not None:
            self.params["scope_enforcement"] = mode
        self.saved.append(dict(self.params))


def test_single_target_replaces_rhost_and_scope():
    shell = _FakeShell({"rhost": "10.0.0.1", "scope": ["172.17.0.2", "127.0.0.1"]})
    summary = bind_target_authority(shell, ["127.0.0.1"])
    assert summary["bound"] is True
    assert shell.params["rhost"] == "127.0.0.1"
    assert shell.params["scope"] == ["127.0.0.1"]
    assert summary["previous_rhost"] == "10.0.0.1"
    assert summary["previous_scope"] == ["172.17.0.2", "127.0.0.1"]
    assert shell.saved, "scope writer must persist"


def test_multi_target_scope_is_every_target():
    shell = _FakeShell({"rhost": "10.0.0.1", "scope": ["old"]})
    bind_target_authority(shell, ["10.10.10.5", "10.10.10.7"])
    assert shell.params["rhost"] == "10.10.10.5"
    assert shell.params["scope"] == ["10.10.10.5", "10.10.10.7"]


def test_dedupes_and_strips():
    shell = _FakeShell({"rhost": "", "scope": []})
    bind_target_authority(shell, [" 127.0.0.1 ", "127.0.0.1", "", "10.0.0.2"])
    assert shell.params["scope"] == ["127.0.0.1", "10.0.0.2"]


def test_noop_when_already_bound():
    shell = _FakeShell({"rhost": "127.0.0.1", "scope": ["127.0.0.1"]})
    summary = bind_target_authority(shell, ["127.0.0.1"])
    assert summary["bound"] is False
    assert shell.saved == []


def test_enforcement_mode_untouched():
    shell = _FakeShell({"rhost": "10.0.0.1", "scope": ["old"], "scope_enforcement": "enforce"})
    bind_target_authority(shell, ["127.0.0.1"])
    assert shell.params["scope_enforcement"] == "enforce"


def test_empty_targets_is_noop():
    shell = _FakeShell({"rhost": "10.0.0.1", "scope": ["old"]})
    assert bind_target_authority(shell, [])["bound"] is False
    assert shell.params["rhost"] == "10.0.0.1"
    assert shell.params["scope"] == ["old"]


def test_fallback_writer_without_scope_save(monkeypatch):
    saved = {}

    def _fake_save(params, *a, **k):
        saved.update(params)

    monkeypatch.setattr("core.config.save_payload", _fake_save)

    class _Bare:
        def __init__(self):
            self.params = {"rhost": "10.0.0.1", "scope": ["old"]}

    shell = _Bare()
    bind_target_authority(shell, ["127.0.0.1"])
    assert shell.params["rhost"] == "127.0.0.1"
    assert shell.params["scope"] == ["127.0.0.1"]
    assert saved.get("scope") == ["127.0.0.1"]
