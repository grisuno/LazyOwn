"""Coverage mode: the engine exercises every Metasploitable path, not just one.

By default auto_pwn stops at the first shell (one foothold, efficient for a real
engagement). The gym exists to exercise and learn from every vector, so a
coverage run must try all ranked candidates, record a result per vector, and
keep going past a shell -- otherwise the loop only ever learns one path and the
other 40+ Metasploitable vectors rot.
"""

from __future__ import annotations

import sys
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


def _profile() -> TargetProfile:
    return TargetProfile(ip="10.0.0.2", open_ports=(21, 139, 512, 1524, 3632, 6667))


def _candidates(n: int) -> list[ExploitCandidate]:
    return [ExploitCandidate(service=f"svc{i}", product="", version="", strategy=f"ms2_{i}", confidence=0.9) for i in range(n)]


def _engine(monkeypatch, candidates, shell_at):
    eng = AutonomousExploitEngine()
    monkeypatch.setattr(eng, "profile", lambda target: _profile())
    monkeypatch.setattr(eng, "rank_exploits", lambda profile: candidates)
    monkeypatch.setattr(eng, "_apply_stealth_delay", lambda: None)
    executed: list[str] = []

    def fake_exec(candidate, profile):
        executed.append(candidate.strategy)
        got_shell = candidate.strategy in shell_at
        return ExploitResult(candidate=candidate, success=True, shell_obtained=got_shell, session_id=candidate.strategy if got_shell else "")

    monkeypatch.setattr(eng, "execute_candidate", fake_exec)
    return eng, executed


def test_default_hunt_stops_at_first_shell(monkeypatch):
    eng, executed = _engine(monkeypatch, _candidates(6), shell_at={"ms2_2"})
    results = eng.hunt("10.0.0.2", max_exploits=6)
    assert executed == ["ms2_0", "ms2_1", "ms2_2"]
    assert sum(1 for r in results if r.shell_obtained) == 1


def test_coverage_hunt_exercises_every_vector(monkeypatch):
    eng, executed = _engine(monkeypatch, _candidates(6), shell_at={"ms2_2", "ms2_5"})
    results = eng.hunt("10.0.0.2", max_exploits=6, stop_on_first_shell=False)
    assert executed == ["ms2_0", "ms2_1", "ms2_2", "ms2_3", "ms2_4", "ms2_5"]
    assert sum(1 for r in results if r.shell_obtained) == 2
    assert len(results) == 6


def test_coverage_hunt_counts_all_shells(monkeypatch):
    eng, _ = _engine(monkeypatch, _candidates(10), shell_at={"ms2_1", "ms2_4", "ms2_9"})
    results = eng.hunt("10.0.0.2", max_exploits=20, stop_on_first_shell=False)
    shells = [r.candidate.strategy for r in results if r.shell_obtained]
    assert shells == ["ms2_1", "ms2_4", "ms2_9"]


def test_atomic_specs_surface_port_based_vectors():
    """Curated bind-shell/backdoor vectors the generic DB matcher misses must
    surface by open port even when the scan mangled the service name."""
    eng = AutonomousExploitEngine()
    profile = TargetProfile(
        ip="10.0.0.2",
        open_ports=(1524, 6667, 21),
        services=(
            {"port": "1524", "name": "with", "product": "service", "version": "bindshell"},
            {"port": "6667", "name": "irc", "product": "", "version": ""},
            {"port": "21", "name": "ftp", "product": "vsftpd", "version": "vsftpd 2.3.4"},
        ),
    )
    strategies = {c.strategy for c in eng._match_atomic_specs(profile)}
    assert "ms2_ingreslock" in strategies
    assert "ms2_unrealircd_backdoor" in strategies
    assert "vsftpd_backdoor" in strategies


