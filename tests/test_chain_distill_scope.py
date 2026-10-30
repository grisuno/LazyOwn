"""Chain distillation scope contract: config-driven target exclusion.

The operator denylist (``sessions/scope_deny.txt``) and RFC 2606
reserved domains drive which hosts never become the distilled target;
label-precise matching keeps unrelated lookalikes as candidates.
"""

from __future__ import annotations

from pathlib import Path

from modules.chain_distill import _excluded_host, _infer_target


def test_reserved_documentation_domains_excluded():
    """Given RFC 2606 placeholders, When inferring, Then they never win."""
    assert _excluded_host("example.com", frozenset()) is True
    assert _excluded_host("api.example.net", frozenset()) is True
    assert _excluded_host("help.example.org.", frozenset()) is True


def test_lookalikes_still_candidates():
    """Given lookalike labels, When inferring, Then they stay candidates."""
    assert _excluded_host("evilexample.com", frozenset()) is False
    assert _excluded_host("notexample.com", frozenset()) is False


def test_operator_denylist_excludes_label_tree(tmp_path: Path):
    """Given the operator denylist, When a denied host leads frequency, Then it is skipped."""
    (tmp_path / "scope_deny.txt").write_text("# operator scope\n10.0.0.9\ninternal.corp\n", encoding="utf-8")
    from modules import lazy_scope

    deny = lazy_scope.read_denylist(tmp_path)
    assert _excluded_host("10.0.0.9", deny) is True
    assert _excluded_host("vpn.internal.corp", deny) is True
    assert _excluded_host("10.0.0.10", deny) is False
    assert _excluded_host("external.corp.evil.com", deny) is False


def test_infer_target_respects_operator_deny(tmp_path: Path):
    """Given a denied host dominating command frequency, When inferring, Then the next host wins."""
    (tmp_path / "scope_deny.txt").write_text("10.0.0.9\n", encoding="utf-8")
    from modules import lazy_scope

    deny = lazy_scope.read_denylist(tmp_path)
    rows = [
        {"command": "probe 10.0.0.9"},
        {"command": "probe 10.0.0.9"},
        {"command": "probe 10.0.0.9"},
        {"command": "probe 10.0.0.8"},
    ]
    assert _infer_target(rows, {"goal": ""}, operator_deny=deny) == "10.0.0.8"


def test_infer_target_defers_denylist_load(tmp_path, monkeypatch):
    """Given no pre-loaded entries, When inferring, Then the denylist is loaded from sessions."""
    import modules.chain_distill as distill

    (tmp_path / "scope_deny.txt").write_text("10.0.0.9\n", encoding="utf-8")
    monkeypatch.setattr(distill, "SESSIONS_DIR", tmp_path, raising=False)
    rows = [{"command": "attack 10.0.0.9"}, {"command": "hit 10.0.0.11"}]
    assert distill._infer_target(rows, {"goal": ""}, operator_deny=None) == "10.0.0.11"
