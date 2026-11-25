"""Contract tests for the Campaign Explorer (SessionIndex + C2 blueprint).

Covers artefact classification, path-traversal fail-closed resolution,
the plain-text viewer, the evidence search, host-card aggregation over
world-model/findings/outcomes/beacon history, and the scope frontier
ranking with in-scope/out-of-scope marking.
"""

from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path

import pytest
from flask import Flask
from flask_login import LoginManager

FIXED_NOW = 1_800_000_000.0
DAY = 86400
SCOPE_ENTRY = "10.10.10.5/32"
IN_SCOPE_HOST = "10.10.10.5"
OUT_SCOPE_HOST = "10.10.10.9"


def _sessions_tree(tmp_path: Path) -> Path:
    """Build a synthetic sessions tree covering every indexed source."""
    root = tmp_path / "sessions"
    if (root / "outcomes.jsonl").exists():
        return root
    (root / "findings").mkdir(parents=True)
    (root / "loot").mkdir()
    recent = FIXED_NOW - 60
    stale = FIXED_NOW - 8 * DAY

    (root / "world_model.json").write_text(
        json.dumps(
            {
                "hosts": {
                    IN_SCOPE_HOST: {
                        "ip": IN_SCOPE_HOST,
                        "state": "exploited",
                        "os_hint": "linux",
                        "services": {
                            "22": {"port": 22, "name": "ssh", "version": "8.2", "protocol": "tcp", "state": "open"},
                            "80": {"port": 80, "name": "http", "version": "2.4.49", "protocol": "tcp", "state": "open"},
                        },
                    },
                    OUT_SCOPE_HOST: {"ip": OUT_SCOPE_HOST, "state": "scanned", "os_hint": "", "services": {}},
                },
                "credentials": [
                    {
                        "value": "admin:Sup3rSecret",
                        "host": IN_SCOPE_HOST,
                        "service": "ssh",
                        "confirmed": True,
                        "found_at": "now",
                    },
                    {"value": "12:34", "host": IN_SCOPE_HOST, "service": "", "confirmed": False, "found_at": "now"},
                ],
            }
        )
    )
    (root / "findings" / f"{IN_SCOPE_HOST}.jsonl").write_text(
        json.dumps(
            {
                "id": "f1",
                "title": "Path traversal RCE",
                "state": "confirmed",
                "severity": "critical",
                "target": IN_SCOPE_HOST,
                "technique_id": "T1210",
            }
        )
        + "\n"
    )
    (root / "outcomes.jsonl").write_text(
        json.dumps(
            {
                "ts": recent,
                "event": {
                    "kind": "exploit",
                    "target": IN_SCOPE_HOST,
                    "severity": "critical",
                    "success": True,
                    "shell": True,
                    "port": "80",
                    "title": "CVE-2021-41773",
                },
            }
        )
        + "\n"
    )
    (root / "scan_10.10.10.9.nmap").write_text("Nmap scan report for host\nPORT STATE\n445/tcp open smb\n")
    (root / "credentials_10.10.10.5.txt").write_text("admin:Sup3rSecret\nsvc: filler\n")
    (root / "hashes_dump.txt").write_text("aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0\n")
    beacon_ts = datetime.fromtimestamp(recent, tz=UTC).isoformat()
    (root / "linux_beacon.records.jsonl").write_text(
        json.dumps(
            {
                "client_id": "linux_beacon",
                "ips": IN_SCOPE_HOST,
                "user": "www-data",
                "hostname": "web01",
                "timestamp": beacon_ts,
                "command": "id",
            }
        )
        + "\n"
    )
    (root / "loot" / "captured.bin").write_bytes(b"\x00\x01binary\x00")
    (root / "loot" / "notes.txt").write_text("operator note\n")
    for path in root.rglob("*"):
        if path.is_file():
            mtime = stale if path.name.startswith("scan_") else recent
            os.utime(path, (mtime, mtime))
    return root


def _index(tmp_path: Path):
    from modules.session_index import SessionIndex

    return SessionIndex(_sessions_tree(tmp_path), now=lambda: FIXED_NOW)


def test_classify_rules():
    from modules.session_index import classify

    assert classify("scan_10.10.10.9.nmap") == ("scan", "10.10.10.9")
    assert classify("findings/172.17.0.4.jsonl") == ("findings", "172.17.0.4")
    assert classify("linux_beacon.records.jsonl") == ("beacon_history", "")
    assert classify("credentials_10.10.10.5.txt") == ("creds", "10.10.10.5")
    assert classify("hashes_dump.txt") == ("hashes", "")
    assert classify("outcomes.jsonl") == ("outcomes", "")
    assert classify("world_model.json") == ("world_model", "")
    assert classify("lazy/activity_t0001.jsonl") == ("loop_run", "")
    assert classify("loot/captured.bin") == ("loot", "")


