"""Loop trace and engagement collectors tests over synthetic sessions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules import loop_trace
from modules import report_engagement as re_engage
from modules.report_engagement import (
    aggregate_metrics,
    collect_loop_runs,
    render_beacons_html,
    render_loops_html,
)


@pytest.fixture()
def fake_sessions(tmp_path, monkeypatch):
    """Build a minimal sessions/lazy tree with one task."""
    lazy = tmp_path / "lazy"
    lazy.mkdir()
    (lazy / "tasks.json").write_text(
        json.dumps({"seq": 1, "tasks": {"t0001": {"task_id": "t0001", "goal": "php2shell", "status": "done"}}})
    )
    (lazy / "audit_t0001.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "ts": 100.0,
                        "kind": "run_start",
                        "goal": "php2shell",
                        "target": "10.0.0.5",
                        "rounds": 2,
                        "workers": 1,
                    }
                ),
                json.dumps(
                    {
                        "ts": 101.0,
                        "kind": "command",
                        "command": "nmap -sT -sV 10.0.0.5",
                        "ok": True,
                        "judge_action": "allow",
                        "opsec_gate": "allow",
                        "detection_prob": 0.2,
                        "step": "gain access",
                        "output_tail": "PORT STATE",
                    }
                ),
                json.dumps(
                    {
                        "ts": 102.0,
                        "kind": "command",
                        "command": "curl http://10.0.0.5",
                        "ok": False,
                        "judge_action": "deny",
                        "opsec_gate": "allow",
                        "detection_prob": 0.4,
                    }
                ),
                json.dumps(
                    {
                        "ts": 103.0,
                        "kind": "command",
                        "command": "nuclei -u http://10.0.0.5",
                        "ok": False,
                        "judge_action": "allow",
                        "opsec_gate": "allow",
                        "detection_prob": 0.4,
                    }
                ),
            ]
        )
        + "\n"
    )
    (lazy / "activity_t0001.jsonl").write_text(
        json.dumps({"ts": 101.5, "kind": "decompose", "text": "split goal", "worker": "engine"}) + "\n"
    )
    findings = lazy / "findings"
    findings.mkdir()
    (findings / "progress_t0001.json").write_text(
        json.dumps({"log": [{"signals": {"findings": 3, "reproduced": 1}}], "brief": {}})
    )
    monkeypatch.setattr(re_engage, "LAZY_DIR", lazy)
    monkeypatch.setattr(re_engage, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop_trace, "LAZY_DIR", lazy)
    return tmp_path


class TestCollectLoopRuns:
    def test_summary_counts(self, fake_sessions):
        runs = collect_loop_runs(fake_sessions / "lazy")
        assert len(runs) == 1
        run = runs[0]
        assert run.task_id == "t0001"
        assert run.goal == "php2shell"
        assert run.target == "10.0.0.5"
        assert run.commands == 3
        assert run.commands_ok == 1
        assert run.blocked == 1
        assert run.rounds == 2
        assert run.findings == 3
        assert run.reproduced == 1
        assert run.detection_avg == pytest.approx(1 / 3)

    def test_ok_rate(self, fake_sessions):
        run = collect_loop_runs(fake_sessions / "lazy")[0]
        assert run.ok_rate == pytest.approx(1 / 3)
        assert run.duration_sec == 3.0

    def test_metrics_aggregate(self, fake_sessions):
        runs = collect_loop_runs(fake_sessions / "lazy")
        metrics = aggregate_metrics(runs)
        assert metrics["commands"] == 3
        assert metrics["ok_rate"] == pytest.approx(0.333, abs=1e-3)
        assert metrics["blocked"] == 1
        assert metrics["findings"] == 3

    def test_missing_files_yield_no_runs(self, tmp_path):
        assert collect_loop_runs(tmp_path) == []


class TestRenderers:
    def test_loops_html_tables(self, fake_sessions):
        runs = collect_loop_runs(fake_sessions / "lazy")
        html = render_loops_html(runs, aggregate_metrics(runs))
        assert "t0001" in html and "php2shell" in html

    def test_beacons_html_rows(self, tmp_path, monkeypatch):
        monkeypatch.setattr(re_engage, "SESSIONS_DIR", tmp_path)
        record = tmp_path / "agent_x.records.jsonl"
        record.write_text(
            json.dumps(
                {
                    "client_id": "agent_x",
                    "hostname": "h1",
                    "ips": "10.0.0.5",
                    "user": "root",
                    "command": "id",
                    "output": "uid=0",
                }
            )
            + "\n"
        )
        sessions = re_engage.collect_beacon_sessions()
        html = render_beacons_html(sessions)
        assert "agent_x" in html and "root" in html

    def test_beacons_html_empty(self, tmp_path):
        assert render_beacons_html([]) == ""


class TestTrace:
    def test_timeline_merges_kinds(self, fake_sessions):
        trace = loop_trace.build_trace("t0001")
        kinds = {event["kind"] for event in trace["events"]}
        assert "command_ok" in kinds
        assert "command_fail" in kinds
        assert "worker" in kinds
        assert trace["summary"]["commands"] == 3

    def test_write_trace_artifact(self, fake_sessions):
        path = loop_trace.write_trace("t0001", out_path=fake_sessions / "trace.html")
        content = Path(path).read_text()
        assert "LazyOwn loop trace" in content
        assert "nmap" in content

    def test_unknown_task_zeroed_summary(self, fake_sessions):
        trace = loop_trace.build_trace("t9999")
        assert trace["summary"]["commands"] == 0

    def test_index_lists_tasks(self, fake_sessions):
        html = loop_trace.trace_index_html()
        assert "t0001" in html

    def test_event_store_rows_tolerate_missing_db(self, fake_sessions):
        assert isinstance(loop_trace._event_store_rows("t0001"), list)
