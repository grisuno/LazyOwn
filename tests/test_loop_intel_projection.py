"""graph_state projects known assets, auto-findings carry class/CVE (bugs 2.4, 2.6).

2.4: the agent's ``graph_state`` read only the exploration graph, so bootstrap
intel was invisible and the agent re-ran recon. It now projects the global
asset coverage. 2.6: the auto-finding path titled every finding "possible issue
via <cmd>" and passed no class; it now derives a concrete class and CVE so the
ATT&CK technique resolves precisely.
"""

from __future__ import annotations

import json

import modules.lazy_loop as loop


def _sandbox(tmp_path, monkeypatch):
    """Redirect loop persistence into a scratch directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def test_derive_finding_class_maps_marks_and_cve():
    """A known mark yields its class; a lone CVE yields the cve class."""
    assert loop._derive_finding_class("parameter vulnerable to sqli; CVE-2020-1234") == ("sqli", "CVE-2020-1234")
    assert loop._derive_finding_class("got a root shell on host") == ("shell", "")
    assert loop._derive_finding_class("vsftpd backdoor CVE-2011-2523 triggered") == ("cve", "CVE-2011-2523")
    assert loop._derive_finding_class("nothing notable here") == ("", "")


def test_report_resolves_technique_from_vulnclass(tmp_path, monkeypatch):
    """An explicit vulnclass resolves the ATT&CK technique deterministically."""
    _sandbox(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph("tc")
    svc = loop.FindingService("tc", graph, loop.ActivityLog("tc"), None)
    node = svc.report(name="SQLI via sqlmap", summary="injectable", poc="sqlmap -u x", vulnclass="sqli")
    assert node.meta["technique_id"] == "T1190"
    assert node.meta["vulnclass"] == "sqli"
    assert "possible issue" not in node.meta["name"]


def test_graph_state_projects_known_assets(tmp_path, monkeypatch):
    """graph_state surfaces discovered assets so the agent does not re-scan."""
    _sandbox(tmp_path, monkeypatch)

    class _Graph:
        task_id = "t3"

        def overview(self):
            return {"facts": 1, "findings": 0, "fact_list": [], "intents": []}

    worker = loop.Worker.__new__(loop.Worker)
    worker.name = "w"
    worker.graph = _Graph()
    worker.assets = loop.AssetGraph()
    worker.assets.insert("service", "tcp/21 ftp")
    worker.assets.insert("service", "tcp/80 http")
    worker.assets.insert("ip", "172.17.0.2")

    intent = type("Intent", (), {"node_id": 5, "text": "enum"})()
    specs = loop.Worker._agent_tools(worker, intent, None, [], None, None, {})
    graph_state = next(spec["func"] for spec in specs if spec["name"] == "graph_state")
    state = json.loads(graph_state())

    assert state["facts_total"] == 1
    known = state["known_assets"]
    assert known["total"] == 3
    assert known["by_type"].get("service", {}).get("total") == 2
    assert any("ftp" in sample for sample in known["services"])


def test_writeback_finding_has_concrete_class_and_name(tmp_path, monkeypatch):
    """A writeback finding is titled by class/CVE and passes the vulnclass."""
    _sandbox(tmp_path, monkeypatch)
    captured: dict = {}

    class _FindingService:
        def __init__(self, *args, **kwargs):
            pass

        def report(self, **kwargs):
            captured.update(kwargs)
            return loop.ExplorationNode(node_id=9, kind="finding", text=str(kwargs.get("name", "")))

    class _Evidence:
        def __init__(self, *args, **kwargs):
            pass

        def add(self, *args, **kwargs):
            return None

    monkeypatch.setattr(loop, "FindingService", _FindingService)
    monkeypatch.setattr(loop, "EvidenceStore", _Evidence)

    class _Graph:
        task_id = "t6"

        def add_node(self, kind, text, **kwargs):
            return loop.ExplorationNode(node_id=7, kind=kind, text=str(text))

        def add_edge(self, *args, **kwargs):
            return None

        def has_finding(self, text):
            return None

        def anchors_for(self, node_id):
            return []

        def anchor(self, *args, **kwargs):
            return None

    class _Assets:
        def insert(self, *args, **kwargs):
            raise ValueError("no asset")

    class _Traffic:
        def read(self, _n):
            return []

        def bind(self, *args, **kwargs):
            return None

    worker = loop.Worker.__new__(loop.Worker)
    worker.name = "w"
    worker.graph = _Graph()
    worker.assets = _Assets()
    worker.traffic = _Traffic()
    worker.activity = loop.ActivityLog("t6")
    worker.store = None
    worker.task_id = "t6"

    transcripts = [("sqlmap -u http://x", "parameter is vulnerable to sqli; CVE-2020-1234 confirmed")]
    worker._writeback(type("Intent", (), {"node_id": 3, "text": "enum"})(), transcripts, allow_finding=True)

    assert captured, "a finding should have been reported"
    assert captured["vulnclass"] == "sqli"
    assert captured["name"].startswith("CVE-2020-1234")
    assert "possible issue" not in captured["name"]