def test_resolve_safe_blocks_traversal_and_symlink(tmp_path):
    index = _index(tmp_path)
    assert index.resolve_safe("loot/notes.txt").is_file()
    with pytest.raises(PermissionError):
        index.resolve_safe("../payload.json")
    with pytest.raises(PermissionError):
        index.resolve_safe("/etc/passwd")
    with pytest.raises(ValueError):
        index.resolve_safe("")
    escape = tmp_path / "outside.txt"
    escape.write_text("secret")
    link = _sessions_tree(tmp_path) / "leak"
    link.symlink_to(escape)
    with pytest.raises(PermissionError):
        index.resolve_safe("leak")


def test_artifacts_classify_and_stale(tmp_path):
    index = _index(tmp_path)
    artifacts = {a.rel: a for a in index.artifacts()}
    scan = artifacts["scan_10.10.10.9.nmap"]
    assert scan.kind == "scan" and scan.host == OUT_SCOPE_HOST and scan.stale
    creds = artifacts["credentials_10.10.10.5.txt"]
    assert creds.kind == "creds" and not creds.stale
    assert artifacts["loot/captured.bin"].kind == "loot"


def test_read_caps_and_binary(tmp_path):
    index = _index(tmp_path)
    text = index.read("loot/notes.txt")
    assert text["exists"] and text["content"] == "operator note\n"
    binary = index.read("loot/captured.bin")
    assert binary["binary"] and binary["content"] == ""
    big = _sessions_tree(tmp_path) / "big.txt"
    big.write_text("x" * 1000)
    capped = index.read("big.txt", max_bytes=10)
    assert capped["truncated"] and len(capped["content"]) == 10
    assert not index.read("missing.txt")["exists"]
    assert not index.read("../payload.json")["exists"]


def test_search_semantics(tmp_path):
    index = _index(tmp_path)
    result = index.search("smb")
    paths = [m["path"] for m in result["matches"]]
    assert "scan_10.10.10.9.nmap" in paths
    assert result["match_count"] >= 1
    bad = index.search("[invalid")
    assert "invalid_regex" in bad.get("error", "")


def test_host_cards_aggregate(tmp_path):
    index = _index(tmp_path)
    cards = {c["ip"]: c for c in index.host_cards()}
    card = cards[IN_SCOPE_HOST]
    assert card["state"] == "exploited" and card["os_hint"] == "linux"
    assert [s["port"] for s in card["services"]] == [22, 80]
    assert card["findings"]["top_severity"] == "critical"
    assert card["outcomes"]["shells"] == 1
    assert "80" in card["worked_ports"] and "22" not in card["worked_ports"]
    cred_values = " ".join(c["display"] for c in card["credentials"])
    assert "ad*" in cred_values
    assert "conf 0.90" in " ".join(c["display"] for c in card["credentials"])
    bogus = [c for c in card["credentials"] if c["reason"] == "timestamp"]
    assert bogus and "conf" not in bogus[0]["display"]
    beacon = card["beacons"][0]
    assert beacon["client_id"] == "linux_beacon" and beacon["active"] and beacon["last_seen_age"] <= 90
    assert cards[OUT_SCOPE_HOST]["stale_recon"]


def test_scope_frontier_ranks_and_marks_scope(tmp_path):
    index = _index(tmp_path)
    frontier = {f["ip"]: f for f in index.scope_frontier({SCOPE_ENTRY})}
    inside = frontier[IN_SCOPE_HOST]
    outside = frontier[OUT_SCOPE_HOST]
    assert inside["in_scope"] and not outside["in_scope"]
    assert outside["score"] >= 3
    assert any("stale" in reason for reason in outside["reasons"])
    assert any("unworked" in reason for reason in outside["reasons"])
    scores = [f["score"] for f in index.scope_frontier({SCOPE_ENTRY})]
    assert scores == sorted(scores, reverse=True)
    unscoped = index.scope_frontier(None)
    assert all(f["in_scope"] for f in unscoped)


def test_overview_totals(tmp_path):
    data = _index(tmp_path).overview({SCOPE_ENTRY})
    assert data["totals"]["hosts"] >= 2
    assert data["totals"]["shells"] >= 1
    assert "scan" in data["artifacts_by_kind"] and "findings" in data["artifacts_by_kind"]
    assert data["frontier"]


