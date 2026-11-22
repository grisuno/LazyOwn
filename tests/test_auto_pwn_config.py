"""auto_pwn payload configuration contract: every engine knob is editable.

The orchestrator Config tab exposes the auto_pwn_* payload knobs; the
engine and the auto_pwn command must honour them (with the historical
hardcoded values as fallbacks) so the operator tunes behaviour without
touching code.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "modules"))

from modules.autonomous_exploit_engine import (  # noqa: E402
    AutonomousExploitEngine,
    ExploitCandidate,
    ExploitResult,
    TargetProfile,
)


def _candidates(n: int) -> list[ExploitCandidate]:
    return [
        ExploitCandidate(service=f"svc{i}", product="", version="", strategy=f"ms2_{i}", confidence=0.9)
        for i in range(n)
    ]


def _engine(config: dict | None = None) -> AutonomousExploitEngine:
    eng = object.__new__(AutonomousExploitEngine)
    eng._payload_config = dict(config or {})
    eng._stealth_config = {
        "low": {"delay_min": 0.0, "delay_max": 0.5, "concurrent_limit": 0},
        "medium": {"delay_min": 2.0, "delay_max": 8.0, "concurrent_limit": 3},
        "high": {"delay_min": 10.0, "delay_max": 30.0, "concurrent_limit": 1},
        "paranoid": {"delay_min": 30.0, "delay_max": 120.0, "concurrent_limit": 1},
    }
    eng._stealth_level = "low"
    eng._results = []
    eng._strategy_stack = []
    eng._attempted_cves = set()
    eng._shelled_targets = set()
    return eng


def test_cfg_int_coerces_and_clamps():
    eng = _engine({"auto_pwn_foothold_cap": "12"})
    assert eng._cfg_int("auto_pwn_foothold_cap", 8, minimum=1) == 12
    assert eng._cfg_int("auto_pwn_foothold_cap", 8, minimum=1, maximum=5) == 5
    assert eng._cfg_int("auto_pwn_foothold_cap", 8, minimum=20, maximum=100) == 20


def test_cfg_helpers_fall_back_on_garbage():
    eng = _engine(
        {
            "auto_pwn_foothold_cap": "abc",
            "auto_pwn_vector_timeout_sec": True,
            "auto_pwn_retry_budget_sec": ["nope"],
            "auto_pwn_confidence_floor": None,
        }
    )
    assert eng._cfg_int("auto_pwn_foothold_cap", 8) == 8
    assert eng._cfg_float("auto_pwn_vector_timeout_sec", 45.0) == 45.0
    assert eng._cfg_float("auto_pwn_retry_budget_sec", 180.0) == 180.0
    assert eng._cfg_float("auto_pwn_confidence_floor", 0.65, maximum=1.0) == 0.65


def test_cfg_helpers_tolerate_uninitialised_instance():
    eng = object.__new__(AutonomousExploitEngine)
    assert eng._cfg_int("auto_pwn_foothold_cap", 8) == 8
    assert eng._cfg_float("auto_pwn_confidence_floor", 0.65) == 0.65


def test_stealth_level_defaults_from_payload(monkeypatch):
    from modules import autonomous_exploit_engine as mod

    monkeypatch.setattr(
        mod.AutonomousExploitEngine,
        "_load_payload_config",
        lambda self: {"auto_pwn_stealth": "paranoid"},
    )
    assert mod.AutonomousExploitEngine()._stealth_level == "paranoid"

    monkeypatch.setattr(
        mod.AutonomousExploitEngine,
        "_load_payload_config",
        lambda self: {"auto_pwn_stealth": "MAXIMUM"},
    )
    assert mod.AutonomousExploitEngine()._stealth_level == "low"

    monkeypatch.setattr(
        mod.AutonomousExploitEngine,
        "_load_payload_config",
        lambda self: {},
    )
    assert mod.AutonomousExploitEngine()._stealth_level == "low"


def test_bounded_execute_timeout_from_payload():
    eng = _engine({"auto_pwn_vector_timeout_sec": 0.5})
    profile = TargetProfile(ip="10.0.0.2", open_ports=(21,))

    def hang(candidate, prof):
        time.sleep(2)
        return ExploitResult(candidate=candidate, success=True)

    result = eng._bounded_execute(_candidates(1)[0], profile, hang)
    assert result.success is False
    assert "timeout" in result.error.lower()


def test_bounded_execute_timeout_falls_back_to_module_constant(monkeypatch):
    from modules import autonomous_exploit_engine as mod

    monkeypatch.setattr(mod, "_PER_VECTOR_TIMEOUT", 0.2)
    eng = _engine({})
    profile = TargetProfile(ip="10.0.0.2", open_ports=(21,))

    def hang(candidate, prof):
        time.sleep(1)
        return ExploitResult(candidate=candidate, success=True)

    result = eng._bounded_execute(_candidates(1)[0], profile, hang)
    assert result.success is False
    assert "timeout" in result.error.lower()


def _wired_engine(monkeypatch, config: dict, executed: list[str], shell_at: set[str] | None = None):
    from modules import autonomous_exploit_engine as mod

    eng = _engine(config)
    monkeypatch.setattr(mod.AutonomousExploitEngine, "_load_payload_config", lambda self: dict(config))
    monkeypatch.setattr(eng, "profile", lambda target: TargetProfile(ip="10.0.0.2", open_ports=(21,)))
    monkeypatch.setattr(eng, "scan_vulnerabilities", lambda profile: [])
    monkeypatch.setattr(eng, "rank_exploits", lambda profile: _candidates(6))
    monkeypatch.setattr(eng, "_apply_stealth_delay", lambda: None)
    shell_at = shell_at or set()

    def fake_exec(candidate, profile):
        executed.append(candidate.strategy)
        got_shell = candidate.strategy in shell_at
        return ExploitResult(candidate=candidate, success=True, shell_obtained=got_shell)

    monkeypatch.setattr(eng, "execute_candidate", fake_exec)
    monkeypatch.setattr(
        eng, "_bounded_execute", lambda candidate, profile, timeout=None: fake_exec(candidate, profile)
    )
    monkeypatch.setattr(
        AutonomousExploitEngine, "get_instance", classmethod(lambda cls: eng)
    )
    eng._attempted_cves = set()
    return eng


def test_full_auto_pwn_foothold_cap_from_payload(monkeypatch):
    from modules import autonomous_exploit_engine as mod

    executed: list[str] = []
    _wired_engine(monkeypatch, {"auto_pwn_foothold_cap": 2}, executed)
    summary = mod.AutonomousExploitEngine.full_auto_pwn("10.0.0.2")
    assert summary["error"] == ""
    assert executed == ["ms2_0", "ms2_1"]


def test_full_auto_pwn_coverage_cap_from_payload(monkeypatch):
    from modules import autonomous_exploit_engine as mod

    executed: list[str] = []
    _wired_engine(monkeypatch, {"auto_pwn_coverage_max_vectors": 3}, executed, shell_at={"ms2_0"})
    summary = mod.AutonomousExploitEngine.full_auto_pwn("10.0.0.2", cover_all=True)
    assert summary["error"] == ""
    assert executed == ["ms2_0", "ms2_1", "ms2_2"]
    assert summary["shells_obtained"] == 1


def test_hunt_cap_defaults_from_payload(monkeypatch):
    from modules import autonomous_exploit_engine as mod

    config = {"auto_pwn_foothold_cap": 2}
    executed: list[str] = []
    eng = _engine(config)
    monkeypatch.setattr(mod.AutonomousExploitEngine, "_load_payload_config", lambda self: dict(config))
    monkeypatch.setattr(eng, "profile", lambda target: TargetProfile(ip="10.0.0.2", open_ports=(21,)))
    monkeypatch.setattr(eng, "rank_exploits", lambda profile: _candidates(6))
    monkeypatch.setattr(eng, "_apply_stealth_delay", lambda: None)

    def fake_exec(candidate, profile):
        executed.append(candidate.strategy)
        return ExploitResult(candidate=candidate, success=False)

    monkeypatch.setattr(eng, "execute_candidate", fake_exec)
    eng.hunt("10.0.0.2")
    assert executed == ["ms2_0", "ms2_1"]


def test_full_auto_pwn_rereads_payload_between_runs(monkeypatch, tmp_path):
    """The singleton engine must honour payload edits saved mid-session.

    An operator raising auto_pwn_foothold_cap in the orchestrator while the
    shell runs must change the next run's cap without restarting the shell.
    """
    import json

    from modules import autonomous_exploit_engine as mod

    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"rhost": "10.0.0.9", "auto_pwn_foothold_cap": 2}))
    monkeypatch.setattr(mod, "PAYLOAD_PATH", payload_file)

    executed: list[str] = []
    eng = _engine({})
    monkeypatch.setattr(eng, "profile", lambda target: TargetProfile(ip="10.0.0.2", open_ports=(21,)))
    monkeypatch.setattr(eng, "scan_vulnerabilities", lambda profile: [])
    monkeypatch.setattr(eng, "rank_exploits", lambda profile: _candidates(6))
    monkeypatch.setattr(eng, "_apply_stealth_delay", lambda: None)
    monkeypatch.setattr(
        eng, "_bounded_execute", lambda candidate, profile: eng.execute_candidate(candidate, profile)
    )

    def fake_exec(candidate, profile):
        executed.append(candidate.strategy)
        return ExploitResult(candidate=candidate, success=True, shell_obtained=False)

    monkeypatch.setattr(eng, "execute_candidate", fake_exec)
    monkeypatch.setattr(mod.AutonomousExploitEngine, "get_instance", classmethod(lambda cls: eng))
    eng._attempted_cves = set()

    for cap, expected in ((2, ["ms2_0", "ms2_1"]), (5, ["ms2_0", "ms2_1", "ms2_2", "ms2_3", "ms2_4"])):
        payload_file.write_text(json.dumps({"rhost": "10.0.0.9", "auto_pwn_foothold_cap": cap}))
        summary = mod.AutonomousExploitEngine.full_auto_pwn("10.0.0.2")
        assert summary["error"] == ""
        assert executed == expected, f"cap {cap} must yield {expected}"
        executed.clear()


def test_load_fresh_payload_reads_disk():
    from cli.commands.pwn import load_fresh_payload

    payload = load_fresh_payload()
    assert isinstance(payload, dict)
    assert "rhost" in payload or payload == {}


def test_resolve_auto_pwn_defaults():
    from cli.commands.pwn import resolve_auto_pwn_defaults

    defaults = resolve_auto_pwn_defaults(
        {
            "auto_pwn_stealth": "HIGH",
            "auto_pwn_enable_pivot": True,
            "auto_pwn_enable_privesc": "true",
            "auto_pwn_cover_all": False,
        }
    )
    assert defaults == {
        "pivot": True,
        "privesc": True,
        "cover_all": False,
        "stealth": "high",
    }
    assert resolve_auto_pwn_defaults({"auto_pwn_stealth": "bogus"})["stealth"] == "low"
    assert resolve_auto_pwn_defaults({}) == {
        "pivot": False,
        "privesc": False,
        "cover_all": False,
        "stealth": "low",
    }


def test_schema_validates_auto_pwn_keys():
    from core.payload_schema import validate_value

    assert validate_value("auto_pwn_stealth", "medium") is None
    assert validate_value("auto_pwn_stealth", "silent") is not None
    assert validate_value("auto_pwn_foothold_cap", 3) is None
    assert validate_value("auto_pwn_coverage_max_vectors", 500) is None
    assert validate_value("auto_pwn_vector_timeout_sec", 30) is None
    assert validate_value("auto_pwn_retry_budget_sec", "600") is None
    assert validate_value("auto_pwn_confidence_floor", 0.7) is None
    assert validate_value("auto_pwn_port_confidence", "0.9") is None
    assert validate_value("auto_pwn_port_confidence", 2) is not None


def test_orchestrator_config_tab_exposes_auto_pwn_keys():
    from cli.orchestrator_assets_tabs import CONFIG_FIELDS

    keys = {spec.key for spec in CONFIG_FIELDS}
    expected = {
        "auto_pwn_stealth",
        "auto_pwn_enable_pivot",
        "auto_pwn_enable_privesc",
        "auto_pwn_cover_all",
        "auto_pwn_foothold_cap",
        "auto_pwn_coverage_max_vectors",
        "auto_pwn_vector_timeout_sec",
        "auto_pwn_retry_budget_sec",
        "auto_pwn_confidence_floor",
        "auto_pwn_port_confidence",
    }
    assert expected <= keys


def test_refresh_stale_profile_skips_rescan_when_enough_ports_answer(monkeypatch):
    from cli.commands.pwn import refresh_stale_profile
    from modules import loop_preflight

    monkeypatch.setattr(loop_preflight, "probe_tcp", lambda *a, **k: [21, 22])
    commands: list[str] = []

    def onecmd(line):
        commands.append(line)

    assert refresh_stale_profile("10.0.0.2", [21, 22, 23, 25], onecmd) is True
    assert commands == []


def test_refresh_stale_profile_rescans_when_most_ports_are_ghosts(monkeypatch, tmp_path):
    """One live port against many cached ghosts means the profile is stale."""
    import cli.commands.pwn as pwn_mod
    from modules import loop_preflight

    monkeypatch.setattr(loop_preflight, "probe_tcp", lambda *a, **k: [80])
    monkeypatch.setattr(pwn_mod, "SESSIONS_DIR", tmp_path)
    (tmp_path / "scan_10.0.0.9.nmap.xml").write_text(
        "<nmaprun><host><ports>"
        '<port protocol="tcp" portid="80"><state state="open"/>'
        '<service name="http" product="PHP" version="5.6.40"/></port>'
        "</ports></host></nmaprun>"
    )

    class _FakeWorld:
        def __init__(self):
            self.reset_calls: list[str] = []
            self.services: list[tuple] = []

        def reset_host(self, ip):
            self.reset_calls.append(ip)

        def add_service(self, ip, port, name, version, protocol):
            self.services.append((ip, port, name, version, protocol))

    fake = _FakeWorld()

    from modules import world_model as wm_mod

    monkeypatch.setattr(wm_mod, "get_world_model", lambda *a, **k: fake)
    commands: list[str] = []
    assert pwn_mod.refresh_stale_profile("10.0.0.9", [21, 22, 23, 80], commands.append) is True
    assert commands == ["lazynmap 10.0.0.9"]
    assert fake.reset_calls == ["10.0.0.9"]
    assert fake.services == [("10.0.0.9", 80, "http", "5.6.40", "tcp")]


def test_refresh_stale_profile_rebuilds_world_model_from_fresh_scan(monkeypatch, tmp_path):
    import cli.commands.pwn as pwn_mod
    from modules import loop_preflight
    from modules import world_model as wm_mod

    monkeypatch.setattr(loop_preflight, "probe_tcp", lambda *a, **k: [])
    commands: list[str] = []

    def onecmd(line):
        commands.append(line)

    (tmp_path / "scan_10.0.0.9.nmap.xml").write_text(
        "<nmaprun><host><ports>"
        '<port protocol="tcp" portid="80"><state state="open"/>'
        '<service name="http" product="PHP" version="5.6.40"/></port>'
        "</ports></host></nmaprun>"
    )

    class _FakeWorld:
        def __init__(self):
            self.reset_calls: list[str] = []
            self.services: list[tuple] = []

        def reset_host(self, ip):
            self.reset_calls.append(ip)

        def add_service(self, ip, port, name, version, protocol):
            self.services.append((ip, port, name, version, protocol))

    fake = _FakeWorld()
    monkeypatch.setattr(pwn_mod, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(wm_mod, "get_world_model", lambda *a, **k: fake)

    assert pwn_mod.refresh_stale_profile("10.0.0.9", [21], onecmd) is True
    assert commands == ["lazynmap 10.0.0.9"]
    assert fake.reset_calls == ["10.0.0.9"]
    assert fake.services == [("10.0.0.9", 80, "http", "5.6.40", "tcp")]


def test_refresh_stale_profile_fails_without_fresh_scan(monkeypatch, tmp_path):
    import cli.commands.pwn as pwn_mod
    from modules import loop_preflight

    monkeypatch.setattr(loop_preflight, "probe_tcp", lambda *a, **k: [])
    monkeypatch.setattr(pwn_mod, "SESSIONS_DIR", tmp_path)
    commands: list[str] = []
    assert pwn_mod.refresh_stale_profile("10.0.0.9", [21], commands.append) is False
