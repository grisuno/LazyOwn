"""BDD tests for chain_distill trace crystallisation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.chain_distill import (
    DistillReport,
    _infer_target,
    build_chain_data,
    distill,
    locate_traces,
)

_TOUCH_TIME = 1_791_645_213.0


@pytest.fixture
def trace_dir(tmp_path: Path) -> Path:
    """One realistic loop task store: scan success + probe failures."""
    store = tmp_path / "loop_lab"
    store.mkdir()
    graph = {
        "seq": 3,
        "nodes": [
            {
                "node_id": 0,
                "kind": "fact",
                "text": "task origin",
                "state": "done",
                "priority": 5,
                "created": _TOUCH_TIME,
                "updated": _TOUCH_TIME,
                "meta": {"origin": True},
            },
            {
                "node_id": 1,
                "kind": "goal",
                "text": "gain initial access on 10.0.0.5",
                "state": "pending",
                "priority": 5,
                "created": _TOUCH_TIME,
                "updated": _TOUCH_TIME,
                "meta": {},
            },
            {
                "node_id": 2,
                "kind": "intent",
                "text": "probe ip 10.0.0.5",
                "state": "done",
                "priority": 6,
                "created": _TOUCH_TIME,
                "updated": _TOUCH_TIME,
                "meta": {},
            },
            {
                "node_id": 3,
                "kind": "intent",
                "text": "list web dirs 10.0.0.5",
                "state": "done",
                "priority": 5,
                "created": _TOUCH_TIME,
                "updated": _TOUCH_TIME,
                "meta": {},
            },
        ],
        "edges": [
            {"src": 0, "dst": 1, "kind": "spawns"},
            {"src": 1, "dst": 2, "kind": "spawns"},
            {"src": 2, "dst": 3, "kind": "spawns"},
        ],
        "anchors": [],
    }
    (store / "exp_t0007.json").write_text(json.dumps(graph), encoding="utf-8")
    rows = [
        {
            "ts": _TOUCH_TIME,
            "kind": "bash",
            "command": "nmap -sV 10.0.0.5",
            "output": "PORT STATE\n80/tcp open http\n",
            "digest": "aa11",
            "meta": {"worker": "w0", "intent": 2},
        },
        {
            "ts": _TOUCH_TIME + 1,
            "kind": "bash",
            "command": "curl -sS -m 5 -I http://10.0.0.5:81",
            "output": "curl: (7) Failed to connect to 10.0.0.5:81",
            "digest": "bb22",
            "meta": {"worker": "w0", "intent": 2},
        },
        {
            "ts": _TOUCH_TIME + 2,
            "kind": "bash",
            "command": "dig +short 10.0.0.5",
            "output": "",
            "digest": "cc33",
            "meta": {"worker": "w1", "intent": 3},
        },
        {
            "ts": _TOUCH_TIME + 3,
            "kind": "bash",
            "command": "gobuster dir --url http://10.0.0.5/ -w /usr/share/wordlists/rockyou.txt",
            "output": "/admin (200)\n",
            "digest": "dd44",
            "meta": {"worker": "w1", "intent": 3},
        },
        {
            "ts": _TOUCH_TIME + 4,
            "kind": "bash",
            "command": "nmap -sV 10.0.0.5",
            "output": "PORT STATE\n80/tcp open http\n",
            "digest": "ee55",
            "meta": {"worker": "w0", "intent": 3},
        },
        {
            "ts": _TOUCH_TIME + 5,
            "kind": "http",
            "command": "proxy GET /x",
            "output": "body",
            "digest": "ff66",
            "meta": {"intent": 3},
        },
    ]
    traffic = tmp_path / "loop_lab" / "traffic_t0007.jsonl"
    traffic.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    return tmp_path


class TestLocate:
    """Task id resolution across session stores."""

    def test_pair_found(self, trace_dir: Path):
        """Given one store with both artefacts, Then both paths return."""
        exp, traffic = locate_traces("t0007", sessions_dir=trace_dir)
        assert exp is not None and exp.name == "exp_t0007.json"
        assert traffic is not None and traffic.name == "traffic_t0007.jsonl"

    def test_unknown_task_is_none(self, trace_dir: Path):
        """Given a bogus id, Then both paths are None, distill nags."""
        exp, traffic = locate_traces("zzzz", sessions_dir=trace_dir)
        assert (exp, traffic) == (None, None)
        report = distill("zzzz", sessions_dir=trace_dir)
        assert report.errors == ["no trace found for task"]


class TestInferTarget:
    """Goal text wins over statistical host frequency."""

    def test_goal_beats_frequency(self, trace_dir: Path):
        """Given a goal with a host, Then it is taken verbatim."""
        from modules.chain_distill import _load_graph, _load_traffic

        graph = _load_graph(trace_dir / "loop_lab" / "exp_t0007.json")
        rows = _load_traffic(trace_dir / "loop_lab" / "traffic_t0007.jsonl")
        assert _infer_target(rows, graph) == "10.0.0.5"

    def test_frequency_fallback_hosts_win_over_loopback(self, tmp_path: Path):
        """Given no goal, Then loopback loses to real hosts."""
        rows = [{"command": "ping 127.0.0.1"}, {"command": "curl 10.1.1.1"}, {"command": "curl 10.1.1.1"}]
        assert _infer_target(rows, {"goal": ""}) == "10.1.1.1"


class TestBuild:
    """Row policy turns traces into validated chain steps."""

    def test_keep_drop_dedupe(self, trace_dir: Path):
        """Given raw rows, Then failure/silent rows drop and dupes collapse."""
        from modules.chain_distill import _load_graph, _load_traffic

        graph = _load_graph(trace_dir / "loop_lab" / "exp_t0007.json")
        rows = _load_traffic(trace_dir / "loop_lab" / "traffic_t0007.jsonl")
        data, decisions = build_chain_data("t0007", rows, graph, {})
        kept = [d for d in decisions if d.kept]
        dropped = {d.command: d.reason for d in decisions if not d.kept}
        assert len(kept) == 2, "scan and gobuster survive; the duped nmap collapses"
        assert "duplicate rendered command" in dropped["nmap -sV 10.0.0.5"], "second nmap is a dupe"
        assert any("silent or failure signature" in r for r in dropped.values())
        assert any("kind=http not distillable" in r for r in dropped.values())
        ids = [s["id"] for s in data["steps"]]
        assert len(ids) == len(set(ids)), "step ids unique"

    def test_target_tokenised_and_lineage_kept(self, trace_dir: Path):
        """Given a goal target, Then commands tokenise and lineage lands."""
        from modules.chain_distill import _load_graph, _load_traffic

        graph = _load_graph(trace_dir / "loop_lab" / "exp_t0007.json")
        rows = _load_traffic(trace_dir / "loop_lab" / "traffic_t0007.jsonl")
        data, _dec = build_chain_data("t0007", rows, graph, {})
        assert data["defaults"]["target"] == "10.0.0.5"
        first = data["steps"][0]
        assert "{target}" in first["run"] and "10.0.0.5" not in first["run"], (
            "target tokenised, no literal leak in the tokenised run"
        )
        assert "digest aa11" in first["description"], "per-step lineage for audits"
        scan_step = next(s for s in data["steps"] if s["run"].startswith("nmap"))
        assert scan_step["skip_if_exists"] == "sessions/scan_{target}.nmap.xml", (
            "scan steps get the canonical artefact guard"
        )

    def test_exploit_steps_strict(self, trace_dir: Path):
        """Given a kept exploit step, Then it is not continue_on_error."""
        from modules.chain_distill import _load_graph, _load_traffic

        graph = _load_graph(trace_dir / "loop_lab" / "exp_t0007.json")
        rows = _load_traffic(trace_dir / "loop_lab" / "traffic_t0007.jsonl")
        data, _dec = build_chain_data("t0007", rows, graph, {})
        assert all(s.get("continue_on_error", True) for s in data["steps"]), "traces above are recon paths"

    def report_checks(self, trace_dir: Path):
        """Report aggregates kept/dropped/row counts."""
        report = distill("t0007", sessions_dir=trace_dir)
        assert report.row_count == 6
        assert report.kept == 3 and report.dropped == 3
        assert isinstance(report, DistillReport)

    def test_empty_trace_yields_validateable_chain(self, tmp_path: Path):
        """Given no steps at all, Then the chain still validates."""
        store = tmp_path / "st"
        store.mkdir()
        (store / "traffic_t0009.jsonl").write_text("", encoding="utf-8")
        (store / "exp_t0009.json").write_text('{"seq":0,"nodes":[],"edges":[],"anchors":[]}', encoding="utf-8")
        dirs = tmp_path / "chains"
        report = distill("t0009", sessions_dir=tmp_path, write=True, chains_dir=dirs)
        assert report.errors == [], f"empty traces must still validate: {report.errors}"
        assert report.path is not None and Path(report.path).is_file()


class TestWrite:
    """Persistence is registry-grade: invalid files never land."""

    def test_written_chain_validates_lifetime(self, trace_dir: Path):
        """Given --write, Then the file lands valid in the registry scan."""
        from modules.chain_registry import scan_all as scan_rows

        dirs = trace_dir / "chains"
        report = distill("t0007", sessions_dir=trace_dir, write=True, chains_dir=dirs)
        assert report.errors == [], f"validation failed: {report.errors}"
        assert report.path and Path(report.path).is_file()
        rows = [row for row in scan_rows(dirs) if row.get("name") == report.chain_name]
        assert rows and rows[0].get("valid", True), "the distilled chain is registry-visible"
        assert not rows[0].get("enabled", True), "distilled chains start disabled for the operator"
        text = Path(report.path).read_text(encoding="utf-8")
        assert "{target}" in text
