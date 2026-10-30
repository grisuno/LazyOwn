"""Host heat score contract: deterministic, capped, auditable priorities.

Every scenario states Given, When, Then. One pure function returns the
score with its reason list; persistence never raises and the planner
boost reads the persisted table.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.lazy_hostscore import (
    FINDINGS_CAP,
    SCORE_FILENAME,
    load_scores,
    score_host,
)


def test_hot_cve_and_findings_and_shell_stay_capped():
    """Given heavy inputs, When scoring, Then the score saturates at 100."""
    inputs = {
        "cves": [{"heat": "hot", "kev": True}],
        "findings": [
            {"severity": "critical", "status": "confirmed"},
            {"severity": "high", "status": "confirmed"},
            {"severity": "medium", "status": "confirmed"},
        ],
        "shell": True,
        "admin_paths": ["/admin"],
        "recency": 1.0,
    }
    score, detail = score_host(inputs)
    assert score == 100
    assert {row["label"] for row in detail} >= {"shell foothold", "admin surface open"}


def test_findings_cap_bounds_the_subtotal():
    """Given an absurd finding pile, When scoring, Then the subtotal respects the cap."""
    inputs = {
        "cves": [],
        "findings": [
            {"severity": "critical", "status": "confirmed"},
            {"severity": "high", "status": "confirmed"},
            {"severity": "medium", "status": "confirmed"},
            {"severity": "low", "status": "confirmed"},
        ],
        "shell": False,
        "admin_paths": [],
        "recency": 0.0,
    }
    _score, detail = score_host(inputs)
    subtotal = sum(row["points"] for row in detail if "severity" in row["label"])
    assert subtotal == FINDINGS_CAP


def test_discarded_findings_and_cold_no_points():
    """Given discards and no CVEs, When scoring, Then they cost nothing."""
    inputs = {
        "cves": [{"heat": "warm"}, {"heat": "cold"}],
        "findings": [
            {"severity": "critical", "status": "discarded"},
            {"severity": "high", "status": "discarded"},
        ],
        "shell": False,
        "admin_paths": [],
        "recency": 30 * 86400.0,
    }
    score, detail = score_host(inputs)
    labels = {row["label"] for row in detail}
    assert "cve heat warm" in labels
    assert all("severity" not in label for label in labels)
    assert "changed this week" not in labels
    assert 0 < score <= 100


def test_empty_inputs_score_zero():
    """Given nothing, When scoring, Then zero with empty detail."""
    assert score_host({}) == (0, [])


def test_persistence_roundtrip(tmp_path: Path):
    """Given a writer and a reader, When reloaded, Then scores survive."""
    table = {"10.0.0.9": {"score": 42, "detail": [{"label": "x", "points": 42}]}}
    path = tmp_path / "lazy" / SCORE_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"ts": 0.0, "hosts": table}), encoding="utf-8")
    assert load_scores(tmp_path) == {"10.0.0.9": 42.0}
    assert load_scores(tmp_path / "nowhere") == {}


def test_rescore_offline_survives_errors(tmp_path: Path, monkeypatch):
    """Given an offline rescore, When the feed fails, Then the table still writes."""
    import modules.lazy_hostscore as hostscore

    class _StubWorld:
        """World model stub with one host."""

        def snapshot(self):
            """Return one host with a service but no CVE network."""
            return {
                "phase": "recon",
                "hosts": {
                    "10.0.0.9": {
                        "state": "OWNED",
                        "services": {"22": {"name": "ssh", "version": "OpenSSH 8.4", "state": "open"}},
                        "notes": ["admin panel open at /admin"],
                    }
                },
                "vulnerabilities": [
                    {"host": "10.0.0.9", "severity": "high", "status": "confirmed", "summary": "open ssh"}
                ],
            }

    def broken_correlate(*_args, **_kwargs):
        """Raise to simulate a dead feed."""
        raise RuntimeError("offline")

    monkeypatch.setattr("modules.world_model.get_world_model", lambda: _StubWorld(), raising=False)
    monkeypatch.setattr("modules.lazy_cve_feed.correlate", broken_correlate, raising=False)
    monkeypatch.setattr("modules.lazy_world_diff.recent_changes", lambda *a, **k: [], raising=False)
    table = hostscore.rescore(tmp_path, allow_network=False)
    assert table["10.0.0.9"]["score"] > 0
    assert load_scores(tmp_path)["10.0.0.9"] > 0
