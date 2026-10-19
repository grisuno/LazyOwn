"""Unit tests for the Metasploitable 2 gym migrations module."""

from __future__ import annotations

import pytest

import modules.metasploitable_migrations as migrations


def test_build_migrations_ordered_and_unique() -> None:
    steps = migrations.build_migrations("10.0.0.")
    assert len(steps) >= 8
    ids = [step.id for step in steps]
    assert len(ids) == len(set(ids))
    assert ids[0] == "core-services"
    assert ids[-1] == "dvwa-dom-page"


def test_hosts_allow_uses_subnet_prefix() -> None:
    steps = {s.id: s for s in migrations.build_migrations("192.168.7.")}
    apply_script = steps["rservices-access"].apply
    assert "192.168.7." in apply_script
    assert "{subnet}" not in apply_script
    assert "in.rlogind" in apply_script
    assert "pts/$i" in apply_script
    assert "0 1 2 3 4 5" in apply_script


def test_apply_migrations_skips_when_check_passes(monkeypatch) -> None:
    monkeypatch.setattr(migrations, "_docker_exec", lambda *a, **k: (0, ""))
    report = migrations.apply_migrations("fake-container")
    steps = migrations.build_migrations()
    no_check = [s.id for s in steps if not s.check]
    skipped = [mid for mid, row in report.items() if row["skipped"]]
    applied = [mid for mid, row in report.items() if row["applied"]]
    assert skipped == [s.id for s in steps if s.check]
    assert applied == no_check


def test_apply_migrations_applies_when_check_fails(monkeypatch) -> None:
    def _fake_exec(container, script, payload="", timeout=120):
        looks_like_check = script.startswith(("grep -q", "test -", "ps aux", "mysql -u root -N"))
        touches_state = any(token in script for token in (">>", "restart", "mkdir", "cat >"))
        if looks_like_check and not touches_state:
            return 1, "check failed"
        return 0, ""

    monkeypatch.setattr(migrations, "_docker_exec", _fake_exec)
    report = migrations.apply_migrations("fake-container")
    assert not any(row["skipped"] for row in report.values())
    assert all(row["applied"] for row in report.values())


def test_dvwa_dom_page_payload_contains_sink() -> None:
    steps = {s.id: s for s in migrations.build_migrations()}
    payload = steps["dvwa-dom-page"].payload
    assert "document.write" in payload
    assert "decodeURIComponent" in payload
    assert "<script>" in payload


def test_database_mirror_uses_dump_and_restore() -> None:
    steps = {s.id: s for s in migrations.build_migrations()}
    apply_script = steps["mutillidae-database"].apply
    assert "set-up-database.php" in apply_script
    assert "mysqldump" in apply_script
    assert migrations.MUTILLIDAE_DB in apply_script


__all__: list[str] = []
