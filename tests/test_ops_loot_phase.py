"""Tests for unified loot, cred-graph view, and quantitative phase progress.

Covers the loot model and operator helpers added to ``cli/ops_commands.py``
(``gather_loot`` / ``loot_show`` / ``loot_search`` / ``loot_reuse`` /
``loot_graph`` / ``loot_mark`` / ``resolve_cred_value`` / ``phase_progress``)
and the symmetric ``WorldModel.link_credential_to_failure`` cred-graph edge.

All tests run against ``tmp_path`` session fixtures — no mocking of real
``sessions/`` artefacts, per the project's integration-first test policy.
"""

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
for _p in (str(_ROOT), str(_ROOT / "modules")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from cli.ops_commands import (  # noqa: E402
    LootEntry,
    gather_loot,
    loot_graph,
    loot_mark,
    loot_reuse,
    loot_search,
    loot_show,
    phase_progress,
    resolve_cred_value,
)


def _seed_loot(sessions_dir: Path) -> None:
    """Write a credentials file and a hash file with a comment and blank line."""
    (sessions_dir / "credentials.txt").write_text(
        "# captured creds\nadmin:Passw0rd!\n\nsvc_sql:Summer2024\n",
        encoding="utf-8",
    )
    (sessions_dir / "hash1.txt").write_text(
        "administrator:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0\n",
        encoding="utf-8",
    )


def _write_world(sessions_dir: Path, world: dict) -> None:
    (sessions_dir / "world_model.json").write_text(json.dumps(world), encoding="utf-8")


# ── loot model ────────────────────────────────────────────────────────────────


def test_gather_loot_parses_kinds_and_skips_noise(tmp_path):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    entries = gather_loot(str(sess))
    assert [(e.user, e.kind) for e in entries] == [
        ("admin", "cleartext"),
        ("svc_sql", "cleartext"),
        ("administrator", "hash"),
    ]


def test_loot_entry_value():
    assert LootEntry("f", "cleartext", "admin", "pw").value == "admin:pw"
    assert LootEntry("f", "cleartext", "lonely", "").value == "lonely"


def test_resolve_cred_value_precedence():
    entries = [
        LootEntry("f", "cleartext", "admin", "pw1"),
        LootEntry("f", "cleartext", "service-admin", "pw2"),
    ]
    assert resolve_cred_value("admin", entries) == "admin:pw1"
    assert resolve_cred_value("admin:pw1", entries) == "admin:pw1"
    assert resolve_cred_value("pw2", entries) == "service-admin:pw2"
    assert resolve_cred_value("nope", entries) is None
    assert resolve_cred_value("", entries) is None


# ── loot_show / loot_search ─────────────────────────────────────────────────────


def test_loot_show_renders_table(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    loot_show(str(sess))
    out = capsys.readouterr().out
    assert "Loot" in out and "admin" in out and "3 credential" in out


def test_loot_show_empty(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    loot_show(str(sess))
    assert "No l00t" in capsys.readouterr().out


def test_loot_search_hits_and_provenance(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    (sess / "LazyOwn_session_report.csv").write_text(
        "timestamp,command\n2026-01-01,secretsdump admin found admin:Passw0rd!\n",
        encoding="utf-8",
    )
    loot_search("admin", str(sess))
    out = capsys.readouterr().out
    assert "admin" in out and "administrator" in out
    assert "first seen in log" in out


def test_loot_search_no_match(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    loot_search("zzz", str(sess))
    assert "no credentials match" in capsys.readouterr().out


def test_loot_search_requires_query(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    loot_search("  ", str(sess))
    assert "query required" in capsys.readouterr().out


# ── loot_reuse ──────────────────────────────────────────────────────────────────


def test_loot_reuse_no_target(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    loot_reuse("", str(sess))
    assert "no target" in capsys.readouterr().out


def test_loot_reuse_no_loot(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    loot_reuse("10.0.0.1", str(sess))
    assert "No l00t to reuse" in capsys.readouterr().out


def test_loot_reuse_excludes_rejected_and_flags_confirmed(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _seed_loot(sess)
    _write_world(
        sess,
        {
            "hosts": {"10.0.0.1": {"state": "enumerated", "services": {}}},
            "network_graph": {
                "relations": [
                    {"source": "cred:admin:Passw0", "target": "host:10.0.0.2", "relation": "authenticates_to"},
                    {"source": "cred:svc_sql:Summ", "target": "host:10.0.0.1", "relation": "rejected_by"},
                ]
            },
        },
    )
    loot_reuse("10.0.0.1", str(sess))
    out = capsys.readouterr().out
    assert "confirmed elsewhere" in out
    assert "admin" in out
    assert "svc_sql" not in out  # rejected against this host -> excluded


# ── loot_graph ──────────────────────────────────────────────────────────────────


def test_loot_graph_renders_edges(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    _write_world(
        sess,
        {
            "network_graph": {
                "relations": [
                    {"source": "host:10.0.0.1", "target": "cred:admin:Passw0", "relation": "exposes_credential"},
                    {"source": "cred:admin:Passw0", "target": "host:10.0.0.2", "relation": "authenticates_to"},
                    {"source": "cred:admin:Passw0", "target": "host:10.0.0.3", "relation": "rejected_by"},
                    {"source": "cred:admin:Passw0", "target": "host:10.0.0.4", "relation": "may_authenticate_to"},
                ]
            }
        },
    )
    loot_graph(str(sess))
    out = capsys.readouterr().out
    assert "Credential graph" in out
    assert "10.0.0.1" in out and "10.0.0.2" in out and "10.0.0.3" in out


def test_loot_graph_empty(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    loot_graph(str(sess))
    assert "No credential graph yet" in capsys.readouterr().out


# ── loot_mark (end-to-end into world_model.json) ────────────────────────────────


def test_loot_mark_writes_rejected_edge(tmp_path):
    import modules.world_model as wmmod

    wmmod._default_wm = None
    try:
        sess = tmp_path / "sessions"
        sess.mkdir()
        (sess / "credentials.txt").write_text("admin:Passw0rd!\n", encoding="utf-8")
        assert loot_mark("admin", "rejected", "10.0.0.9", sessions_dir=str(sess)) is True
        data = json.loads((sess / "world_model.json").read_text(encoding="utf-8"))
        rels = data["network_graph"]["relations"]
        assert any(r["relation"] == "rejected_by" and r["target"] == "host:10.0.0.9" for r in rels)
    finally:
        wmmod._default_wm = None


def test_loot_mark_rejects_bad_outcome(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    (sess / "credentials.txt").write_text("admin:pw\n", encoding="utf-8")
    assert loot_mark("admin", "bogus", "10.0.0.1", sessions_dir=str(sess)) is False
    assert "worked" in capsys.readouterr().out


def test_loot_mark_unknown_credential(tmp_path, capsys):
    sess = tmp_path / "sessions"
    sess.mkdir()
    (sess / "credentials.txt").write_text("admin:pw\n", encoding="utf-8")
    assert loot_mark("ghost", "worked", "10.0.0.1", sessions_dir=str(sess)) is False
    assert "no captured credential matches" in capsys.readouterr().out


# ── phase_progress ──────────────────────────────────────────────────────────────


def test_phase_progress_ranks(tmp_path):
    sess = tmp_path / "sessions"
    sess.mkdir()
    world = {"hosts": {"a": {"state": "scanned", "services": {"80": {}}}}}
    pp = phase_progress(world, str(sess))
    assert pp["recon"] == 0.5  # host present, OS not identified
    assert pp["scan"] == 1.0
    assert pp["enum"] == 0.25  # service-presence floor, not enumerated
    assert pp["exploit"] == 0.0
    assert pp["report"] == 0.0


def test_phase_progress_completed_override(tmp_path):
    sess = tmp_path / "sessions"
    sess.mkdir()
    world = {"hosts": {}, "completed_phases": ["recon", "scan"]}
    pp = phase_progress(world, str(sess))
    assert pp["recon"] == 1.0
    assert pp["scan"] == 1.0
    assert pp["exploit"] == 0.0


def test_phase_progress_os_owned_report_and_loot(tmp_path):
    sess = tmp_path / "sessions"
    sess.mkdir()
    (sess / "os.json").write_text(json.dumps([{"state": "active"}]), encoding="utf-8")
    (sess / "report_20260101_000000.md").write_text("# report", encoding="utf-8")
    (sess / "credentials.txt").write_text("admin:pw\n", encoding="utf-8")
    world = {"hosts": {"a": {"state": "owned", "services": {"22": {}}}}}
    pp = phase_progress(world, str(sess))
    assert pp["recon"] == 1.0  # host present + OS identified
    assert pp["privesc"] == 1.0  # host owned
    assert pp["exfil"] == 1.0  # loot captured
    assert pp["report"] == 1.0  # report artefact present
    assert pp["lateral"] == 0.0  # single host, no pivots


# ── world_model.link_credential_to_failure ──────────────────────────────────────


def test_link_credential_to_failure_edge_and_roundtrip(tmp_path):
    from world_model import WorldModel

    path = tmp_path / "wm.json"
    wm = WorldModel(path=str(path))
    wm.add_credential("svc:pw", host="10.0.0.1")
    wm.link_credential_to_success("svc:pw", "10.0.0.2")
    wm.link_credential_to_failure("svc:pw", "10.0.0.3")

    rels = wm.graph_snapshot()["relations"]
    assert any(r["relation"] == "rejected_by" and r["target"] == "host:10.0.0.3" for r in rels)
    assert any(r["relation"] == "authenticates_to" and r["target"] == "host:10.0.0.2" for r in rels)

    reloaded = WorldModel(path=str(path)).graph_snapshot()["relations"]
    assert any(r["relation"] == "rejected_by" for r in reloaded)
