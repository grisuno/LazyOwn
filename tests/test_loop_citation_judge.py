"""Citation-first retest and fenced judge prompt integration."""

from __future__ import annotations

import time

import pytest

import modules.lazy_loop as loop
from modules.loop.boundary import CODE_TAIL, TAG, check_leakage


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    """Redirect loop persistence into a scratch directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


class FakeTraffic:
    def __init__(self, rows):
        self._rows = rows
        self.recorded = []

    def read(self, limit=200):
        return self._rows

    def record(self, kind, command, output="", meta=None):
        self.recorded.append((kind, command))
        return {}


def test_citation_verdict_reproduces_without_execution(sandbox):
    graph = loop.ExplorationGraph("tc")
    node = graph.add_node(
        "finding",
        'sqli confirmed: "uid=0(root) gid=0(root)" on target',
        state="pending",
        meta={"poc": "curl http://target/x"},
    )
    traffic = FakeTraffic(
        [
            {
                "command": "id",
                "output": "before\nuid=0(root)  gid=0(root)\nafter",
                "ts": time.time(),
                "digest": "abc",
            }
        ]
    )
    retester = loop.Retester(graph, loop.ActivityLog("tc"), traffic)
    verdict, evidence, attempts = retester._citation_verdict(graph.get(node.node_id))
    assert verdict == "reproduced"
    assert attempts == 0
    assert "[citation]" in evidence
    assert traffic.recorded == []


def test_citation_verdict_none_without_quote(sandbox):
    graph = loop.ExplorationGraph("tc")
    node = graph.add_node("finding", "plain finding without quotes", state="pending", meta={"poc": "curl http://x"})
    retester = loop.Retester(graph, loop.ActivityLog("tc"), FakeTraffic([]))
    assert retester._citation_verdict(graph.get(node.node_id)) is None


def test_citation_verdict_none_when_output_stale(sandbox, monkeypatch):
    graph = loop.ExplorationGraph("tc")
    node = graph.add_node(
        "finding",
        'sqli: "uid=0(root) gid=0(root)" here',
        state="pending",
        meta={"poc": "curl"},
    )
    monkeypatch.setattr(
        loop, "citation_service_bound", lambda: loop.citation_service_bound().__class__(max_age_sec=1.0)
    )
    traffic = FakeTraffic(
        [{"command": "id", "output": "uid=0(root) gid=0(root)", "ts": time.time() - 9999, "digest": "x"}]
    )
    retester = loop.Retester(graph, loop.ActivityLog("tc"), traffic)
    assert retester._citation_verdict(graph.get(node.node_id)) is None


def test_report_binds_quote_meta(sandbox):
    graph = loop.ExplorationGraph("tc")
    service = loop.FindingService("tc", graph, loop.ActivityLog("tc"))
    node = service.report(name="sqli", summary='proof "uid=0(root) gid=0(root)" shown', poc="curl x")
    meta = graph.get(node.node_id).meta
    assert meta["quote"] == "uid=0(root) gid=0(root)"


def test_judge_prompt_fenced_when_enabled(sandbox, monkeypatch):
    from modules import orchestrator_config as oc

    monkeypatch.setattr(oc, "boundary_config", lambda: {"enabled": True})
    called = {}

    class FakePool:
        def members(self):
            return [1]

        def complete(self, prompt, max_tokens=200):
            called["prompt"] = prompt
            return "ALLOW"

    monkeypatch.setattr(loop, "LlmPool", FakePool)
    verdict = loop.judge_command("rm -rf /tmp/x")
    assert verdict["decision"] == "ALLOW"
    prompt = called["prompt"]
    assert f"<{TAG}-judge_request-" in prompt
    assert CODE_TAIL in prompt
    assert check_leakage(prompt) == []
