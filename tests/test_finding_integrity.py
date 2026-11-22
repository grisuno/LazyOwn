"""Typed finding integrity, TPD breaker and host-surface contracts."""

from __future__ import annotations

import time

import pytest

import modules.lazy_loop as loop
from core.host_policy import is_world_host
from modules.chain_registry import ChainStep, render_text, step_gate_verdict
from modules.loop.finding_class import class_for_finding, evidence_supports_class


def test_class_from_technique_metadata_not_output_keywords():
    meta = {"technique_id": "T1005"}
    assert class_for_finding(meta, "SQLI via atomic_tests T1005 sqlite dump") == "collection"


def test_class_vulnclass_priority():
    assert class_for_finding({"vulnclass": "sqli"}) == "sqli"


def test_class_text_technique_fallback():
    assert class_for_finding({}, "atomic_tests T1190 against app") == "auth_bypass"


def test_class_unknown_without_metadata():
    assert class_for_finding({}, "no technique here") == ""


def test_typed_predicate_requires_differential_signal():
    assert evidence_supports_class("sqli", "You have an error in your SQL syntax near 'x'")
    assert not evidence_supports_class("sqli", "sqlite3 users table dump")
    assert not evidence_supports_class("collection", "GET / HTTP/1.1 200 OK")
    assert evidence_supports_class("collection", "root:x:0:0:root:/root:/bin/bash")


def test_typed_predicate_fails_open_for_unknown_class():
    assert evidence_supports_class("never_seen_class", "anything")


def test_derive_finding_class_rejects_substring_marks():
    vulnclass, _cve = loop._derive_finding_class("atomic_tests T1005: sqlite3 users table dump")
    assert vulnclass == "collection"


def test_derive_finding_class_word_boundary():
    vulnclass, _cve = loop._derive_finding_class("hydra found valid credentials: admin:password")
    assert vulnclass == "credentials"


def test_derive_finding_class_prefers_technique_over_keywords():
    vulnclass, _cve = loop._derive_finding_class("SQLI claim in output while running T1083 file test")
    assert vulnclass == "lfi"
    assert loop._derive_finding_class("atomic_tests T1005 sqlite dump")[0] == "collection"


class FakeTraffic:
    def __init__(self, rows):
        self._rows = rows
        self.recorded = []

    def read(self, limit=200):
        return self._rows

    def record(self, kind, command, output="", meta=None):
        self.recorded.append((kind, command))
        return {}


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


def test_citation_gate_conclusive_only_with_typed_evidence(sandbox):
    graph = loop.ExplorationGraph("tc")
    node = graph.add_node(
        "finding",
        'collection via T1005: "sqlite3 users table dump" captured',
        state="pending",
        meta={"technique_id": "T1005", "poc": "atomic_tests T1005"},
    )
    traffic = FakeTraffic(
        [{"command": "atomic_tests T1005", "output": "sqlite3 users table dump", "ts": time.time(), "digest": "d"}]
    )
    retester = loop.Retester(graph, loop.ActivityLog("tc"), traffic)
    verdict, evidence, attempts = retester._citation_verdict(graph.get(node.node_id))
    assert verdict == "inconclusive"
    assert "collection" in evidence
    assert attempts == 0


def test_retest_severity_gated_on_inconclusive(sandbox):
    graph = loop.ExplorationGraph("tc")
    node = graph.add_node(
        "finding",
        "sqli via T1190",
        state="pending",
        meta={"severity": "high", "poc": "curl http://t/x"},
    )
    traffic = FakeTraffic([])
    retester = loop.Retester(graph, loop.ActivityLog("tc"), traffic)
    result = retester.retest(node.node_id, executor=lambda command: "HTTP/1.1 200 OK vulnerable")
    assert result["verdict"] == "inconclusive"
    finding = graph.get(node.node_id)
    assert finding.meta["severity_verified"] is False
    assert finding.meta["level"] == "identified"


def test_report_carries_declared_class_even_without_typed_evidence(sandbox):
    graph = loop.ExplorationGraph("tc")
    service = loop.FindingService("tc", graph, loop.ActivityLog("tc"), None)
    node = service.report(
        name="SQLI via atomic_tests T1005",
        summary="sqlite3 users table dump captured",
        poc="atomic_tests T1005",
        vulnclass="collection",
    )
    meta = graph.get(node.node_id).meta
    assert meta["outcome_class"] == "collection"


