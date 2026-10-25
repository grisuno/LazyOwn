"""Finding confirmation lifecycle + keyless OSINT enrichment."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import modules.osint_enrich as osint  # noqa: E402
from modules.finding_lifecycle import (  # noqa: E402
    add_dead_end,
    apply_confirmation,
    confirm,
    is_dead_end,
    reject,
    resolve,
    suppressed_values,
)
from modules.osint_enrich import enrich_evidence  # noqa: E402


def _finding(fid: str, sources: tuple = ("world_model.json",)) -> dict:
    """Minimal finding node as produced by the graph builders."""
    return {"id": fid, "kind": "finding", "value": f"vuln-{fid}",
            "sources": list(sources)}


def test_pending_by_default(tmp_path: Path) -> None:
    """Single-source findings stay pending intel, not noise."""
    assert resolve(_finding("a", ("world_model.json",)), tmp_path) == "pending"


def test_multi_source_auto_confirms(tmp_path: Path) -> None:
    """Two independent sources confirm without operator action."""
    node = _finding("b", ("world_model.json", "session logs"))
    assert resolve(node, tmp_path) == "confirmed"


def test_explicit_confirm_with_evidence(tmp_path: Path) -> None:
    """Operator confirmation persists evidence on the finding."""
    record = confirm("c", ["world_model vulnerabilities"], tmp_path, by="operator")
    assert record["status"] == "confirmed"
    assert record["evidence"] == ["world_model vulnerabilities"]
    assert resolve(_finding("c"), tmp_path) == "confirmed"


def test_reject_beats_auto_confirm(tmp_path: Path) -> None:
    """Explicit reject wins over the multi-source rule (CAIRN dead-ends)."""
    node = _finding("d", ("world_model.json", "session logs", "scan.nmap"))
    assert resolve(node, tmp_path) == "confirmed"
    reject("d", "false positive on honeypot", tmp_path)
    assert resolve(node, tmp_path) == "rejected"


def test_dead_end_suppresses_value(tmp_path: Path) -> None:
    """Labeled suppression list rejects matching values campaign-wide."""
    add_dead_end("host", "10.9.9.9", "lab printer, out of scope", tmp_path)
    assert is_dead_end("host", "10.9.9.9", tmp_path) is True
    assert is_dead_end("host", "10.0.0.1", tmp_path) is False
    assert "10.9.9.9" in suppressed_values(tmp_path)


def test_apply_confirmation_stamps_nodes(tmp_path: Path) -> None:
    """Builder hook stamps confirmation + display status on findings."""
    confirm("e", ["op"], tmp_path)
    nodes = {"e": _finding("e"), "h": {"id": "h", "kind": "host", "value": "1.1.1.1"}}
    apply_confirmation(nodes, tmp_path)
    assert nodes["e"]["confirmation"] == "confirmed"
    assert nodes["e"]["status"] == "confirmed"
    assert "confirmation" not in nodes["h"]


def test_enrich_evidence_appends_keyless_verdicts(tmp_path: Path, monkeypatch) -> None:
    """CVE mentions gain OSV/KEV/EPSS verdicts without any API key."""
    monkeypatch.setattr(osint, "cve_lookup", lambda cve, sessions="": {
        "cve": cve, "summary": "RCE in widget", "severity": "CVSS:3.1 9.8",
        "kev": True, "epss": 0.94})
    out = enrich_evidence(["open ssh CVE-2024-1234"], tmp_path)
    assert len(out) == 2
    assert "osint:" in out[1] and "CISA-KEV" in out[1] and "EPSS" in out[1]


def test_enrich_evidence_never_fails_offline(tmp_path: Path, monkeypatch) -> None:
    """Broken network degrades to the raw items, never an exception."""
    def _boom(cve, sessions=""):
        raise OSError("offline")

    monkeypatch.setattr(osint, "cve_lookup", _boom)
    assert enrich_evidence(["plain note, no cve"], tmp_path) == ["plain note, no cve"]
    assert enrich_evidence(["note CVE-2024-0001"], tmp_path) == ["note CVE-2024-0001"]
