"""Signalman scoreboard tests: catalogue resolution, sweep and render."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import modules.ctf_capture as ctf_capture
import modules.ctf_signalman as signalman


def _entry(vuln_id: str) -> dict:
    return {"id": vuln_id, "name": vuln_id, "cve": "CVE-2026-0001", "mitre": "T1", "service": "http", "port": "80", "severity": "high"}


@pytest.fixture()
def fake_catalogue(monkeypatch):
    entries = [_entry(v) for v in ("v_a", "v_b", "v_c")]
    lookup = {"v_a": entries[0], "v_b": entries[1], "v_c": entries[2]}
    monkeypatch.setattr(signalman, "catalogue_for", lambda scenario: (entries, lookup.get))
    return entries, lookup


@pytest.fixture()
def sessions(tmp_path, monkeypatch) -> Path:
    (tmp_path / "evidence.txt").write_text("uid=0(root) groups=0(root)\nroot:$6$abc$def:0:0:99999:7:::\n")
    monkeypatch.setattr(ctf_capture, "output_dir", lambda sessions_dir=None: tmp_path / "sessions" / "ctf")
    return tmp_path / "sessions" / "ctf"


def test_catalogue_for_known_scenarios() -> None:
    for scenario in ("metasploitable", "ad_lab", "winbox"):
        entries, lookup = signalman.catalogue_for(scenario)
        assert entries and callable(lookup)
    with pytest.raises(ValueError):
        signalman.catalogue_for("nope")


def test_collect_captures_matches_sweep(sessions, fake_catalogue, monkeypatch) -> None:
    evidence = str(sessions.parent.parent / "evidence.txt")
    report = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[evidence])
    assert sorted(report["captured"]) == ["v_a", "v_b", "v_c"]
    assert report["score"] == 100.0
    assert report["total"] == 3
    stored = json.loads((sessions / "v_a" / "record.json").read_text())
    assert stored["status"] == "captured"


def test_capture_binds_checker_to_vector_objective() -> None:
    """Given a root-shell blob, When an enum vector verifies, Then it is not credited."""
    enum_entry = {"id": "ad_ldap_enum", "name": "ad ldap enum", "service": "ldap", "mitre": "T1087"}
    rce_entry = {"id": "vsftpd_backdoor", "name": "vsftpd backdoor rce", "service": "ftp", "mitre": "T1210"}
    shell_blob = "uid=0(root) groups=0(root)"
    enum = ctf_capture.capture("ad_ldap_enum", "1.2.3.4", output=shell_blob, catalogue=lambda _v: enum_entry)
    assert enum["status"] == "failed"
    assert enum["expected_checkers"] == ["domain_enum"]
    rce = ctf_capture.capture("vsftpd_backdoor", "1.2.3.4", output=shell_blob, catalogue=lambda _v: rce_entry)
    assert rce["status"] == "captured"
    assert rce["matched_checkers"] == ["root_shell"]


def test_capture_honours_declared_checkers() -> None:
    """Given an explicit checkers list, When verifying, Then only those bind."""
    entry = {"id": "v", "name": "x", "service": "ftp", "mitre": "T1", "checkers": ["domain_enum"]}
    record = ctf_capture.capture("v", "1.2.3.4", output="uid=0(root)", catalogue=lambda _v: entry)
    assert record["status"] == "failed"
    assert record["expected_checkers"] == ["domain_enum"]


def test_collect_idempotent_and_missing(sessions, fake_catalogue, monkeypatch) -> None:
    evidence = str(sessions.parent.parent / "empty")
    Path(evidence).mkdir()
    first = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[evidence])
    assert first["captured"] == []
    assert first["score"] == 0.0
    again = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[evidence])
    assert again["captured"] == []
    (sessions.parent.parent / "evidence.txt").write_text("uid=0(root) groups=0(root)\n")
    final = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[str(sessions.parent.parent / "evidence.txt")])
    assert sorted(final["captured"]) == ["v_a", "v_b", "v_c"]


def test_collect_uses_payload_rhost_when_target_empty(sessions, fake_catalogue, monkeypatch) -> None:
    monkeypatch.setattr("core.config.load_payload", lambda: {"rhost": "9.9.9.9"}, raising=False)
    report = signalman.collect("metasploitable", sessions_dir=sessions, search_bases=[str(sessions)])
    assert report["target"] == "9.9.9.9"


def test_render_scoreboard(sessions, fake_catalogue) -> None:
    evidence = str(sessions.parent.parent / "evidence.txt")
    report = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[evidence])
    text = signalman.render_scoreboard(report)
    assert "3/3 captured" in text
    assert "[x] v_a" in text
    assert "score 100.0%" in text


def test_save_scoreboard(sessions, fake_catalogue) -> None:
    report = signalman.collect("metasploitable", target="1.2.3.4", sessions_dir=sessions, search_bases=[str(sessions)])
    path = signalman.save_scoreboard(report, sessions_dir=sessions)
    assert path.name == "scoreboard.json"
    assert json.loads(path.read_text())["scenario"] == "metasploitable"
