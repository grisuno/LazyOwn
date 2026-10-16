"""C2 dashboard surfaces fed by the autonomous loop and APT chains."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.c2_surfaces import (  # noqa: E402
    append_note,
    group_tasks_for_display,
    publish_banner,
    publish_cve,
    register_loot_event,
    severity_to_risk,
)


def _sandbox(tmp_path: Path) -> Path:
    """Isolated sessions dir for every test in this module."""
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    return sessions


def test_publish_banner_dedupes(tmp_path: Path) -> None:
    """Same host/port/service stored once, even across repeated sweeps."""
    sessions = _sandbox(tmp_path)
    assert publish_banner("10.0.0.1", 21, "tcp", "ftp", "vsftpd 2.3.4", sessions) is True
    assert publish_banner("10.0.0.1", "21", "tcp", "FTP", "vsftpd 2.3.4", sessions) is True
    data = json.loads((sessions / "banners.json").read_text(encoding="utf-8"))
    assert len(data["banners"]) == 1
    assert publish_banner("10.0.0.1", 445, "tcp", "microsoft-ds", "Samba", sessions) is True
    data = json.loads((sessions / "banners.json").read_text(encoding="utf-8"))
    assert len(data["banners"]) == 2


def test_publish_cve_validates_and_dedupes(tmp_path: Path) -> None:
    """CVE risk levels mirror the /cves form; titles never duplicate."""
    sessions = _sandbox(tmp_path)
    assert publish_cve("", sessions_dir=sessions) is False
    assert publish_cve("CVE-2011-2523 on 10.0.0.1", "vsftpd backdoor", "autonomous_loop", "critical", sessions) is True
    assert publish_cve("cve-2011-2523 ON 10.0.0.1", sessions_dir=sessions) is True
    data = json.loads((sessions / "cves.json").read_text(encoding="utf-8"))
    assert len(data) == 1 and data[0]["risk"] == "CRITICAL" and data[0]["id"] == 0
    assert publish_cve("CVE-2007-2447 on 10.0.0.1", "samba", "autonomous_loop", "bogus", sessions) is True
    data = json.loads((sessions / "cves.json").read_text(encoding="utf-8"))
    assert [c["id"] for c in data] == [0, 1] and data[1]["risk"] == "MEDIUM"
    assert severity_to_risk("critical") == "CRITICAL" and severity_to_risk("nope") == "MEDIUM"


def test_append_note_never_clobbers(tmp_path: Path) -> None:
    """Operator notes survive loop appends; empty lines are ignored."""
    sessions = _sandbox(tmp_path)
    (sessions / "notes.txt").write_text(json.dumps({"content": "operator plan"}), encoding="utf-8")
    assert append_note("", sessions) is False
    assert append_note("SHELL 10.0.0.1 via vsftpd_backdoor", sessions) is True
    content = json.loads((sessions / "notes.txt").read_text(encoding="utf-8"))["content"]
    assert "operator plan" in content and "SHELL 10.0.0.1" in content


def test_register_loot_event_dedupes_and_rejects_traversal(tmp_path: Path) -> None:
    """Loot event rules dedupe by name and reject path tricks."""
    cfg = tmp_path / "event_config.json"
    assert register_loot_event("loot_msf", "sessions/loot/*", event_config=cfg) is True
    assert register_loot_event("loot_msf", "sessions/loot/*", event_config=cfg) is True
    assert register_loot_event("../../x", "/etc/passwd", event_config=cfg) is False
    assert register_loot_event("", "", event_config=cfg) is False
    data = json.loads(cfg.read_text(encoding="utf-8"))
    assert len(data["events"]) == 1 and data["events"][0]["operator"] == "autonomous_loop"


def test_group_tasks_unique_hits(tmp_path: Path) -> None:
    """Identical titles collapse with counts; junk is tallied as noise."""
    tasks = [
        {"id": 0, "status": "Done", "title": "Recon 10.0.0.1", "operator": "x"},
        {"id": 1, "status": "New", "title": "Leverage new credential: {\"value\": \"a:b\"}"},
        {"id": 2, "status": "New", "title": "Leverage new credential: {\"value\": \"12:09:08\"}"},
        {"id": 3, "status": "New", "title": "Enumerate newly discovered host 10.0.0.1"},
        {"id": 4, "status": "New", "title": "Enumerate newly discovered host 10.0.0.1"},
    ]
    groups, noise = group_tasks_for_display(tasks)
    titles = [g["task"]["title"] for g in groups]
    assert titles.count("Recon 10.0.0.1") == 1
    assert titles.count("Enumerate newly discovered host 10.0.0.1") == 1
    assert noise == 2
    assert group_tasks_for_display([]) == ([], 0)
    assert group_tasks_for_display(None) == ([], 0)


def test_record_outcome_feeds_c2_surfaces(tmp_path: Path, monkeypatch) -> None:
    """Exploit outcomes land in cves.json + notes.txt via record_outcome."""
    import modules.atomic_exploit_bridge as _bridge
    from modules.atomic_exploit_bridge import ExploitCommand as _Cmd
    from modules.atomic_exploit_bridge import ExploitSpec

    sessions = _sandbox(tmp_path)

    class _StubWM:
        def update_from_findings(self, findings):
            return None

    monkeypatch.setattr("modules.world_model.get_world_model", lambda *a, **k: _StubWM())
    monkeypatch.setattr("modules.killchain.KillChain", lambda *a, **k: type("K", (), {"advance_phase": lambda s, p: False})())
    monkeypatch.setattr("modules.intel_fusion.build_intel_graph", lambda *a, **k: {})
    monkeypatch.setattr("modules.lazy_intel.record_routing_outcome", lambda *a, **k: {})
    spec = ExploitSpec(
        id="demo", mitre_id="T1190", cve="CVE-2011-2523", title="Demo RCE",
        severity="critical", confidence=0.9,
        commands=[_Cmd(run="id", timeout=5)],
    )
    fed = _bridge.record_outcome(spec, "10.0.0.1", True, output="uid=0", surfaces_dir=sessions)
    assert fed.get("cves") is True and fed.get("notes") is True
    cves = json.loads((sessions / "cves.json").read_text(encoding="utf-8"))
    assert any("CVE-2011-2523" in c["title"] for c in cves)


def test_lazyreport_errors_are_actionable(monkeypatch) -> None:
    """Ollama failures must explain themselves, never return blank errors."""
    import requests as _requests
    from flask import Flask as _Flask

    import modules.legacy.lazydeepseekcli as _legacy

    _app = _Flask(__name__)
    _app.app_context().push()

    def _refused(*a, **k):
        raise _requests.ConnectionError("refused")

    monkeypatch.setattr(_legacy.requests, "post", _refused)
    resp, code = _legacy._ollama_stream("hello", "console")
    assert code == 503
    body = resp.get_data(as_text=True) if hasattr(resp, "get_data") else resp.data.decode()
    assert "Ollama unreachable" in body and "deepseek" in body

    def _slow(*a, **k):
        raise _requests.Timeout("slow")

    monkeypatch.setattr(_legacy.requests, "post", _slow)
    resp, code = _legacy._ollama_stream("hello", "console")
    assert code == 504
    body = resp.get_data(as_text=True) if hasattr(resp, "get_data") else resp.data.decode()
    assert "timed out" in body
