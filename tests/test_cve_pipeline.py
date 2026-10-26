"""CVE pipeline tests: loop/apt_chain findings must reach the intel graph."""

from pathlib import Path

import pytest

from modules.intel_fusion import build_intel_graph, write_summary
from modules.lazy_bridge import _extract_hosts_from_graph


def _graph_payload(nodes: list[dict]) -> dict:
    """Experiment graph payload shaped like lazy_graph output."""
    return {"nodes": nodes, "edges": []}


def test_extract_hosts_captures_services_versions_and_cves() -> None:
    """Per-port scans with banners and CVE mentions map to observations."""
    graph = _graph_payload(
        [
            {"node_id": 1, "kind": "fact", "state": "done", "text": "21/tcp open ftp vsftpd 2.3.4 on 192.168.1.152"},
            {"node_id": 2, "kind": "finding", "state": "done", "text": "samba usermap RCE CVE-2017-7494 on 192.168.1.152"},
            {"node_id": 3, "kind": "fact", "state": "done", "text": "OS: Linux 2.6.9 - 2.6.33 at 192.168.1.152"},
        ]
    )
    obs = _extract_hosts_from_graph(graph)
    assert "192.168.1.152" in obs
    entry = obs["192.168.1.152"]
    assert {"port": "21", "name": "ftp", "version": "vsftpd 2.3.4"} in entry["services"]
    assert "CVE-2017-7494" in entry["cves"]
    assert "Linux" in entry["os"] or "linux" in entry["os"].lower()


class _StubWorld:
    """Minimal world-model double for bridge tests."""

    def __init__(self) -> None:
        self.data = {"hosts": {}, "vulnerabilities": []}

    def add_host(self, ip: str) -> None:
        self.data["hosts"].setdefault(ip, {"ip": ip, "services": {}})

    def set_os_hint(self, ip: str, hint: str) -> None:
        self.add_host(ip)
        self.data["hosts"][ip]["os_hint"] = hint

    def add_service(self, ip: str, port: int, name: str = "", version: str = "", protocol: str = "tcp") -> None:
        self.add_host(ip)
        self.data["hosts"][ip]["services"][str(port)] = {"port": port, "name": name, "version": version}

    def add_vulnerability(self, description: str, host: str = "", cve: str = "", severity: str = "UNKNOWN") -> None:
        self.data["vulnerabilities"].append({"description": description, "host": host, "cve": cve, "severity": severity})

    def snapshot(self) -> dict:
        return dict(self.data)


def test_pull_to_world_model_writes_services_and_cves(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """The bridge lands services, CVEs and OS on the world model."""
    import modules.lazy_bridge as bridge
    import modules.world_model as wm_module

    fake_graph = _graph_payload(
        [
            {"node_id": 1, "kind": "fact", "state": "done", "text": "445/tcp open netbios-ssn Samba smbd 3.0.20-Debian on 10.10.10.5"},
            {"node_id": 2, "kind": "finding", "state": "done", "text": "CVE-2017-7494 reproduced on 10.10.10.5"},
        ]
    )
    stub = _StubWorld()
    monkeypatch.setattr(bridge, "lazy_tasks", lambda: {"t0001": {"goal": "x", "status": "running"}})
    monkeypatch.setattr(bridge, "lazy_graph", lambda task_id: fake_graph)
    monkeypatch.setattr(bridge, "lazy_assets", lambda: [])
    monkeypatch.setattr(wm_module, "get_world_model", lambda: stub)

    summary = bridge.pull_to_world_model()
    assert summary["services"] >= 1
    assert summary["vulnerabilities"] >= 1

    host = stub.data["hosts"].get("10.10.10.5") or {}
    services = {str(p): s for p, s in host.get("services", {}).items()}
    assert any(s.get("version") for s in services.values())
    cves = {str(v.get("cve")): v for v in stub.data.get("vulnerabilities", []) if v.get("host") == "10.10.10.5"}
    assert "CVE-2017-7494" in cves


def test_intel_graph_exposes_cve_nodes_with_heat() -> None:
    """World-model vulnerabilities with CVE ids become heat-attributed cve nodes."""
    import json

    payload = {
        "phase": "exploit",
        "hosts": {
            "10.99.0.9": {
                "ip": "10.99.0.9",
                "state": "scanned",
                "os_hint": "Linux",
                "services": {"445": {"port": 445, "protocol": "tcp", "name": "netbios-ssn", "version": "", "state": "open"}},
                "notes": [],
                "last_updated": "",
            }
        },
        "vulnerabilities": [
            {"description": "samba usermap script RCE", "host": "10.99.0.9", "cve": "CVE-2017-7494", "severity": "critical"}
        ],
        "credentials": [],
        "emails": [],
        "domains": [],
    }
    wm_dir = Path("/tmp/opencode/lazyown_intel_test_sessions")
    wm_dir.mkdir(parents=True, exist_ok=True)
    (wm_dir / "world_model.json").write_text(json.dumps(payload))
    g = build_intel_graph(wm_dir, est_cap=0)
    cves = [n for n in g["nodes"] if n.get("kind") == "cve"]
    assert any(n.get("value") == "CVE-2017-7494" for n in cves)
    node = next(n for n in cves if n.get("value") == "CVE-2017-7494")
    assert node.get("heat") in ("hot", "warm", "cold")
    summary = write_summary(g, wm_dir)
    top = {row["host"]: row for row in summary["top_exposed"]}
    assert "10.99.0.9" in top
    assert top["10.99.0.9"]["score_detail"]