@pytest.fixture()
def _campaign_app(tmp_path, monkeypatch):
    """Factory app wired to the synthetic sessions tree with auto-login."""
    from lazyc2.blueprints.campaign import campaign_bp

    app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent.parent / "templates"), static_folder=None)
    app.secret_key = "test"
    app.config["SESSIONS_DIR"] = str(_sessions_tree(tmp_path))
    manager = LoginManager(app)
    manager.user_loader(lambda _user_id: None)
    manager.login_view = "login"

    @app.route("/login")
    def login():
        return "login", 200

    class _TestOperator:
        id = "1"
        username = "tester"
        is_authenticated = True
        is_active = True

        def get_id(self) -> str:
            return self.id

    @app.before_request
    def _auto_login():
        from flask_login import login_user

        login_user(_TestOperator())

    app.register_blueprint(campaign_bp)
    for endpoint in _PAGE_STUB_ENDPOINTS:
        if endpoint not in app.view_functions:
            app.add_url_rule(f"/__stub__/{endpoint}", endpoint=endpoint, view_func=lambda: "stub")
    monkeypatch.setattr("lazyc2.blueprints.campaign._payload_entries", lambda: [SCOPE_ENTRY])
    monkeypatch.setattr("lazyc2.blueprints.campaign._campaign_label", lambda: "htb-season")
    return app.test_client()


def test_blueprint_overview_and_host(_campaign_app):
    response = _campaign_app.get("/api/campaign/overview")
    assert response.status_code == 200
    data = response.get_json()
    assert data["campaign"] == "htb-season"
    assert data["scope"]["entries"] == [SCOPE_ENTRY]
    assert data["totals"]["hosts"] >= 2
    host = _campaign_app.get(f"/api/campaign/host/{IN_SCOPE_HOST}")
    assert host.status_code == 200
    assert host.get_json()["in_scope"] is True
    assert _campaign_app.get("/api/campaign/host/9.9.9.9").status_code == 404


def test_blueprint_file_viewer_guard(_campaign_app):
    viewer = _campaign_app.get("/api/campaign/file", query_string={"path": "loot/notes.txt"})
    assert viewer.status_code == 200
    assert viewer.mimetype == "text/plain"
    assert viewer.headers["X-Content-Type-Options"] == "nosniff"
    assert b"operator note" in viewer.data
    traversal = _campaign_app.get("/api/campaign/file", query_string={"path": "../../payload.json"})
    assert traversal.status_code == 403
    assert _campaign_app.get("/api/campaign/file", query_string={"path": "missing.txt"}).status_code == 404
    binary = _campaign_app.get("/api/campaign/file", query_string={"path": "loot/captured.bin"})
    assert binary.status_code == 200
    assert b"binary artifact" in binary.data


def test_blueprint_search(_campaign_app):
    empty = _campaign_app.get("/api/campaign/search")
    assert empty.status_code == 400
    result = _campaign_app.get("/api/campaign/search", query_string={"q": "smb"})
    assert result.status_code == 200
    data = result.get_json()
    assert data["match_count"] >= 1
    assert any(m["path"] == "scan_10.10.10.9.nmap" for m in data["matches"])


_PAGE_STUB_ENDPOINTS = (
    "index",
    "profile",
    "phishing.list_campaigns",
    "addons.list_addons",
    "edit_notes",
    "get_event_config_view",
    "list_tools",
    "tasks",
    "cves",
    "report",
    "banners",
    "connect",
    "graph",
    "mitre",
    "palette_view",
    "lazyreport_view",
    "killchain_view",
    "intel_view",
    "intel_bundle_view",
    "attack3d_view",
    "attack_bundle_view",
    "lazybox.lazybox_page",
    "campaign.campaign_page",
    "login",
    "logout",
    "register",
)


def test_blueprint_page_renders(_campaign_app):
    response = _campaign_app.get("/campaign")
    assert response.status_code == 200
    assert b"Campaign Explorer" in response.data


def test_blueprint_requires_session(monkeypatch, tmp_path):
    from lazyc2.blueprints.campaign import campaign_bp

    app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent.parent / "templates"), static_folder=None)
    app.secret_key = "test"
    app.config["SESSIONS_DIR"] = str(_sessions_tree(tmp_path))
    manager = LoginManager(app)
    manager.user_loader(lambda _user_id: None)
    manager.login_view = "login"

    @app.route("/login")
    def login():
        return "login", 200

    app.register_blueprint(campaign_bp)
    client = app.test_client()
    response = client.get("/api/campaign/overview")
    assert response.status_code == 302 and "/login" in response.headers["Location"]
    time.sleep(0)