def test_report_severity_kept_with_typed_evidence(sandbox):
    graph = loop.ExplorationGraph("tc")
    service = loop.FindingService("tc", graph, loop.ActivityLog("tc"), None)
    node = service.report(
        name="SQLI confirmed",
        summary="You have an error in your SQL syntax near ''",
        poc="curl 'http://t/?id=1'",
        vulnclass="sqli",
    )
    meta = graph.get(node.node_id).meta
    assert meta["severity"] == "high"
    assert meta["outcome_class"] == "sqli"


def test_tpd_parks_member_for_hour_scale(tmp_path, monkeypatch):
    from modules.llm_pool import HealthRegistry, PoolConfig

    monkeypatch.setenv("LAZYOWN_LLM_HEALTH_PATH", str(tmp_path / "health.json"))
    registry = HealthRegistry(PoolConfig(tpd_cooldown_sec=4 * 3600.0))
    registry.report_failure("m1", "Error code: 429 - Rate limit reached on tokens per day (TPD).")
    assert registry.healthy("m1") is False


def test_generic_429_without_tpd_wording_stays_short(tmp_path, monkeypatch):
    from modules.llm_pool import HealthRegistry, PoolConfig

    monkeypatch.setenv("LAZYOWN_LLM_HEALTH_PATH", str(tmp_path / "health.json"))
    registry = HealthRegistry(PoolConfig(tpd_cooldown_sec=4 * 3600.0, backoff_sec=(60.0, 300.0, 1800.0)))
    for _ in range(5):
        registry.report_failure("m2", "Request timed out.")
    assert registry.healthy("m2") is False
    assert registry._tpd_trip == {}


def test_tpd_breaker_persists_and_recovers_after_cooldown(tmp_path, monkeypatch):
    from modules.llm_pool import HealthRegistry, PoolConfig

    monkeypatch.setenv("LAZYOWN_LLM_HEALTH_PATH", str(tmp_path / "health.json"))
    registry = HealthRegistry(PoolConfig(tpd_cooldown_sec=0.01))
    registry.report_failure("m3", "429 tokens per day limit reached")
    assert registry.healthy("m3") is False
    time.sleep(0.05)
    assert registry.healthy("m3") is True


def test_success_clears_tpd_trip(tmp_path, monkeypatch):
    from modules.llm_pool import HealthRegistry, PoolConfig

    monkeypatch.setenv("LAZYOWN_LLM_HEALTH_PATH", str(tmp_path / "health.json"))
    registry = HealthRegistry(PoolConfig(tpd_cooldown_sec=3600.0))
    registry.report_failure("m4", "429 tokens per day")
    assert registry.healthy("m4") is False
    registry.report_success("m4")
    assert registry.healthy("m4") is True


def test_is_world_host_rejects_chain_slugs():
    assert is_world_host("gym_metasploitable_ms2_nfs_exports") is False
    assert is_world_host("t0001") is False
    assert is_world_host("172.17.0.4") is True
    assert is_world_host("target.lab.local") is True
    assert is_world_host("10.0.0.0/24") is False


def test_lenient_invocation_never_binds_chain_slug_as_target():
    from cli.apt_chain_support import resolve_invocation

    chain, target, _playbook, _disabled = resolve_invocation(
        ["gym_metasploitable_ms2_mutillidae_lfi", "gym_metasploitable_ms2_nfs_exports"],
        policy="lenient",
    )
    assert chain == "gym_metasploitable_ms2_mutillidae_lfi"
    assert target == ""


def test_lenient_invocation_binds_host_positional():
    from cli.apt_chain_support import resolve_invocation

    _chain, target, _playbook, _disabled = resolve_invocation(
        ["gym_metasploitable_ms2_mutillidae_lfi", "172.17.0.4"],
        policy="lenient",
    )
    assert target == "172.17.0.4"


def test_verb_capabilities_matches_script_wrappers():
    from modules.verb_capabilities import requires_privilege

    assert requires_privilege("modules/lazynmap.sh -t 172.17.0.2") is True
    assert requires_privilege("nmap -sT -Pn 172.17.0.2") is False


def test_step_gate_missing_input_artifact_skips():
    step = ChainStep(run="cat /tmp/never-there.bin", needs_artifacts=["/tmp/never-there.bin"])
    reason, rendered = step_gate_verdict(step, render_text, {})
    assert "missing input artefact" in reason
    assert rendered == "cat /tmp/never-there.bin"


