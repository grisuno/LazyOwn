"""BDD scenarios for disposable infra, range, and executive reporting.

Each test states its Given/When/Then contract in the docstring so the
``scripts/test_bdd.sh`` gate discovers this module.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

BASE_DIR = Path(__file__).resolve().parent.parent


def test_bdd_redirector_spawn_registers_urls() -> None:
    """BDD redirector spawn workflow.

    Given a C2 port and two tunnel URLs in compose logs,
    When the operator spawns two redirectors,
    Then both URLs persist in redirector state for beacon builds.
    """
    import json

    from cli.commands.infra import InfraCommandSet

    fake_logs = "INF + https://aaa.trycloudflare.com\nINF + https://bbb.trycloudflare.com\n"

    class Completed:
        returncode = 0
        stdout = fake_logs
        stderr = ""

    import tempfile

    candidate = InfraCommandSet.__new__(InfraCommandSet)
    with tempfile.TemporaryDirectory() as tmpdir:
        isolated_state = Path(tmpdir) / "redirectors.json"
        with (
            patch("cli.commands.infra.REDIRECTOR_STATE", isolated_state),
            patch("cli.commands.infra._binary_present", return_value=True),
            patch("cli.commands.infra._run_capture", return_value=Completed()),
            patch.object(InfraCommandSet, "_c2_port", return_value=4444),
        ):
            candidate._redirector_spawn(2, 4444)

        state = json.loads(isolated_state.read_text(encoding="utf-8"))
        urls = {entry["url"] for entry in state.get("redirectors", [])}
        assert {"https://aaa.trycloudflare.com", "https://bbb.trycloudflare.com"} <= urls


def test_bdd_beacon_build_injects_fallback_urls() -> None:
    """BDD beacon fallback injection.

    Given redirector URLs in shell params,
    When the C2 builder renders the Go template context,
    Then the fallback slice reaches the beacon source.
    """
    from modules.c2_builder import _go_string_list, _resolve_fallback_urls

    urls = _resolve_fallback_urls({"c2_fallback_urls": "https://aaa.trycloudflare.com"})
    rendered = _go_string_list(urls)
    assert "https://aaa.trycloudflare.com" in rendered


def test_bdd_range_compose_topology() -> None:
    """BDD cyber range topology.

    Given the ad-mini range profile,
    When the operator inspects its compose file,
    Then DC, workstation, and traffic generator share one isolated
    network with no fixed subnet that could collide with the host.
    """
    from cli.commands.lab import RANGE_PROFILES

    compose = (BASE_DIR / "deploy" / "range" / RANGE_PROFILES["ad-mini"]["compose"]).read_text()
    assert "lazyown-range-dc" in compose
    assert "lazyown-range-ws01" in compose
    assert "lazyown-range-traffic" in compose
    assert "ipv4_address" not in compose
    assert "subnet" not in compose


def test_bdd_report_executive_summary_without_ai() -> None:
    """BDD executive reporting without AI.

    Given engagement findings and loot counters,
    When the operator generates the report without AI,
    Then the template summary states scope impact and remediation windows.
    """
    from modules.professional_report import RedTeamReportGenerator

    generator = RedTeamReportGenerator()
    data = generator.collect_data()
    data["command_history"] = generator.collect_command_history()
    data["loot_summary"] = generator.collect_loot_summary()
    generator.classify_findings(data)
    summary = generator.generate_executive_summary(data, with_ai=False)
    assert "remediat" in summary.lower()
    assert str(len(generator._findings)) in summary or "findings" in summary.lower()
