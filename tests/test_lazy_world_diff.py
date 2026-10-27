"""World-surface diff contract: snapshots, changes, ghost liveness, stats.

Pure-function discipline: every evaluator takes plain dicts and an
injectable checker, so no test needs network access.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from modules.lazy_world_diff import (  # noqa: E402
    HOST_NEW,
    HOST_RETIRED,
    PORT_CLOSED,
    PORT_OPENED,
    SERVICE_CHANGED,
    OS_CHANGED,
    diff_snapshots,
    ghost_endpoints,
    ghost_state_apply,
    host_snapshot,
    load_ghosts,
    prune_changes,
    recent_changes,
    record_changes,
    snapshot_engagement,
    snapshot_fingerprint,
)


def _world(hosts: dict) -> dict:
    return {"phase": "recon", "hosts": hosts}


def _svc(name: str, product: str = "", version: str = "") -> dict:
    return {"name": name, "product": product, "version": version, "state": "open"}


# ---------------------------------------------------------------- snapshots


def test_host_snapshot_reads_open_services_only() -> None:
    """Closed services never enter the snapshot."""
    world = _world(
        {
            "10.0.0.5": {
                "ip": "10.0.0.5",
                "state": "scanned",
                "os_hint": "linux",
                "services": {
                    "22": _svc("ssh", "OpenSSH", "8.9p1"),
                    "9999": {"name": "dead", "state": "closed"},
                },
            }
        }
    )
    snap = host_snapshot(world, "10.0.0.5")
    assert snap["ip"] == "10.0.0.5"
    assert snap["os"] == "linux"
    assert snap["ports"] == {"22/tcp": {"service": "ssh", "product": "OpenSSH", "version": "8.9p1"}}


def test_host_snapshot_missing_host_is_empty() -> None:
    """A host absent from the world snapshots as empty, never raises."""
    assert host_snapshot(_world({}), "10.0.0.9") == {}


def test_snapshot_fingerprint_stable_and_sensitive() -> None:
    """Same snapshot yields the same hash; a new port changes it."""
    world = _world({"10.0.0.5": {"services": {"22": _svc("ssh")}}})
    snap = host_snapshot(world, "10.0.0.5")
    other = host_snapshot(_world({"10.0.0.5": {"services": {"22": _svc("ssh")}}}), "10.0.0.5")
    assert snapshot_fingerprint(snap) == snapshot_fingerprint(other)
    grown = host_snapshot(_world({"10.0.0.5": {"services": {"22": _svc("ssh"), "80": _svc("http")}}}), "10.0.0.5")
    assert snapshot_fingerprint(grown) != snapshot_fingerprint(snap)


def test_snapshot_fingerprint_ignores_key_order() -> None:
    """Canonical JSON keeps the fingerprint key-order independent."""
    world = _world(
        {
            "10.0.0.5": {
                "services": {"22": _svc("ssh"), "80": _svc("http")},
            }
        }
    )
    flipped = _world(
        {
            "10.0.0.5": {
                "services": {"80": _svc("http"), "22": _svc("ssh")},
            }
        }
    )
    assert snapshot_fingerprint(host_snapshot(world, "10.0.0.5")) == snapshot_fingerprint(
        host_snapshot(flipped, "10.0.0.5")
    )


# ---------------------------------------------------------------- diff


def test_diff_reports_port_lifecycle() -> None:
    """Opened and closed ports get distinct kinds with port numbers."""
    before = {"ports": {"22/tcp": {"service": "ssh", "product": "", "version": ""}}}
    after = {
        "ports": {
            "22/tcp": {"service": "ssh", "product": "", "version": ""},
            "443/tcp": {"service": "https", "product": "nginx", "version": "1.18"},
        }
    }
    changes = diff_snapshots(before, after)
    kinds = {c.kind for c in changes}
    assert kinds == {PORT_OPENED}
    opened = changes[0]
    assert opened.port == 443
    assert opened.after["service"] == "https"
    closed = diff_snapshots(after, before)
    assert closed[0].kind == PORT_CLOSED
    assert closed[0].port == 443


def test_diff_service_change_requires_prior_identity() -> None:
    """A product appearing where none was is enrichment, not a change."""
    base = {"ports": {"22/tcp": {"service": "ssh", "product": "", "version": ""}}}
    enriched = {"ports": {"22/tcp": {"service": "ssh", "product": "OpenSSH", "version": "8.9p1"}}}
    assert diff_snapshots(base, enriched) == []
    renamed = {"ports": {"22/tcp": {"service": "ssh", "product": "OpenSSH", "version": "9.3p1"}}}
    changes = diff_snapshots(enriched, renamed)
    assert [c.kind for c in changes] == [SERVICE_CHANGED]
    assert changes[0].before["version"] == "8.9p1"
    assert changes[0].after["version"] == "9.3p1"


def test_diff_os_change_and_empty_states() -> None:
    """An OS hint flip is its own kind; empty snapshots never diff."""
    before = {"os": "linux", "ports": {}}
    after = {"os": "windows", "ports": {}}
    changes = diff_snapshots(before, after)
    assert [c.kind for c in changes] == [OS_CHANGED]
    assert diff_snapshots({}, {}) == []


# ---------------------------------------------------------------- changes log


def test_record_and_recent_changes(tmp_path: Path) -> None:
    """Recorded changes come back newest-first and filter by host."""
    record_changes(
        [
            (HOST_NEW, "10.0.0.5", 0, None, {"state": "scanned"}),
        ],
        tmp_path,
        now=time.time(),
    )
    record_changes(
        [
            (PORT_OPENED, "10.0.0.5", 443, None, {"service": "https"}),
        ],
        tmp_path,
        now=time.time() + 1,
    )
    rows = recent_changes(tmp_path, days=7)
    assert len(rows) == 2
    assert rows[0]["kind"] == PORT_OPENED
    host_rows = recent_changes(tmp_path, days=7, host="10.0.0.5")
    assert len(host_rows) == 2
    assert recent_changes(tmp_path, days=7, host="10.0.0.99") == []


def test_record_changes_dedupes_repeat(tmp_path: Path) -> None:
    """An identical latest entry for the same host is not written twice."""
    change = (PORT_OPENED, "10.0.0.5", 443, None, {"service": "https"})
    record_changes([change], tmp_path, now=time.time())
    record_changes([change], tmp_path, now=time.time() + 5)
    assert len(recent_changes(tmp_path, days=1)) == 1


def test_record_changes_caps_each_host(tmp_path: Path) -> None:
    """A host cannot flood the log past the per-host cap."""
    for port in range(1, 80):
        record_changes(
            [(PORT_OPENED, "10.0.0.5", port, None, {})],
            tmp_path,
            now=time.time() + port,
        )
    rows = recent_changes(tmp_path, days=1, host="10.0.0.5")
    assert len(rows) <= 40


def test_prune_changes(tmp_path: Path) -> None:
    """Changes older than the window are dropped; recent stay."""
    old = time.time() - 91 * 24 * 3600
    record_changes([(PORT_OPENED, "10.0.0.5", 22, None, {})], tmp_path, now=old)
    record_changes([(PORT_OPENED, "10.0.0.6", 22, None, {})], tmp_path, now=time.time())
    removed = prune_changes(tmp_path, keep_days=90)
    assert removed == 1
    assert [row["ip"] for row in recent_changes(tmp_path, days=365)] == ["10.0.0.6"]


# ---------------------------------------------------------------- ghosts


def test_ghost_endpoints_prefers_web_ports() -> None:
    """Web ports surface first, 443 before 80, capped by limit."""
    snap = {
        "ip": "10.0.0.5",
        "ports": {
            "8080/tcp": {"service": "http-alt"},
            "22/tcp": {"service": "ssh"},
            "443/tcp": {"service": "https"},
            "80/tcp": {"service": "http"},
        }
    }
    endpoints = ghost_endpoints(snap, limit=3)
    assert [port for _ip, port, _scheme in endpoints] == [443, 80, 8080]
    assert all(port != 22 for _ip, port, _scheme in endpoints)


def test_ghost_state_apply_roundtrip(tmp_path: Path) -> None:
    """A ghost is stored once, refreshed on re-detection, cleared on resolve."""
    answers = ghost_state_apply("10.0.0.5", ["10.0.0.5:443"], tmp_path, now=time.time())
    assert answers["state"] == "ghost"
    again = ghost_state_apply("10.0.0.5", ["10.0.0.5:443"], tmp_path, now=time.time() + 10)
    assert again["since"] == answers["since"]
    assert again["answers"] == ["10.0.0.5:443"]
    cleared = ghost_state_apply("10.0.0.5", [], tmp_path, now=time.time() + 20)
    assert cleared["state"] == "cleared"
    store = load_ghosts(tmp_path)
    assert store["hosts"]["10.0.0.5"]["state"] == "cleared"


def test_ghost_state_apply_ignores_empty_host(tmp_path: Path) -> None:
    """Empty host values never enter the ghost store."""
    ghost_state_apply("", ["10.0.0.5:443"], tmp_path)
    assert load_ghosts(tmp_path)["hosts"] == {}


# ---------------------------------------------------------------- stats


def test_snapshot_engagement_counts_campaign(tmp_path: Path) -> None:
    """One snapshot counts hosts, owned, findings by severity and heat."""
    world = _world(
        {
            "10.0.0.5": {"state": "owned", "services": {"22": _svc("ssh")}},
            "10.0.0.6": {"state": "scanned", "services": {}},
        }
    )
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    first = snapshot_engagement(tmp_path, now=time.time())
    assert first["hosts"] == 2
    assert first["owned"] == 1
    (tmp_path / "lazy_stats_history.jsonl").write_text(
        json.dumps({"date": "1970-01-01", "hosts": 0}) + "\n", encoding="utf-8"
    )
    second = snapshot_engagement(tmp_path, now=time.time() + 3600)
    assert second["hosts"] == 2
    rows = (tmp_path / "lazy_stats_history.jsonl").read_text().splitlines()
    assert json.loads(rows[-1])["hosts"] == 2


def test_snapshot_engagement_cooldown(tmp_path: Path) -> None:
    """A snapshot taken inside the cooldown window is skipped."""
    world = _world({"10.0.0.5": {"state": "scanned", "services": {}}})
    (tmp_path / "world_model.json").write_text(json.dumps(world))
    first = snapshot_engagement(tmp_path, now=time.time())
    assert first is not None
    second = snapshot_engagement(tmp_path, now=time.time() + 60)
    assert second is None