def test_rank_skips_noise_service_flood():
    """A tcpwrapped port carries no service signal and must not flood the
    ranking with generic exploit-DB candidates."""
    eng = AutonomousExploitEngine()
    profile = TargetProfile(
        ip="10.0.0.2",
        open_ports=(1524,),
        services=({"port": "1524", "name": "tcpwrapped", "product": "", "version": ""},),
    )
    ranked = eng.rank_exploits(profile)
    assert all(c.service != "tcpwrapped" for c in ranked)


def test_coverage_bounded_vector_does_not_stall(monkeypatch):
    """A single hanging vector must not stall a coverage run: it is bounded and
    the traversal continues to the remaining vectors. The wall-clock cap is
    the payload ``auto_pwn_vector_timeout_sec`` knob."""
    import time as _time

    from modules import autonomous_exploit_engine as mod

    eng = AutonomousExploitEngine()
    eng._payload_config = {"auto_pwn_vector_timeout_sec": 0.3}
    profile = _profile()
    cands = _candidates(4)

    def exec_maybe_hang(candidate, profile):
        if candidate.strategy == "ms2_1":
            _time.sleep(5)  # simulate a hanging vector
        return ExploitResult(candidate=candidate, success=True, shell_obtained=False)

    out = mod.AutonomousExploitEngine._bounded_execute(eng, cands[1], profile, exec_maybe_hang)
    assert out.success is False
    assert "timeout" in out.error.lower()


def test_full_auto_pwn_breaker_skips_family(monkeypatch, tmp_path):
    """Two family timeouts must skip the rest of that family, not other paths."""
    from modules import autonomous_exploit_engine as mod
    from modules.exploit_engine.outcomes import SKIP, TIMEOUT

    eng = AutonomousExploitEngine()
    eng._payload_config = {"auto_pwn_coverage_max_vectors": 6, "auto_pwn_breaker_timeouts": 2}
    eng._attempted_cves = set()
    monkeypatch.setattr(mod.AutonomousExploitEngine, "_load_payload_config", lambda self: dict(eng._payload_config))
    monkeypatch.setattr(mod, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(AutonomousExploitEngine, "get_instance", classmethod(lambda cls: eng))
    monkeypatch.setattr(eng, "profile", lambda target: _profile())
    monkeypatch.setattr(
        eng,
        "rank_exploits",
        lambda profile: [
            ExploitCandidate(service="http", product="tomcat", version="", strategy="tomcat_0", confidence=0.9, family="tomcat"),
            ExploitCandidate(service="http", product="tomcat", version="", strategy="tomcat_1", confidence=0.9, family="tomcat"),
            ExploitCandidate(service="http", product="tomcat", version="", strategy="tomcat_2", confidence=0.9, family="tomcat"),
            ExploitCandidate(service="ftp", product="vsftpd", version="", strategy="vsftpd_0", confidence=0.9, family="vsftpd"),
        ],
    )
    monkeypatch.setattr(eng, "_apply_stealth_delay", lambda: None)

    def bounded(candidate, profile, timeout=None):
        if candidate.family == "tomcat":
            return ExploitResult(candidate=candidate, success=False, outcome=TIMEOUT, timed_out=True)
        return ExploitResult(candidate=candidate, success=True, outcome="anon_access")

    monkeypatch.setattr(eng, "_bounded_execute", bounded)

    summary = mod.AutonomousExploitEngine.full_auto_pwn("10.0.0.2", cover_all=True)
    outcomes = {r["strategy"]: r["outcome"] for r in summary["exploit_results"]}
    assert outcomes["tomcat_0"] == TIMEOUT
    assert outcomes["tomcat_1"] == TIMEOUT
    assert outcomes["tomcat_2"] == SKIP
    assert outcomes["vsftpd_0"] == "anon_access"
    assert summary["circuit_open"] == ["tomcat"]
    assert summary["outcomes"] == {"timeout": 2, "skip": 1, "anon_access": 1}
    assert summary["shells_obtained"] == 0
    hb = (tmp_path / "auto_pwn_heartbeat.json").read_text()
    assert '"status": "completed"' in hb