def test_step_gate_present_artifact_runs(tmp_path):
    artifact = tmp_path / "evidence.json"
    artifact.write_text("{}", encoding="utf-8")
    step = ChainStep(run=f"cat {artifact}", needs_artifacts=[str(artifact)])
    reason, _rendered = step_gate_verdict(step, render_text, {})
    assert reason == ""


def test_chain_runner_downgrades_privileged_step(tmp_path, monkeypatch):
    import utils
    from modules.chain_registry import Chain
    from modules.chain_runner import ChainRunner

    monkeypatch.setattr(utils, "sudo_available", lambda: False)
    chain = Chain(name="downgrade_test", steps=[ChainStep(id="scan", run="modules/lazynmap.sh -t 172.17.0.2")])
    runner = ChainRunner(chain, tokens={"target": "172.17.0.2"}, executor=lambda command: "downgraded", dry_run=True)
    command, note = runner._downgrade_privileged("modules/lazynmap.sh -t 172.17.0.2")
    assert note
    assert command.startswith("nmap -Pn -sT")
    assert "-oA sessions/scan_172.17.0.2.nmap" in command
    assert "172.17.0.2" in command


def test_chain_runner_keeps_command_with_passwordless_sudo(tmp_path, monkeypatch):
    import utils
    from modules.chain_registry import Chain
    from modules.chain_runner import ChainRunner

    monkeypatch.setattr(utils, "sudo_available", lambda: True)
    chain = Chain(name="keep_test", steps=[ChainStep(id="scan", run="modules/lazynmap.sh -t 172.17.0.2")])
    runner = ChainRunner(chain, tokens={"target": "172.17.0.2"}, dry_run=True)
    command, note = runner._downgrade_privileged("modules/lazynmap.sh -t 172.17.0.2")
    assert note == ""
    assert command == "modules/lazynmap.sh -t 172.17.0.2"


def test_settlement_headers_stripped():
    reply = "**Facts Observed:**\n- vsftpd 2.3.4 on target\n**Coverage:** 40%"
    out = loop._strip_settlement_headers(reply)
    assert "Facts Observed" not in out
    assert "vsftpd 2.3.4 on target" in out
    assert "40%" in out


def test_settlement_headers_keep_labeled_content():
    reply = "Facts Observed: vsftpd 2.3.4"
    assert loop._strip_settlement_headers(reply) == "Facts Observed: vsftpd 2.3.4"


def test_surface_diff_ignores_phantom_hosts(tmp_path, monkeypatch):
    import modules.lazy_surface_diff as diff

    monkeypatch.setenv("LAZYOWN_WORLD_MODEL_PATH", "")
    world = {
        "hosts": {
            "172.17.0.4": {"ip": "172.17.0.4", "services": {}, "os_hint": "linux"},
            "gym_metasploitable_ms2_nfs_exports": {"ip": "gym_metasploitable_ms2_nfs_exports", "services": {}},
        }
    }
    snapshots = diff.current_snapshots(world)
    assert "172.17.0.4" in snapshots
    assert "gym_metasploitable_ms2_nfs_exports" not in snapshots


def test_emulation_platform_mismatch_skips(tmp_path):
    from modules.emulation_runner import EmulationReport, EmulationRunner

    runner = EmulationRunner(sessions_dir=tmp_path)

    class FakeTest:
        guid = "g"
        name = "windows only"
        platforms = ["windows"]
        command = "whoami"
        executor_name = "sh"
        input_arguments = {}

    report = EmulationReport(target="172.17.0.4", platform="linux")
    result = runner._run_test(FakeTest(), "T1059", "172.17.0.4", None, "127.0.0.1", None, False, True, report)
    assert result.status == "skipped"
    assert "platform mismatch" in result.note


def test_event_consumer_rejects_chain_slug_host(tmp_path, monkeypatch):
    import modules.event_consumers as consumers
    from modules.world_model import read_state_dict

    world_path = tmp_path / "world_model.json"
    world_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(consumers, "_WORLD_MODEL_FILE", world_path)
    consumers._update_world_model_host("gym_metasploitable_ms2_nfs_exports", "scanned")
    consumers._update_world_model_host("172.17.0.4", "scanned")
    data = read_state_dict(world_path)
    assert "gym_metasploitable_ms2_nfs_exports" not in data["hosts"]
    assert "172.17.0.4" in data["hosts"]
    assert data["hosts"]["172.17.0.4"]["provenance"]["source"] == "event_consumer"
