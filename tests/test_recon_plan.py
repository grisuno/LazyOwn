"""Spec coverage for :mod:`cli.recon_plan`.

The recon plan glues together :class:`cli.exploration.ExplorationEngine`
outputs, the phase-aware ``cli/command_index.json`` map and the current
``payload.json`` mapping. Every test below isolates one boundary of that
contract so failures map to a specific responsibility instead of the
whole pipeline. Fixtures touch only ``tmp_path``.
"""

from __future__ import annotations

import json
import textwrap
import unittest
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from cli.exploration import (
    ANY_OS,
    DiscoveredService,
    ExplorationConfig,
    ExplorationEngine,
)
from cli.recon_plan import (
    ReconPlan,
    ReconPlanConfig,
    ReconPlanItem,
    build_recon_plan,
    render_markdown,
    render_rich,
    write_plan,
)

SMB_NMAP_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<nmaprun>
  <host>
    <address addr="10.10.10.50" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="445">
        <state state="open"/>
        <service name="microsoft-ds" product="Samba" version="4.15"/>
      </port>
      <port protocol="tcp" portid="80">
        <state state="open"/>
        <service name="http"/>
      </port>
    </ports>
  </host>
</nmaprun>
"""


EMPTY_NMAP_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<nmaprun>
  <host>
    <address addr="10.10.10.50" addrtype="ipv4"/>
    <ports/>
  </host>
</nmaprun>
"""


def _seed_addon(addons_dir: Path, name: str, os_value: str, triggers: list[str]) -> None:
    addons_dir.mkdir(parents=True, exist_ok=True)
    (addons_dir / f"{name}.yaml").write_text(
        textwrap.dedent(
            f"""\
            name: {name}
            description: spec fixture
            enabled: true
            os: {os_value}
            trigger: {json.dumps(triggers)}
            tool:
              name: {name}
              repo_url: https://example.invalid/{name}.git
              install_path: external/.exploit/{name}
              execute_command: ./{name}
            category: 03. Exploitation
            """
        ),
        encoding="utf-8",
    )


def _seed_tool(
    tools_dir: Path,
    name: str,
    triggers: list[str],
    command: str,
    os_value: str = "any",
) -> None:
    tools_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "toolname": name,
        "command": command,
        "trigger": triggers,
        "active": True,
        "category": "02. Scanning & Enumeration",
        "description": f"fixture tool {name}",
        "os": os_value,
    }
    (tools_dir / f"{name}.tool").write_text(json.dumps(payload), encoding="utf-8")


def _seed_command_index(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "phase_to_commands": {
                    "enum": ["do_enum4linux", "do_gobuster", "do_ffuf"],
                    "recon": ["do_lazynmap"],
                },
                "commands": [
                    {"name": "do_enum4linux", "summary": "enumerate smb shares"},
                    {"name": "do_gobuster", "summary": "directory bruteforce"},
                    {"name": "do_ffuf", "summary": "fuzzer"},
                ],
            }
        ),
        encoding="utf-8",
    )


def _seed_engine(
    sessions: Path,
    addons: Path,
    tools: Path,
    nmap_xml: str,
    history_rows: str = "ts,tool,command\n1,lazynmap,lazynmap\n",
    current_os: str = ANY_OS,
) -> ExplorationEngine:
    sessions.mkdir(parents=True, exist_ok=True)
    (sessions / "scan_10.10.10.50.nmap.xml").write_text(nmap_xml, encoding="utf-8")
    (sessions / "LazyOwn_session_report.csv").write_text(history_rows, encoding="utf-8")
    config = ExplorationConfig(
        sessions_dir=str(sessions),
        lazyaddons_dir=str(addons),
        tools_dir=str(tools),
    )
    return ExplorationEngine(config=config, current_os=current_os)


class BuildReconPlanContractSpec(unittest.TestCase):
    """Spec 1 — :func:`build_recon_plan` honours the documented contract."""

    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.sessions = self.root / "sessions"
        self.addons = self.root / "lazyaddons"
        self.tools = self.root / "tools"
        _seed_addon(self.addons, "smbghost", "any", ["microsoft-ds"])
        _seed_addon(self.addons, "winonly", "windows", ["microsoft-ds"])
        _seed_addon(self.addons, "httpfix", "any", ["http"])
        _seed_tool(
            self.tools,
            "enum4linux",
            ["microsoft-ds", "netbios-ssn"],
            "enum4linux -a {ip} > {outputdir}/{toolname}.txt",
        )
        _seed_tool(
            self.tools,
            "gobuster",
            ["http", "https"],
            "gobuster dir -u http://{ip}/ -w wordlist.txt",
        )
        self.command_index = self.root / "cli" / "command_index.json"
        _seed_command_index(self.command_index)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _build(self, current_os: str = ANY_OS, payload: Mapping[str, Any] | None = None) -> ReconPlan:
        engine = _seed_engine(self.sessions, self.addons, self.tools, SMB_NMAP_XML, current_os=current_os)
        config = ReconPlanConfig(
            sessions_dir=str(self.sessions),
            command_index_path=str(self.command_index),
        )
        return build_recon_plan(
            target="10.10.10.50",
            engine=engine,
            payload=payload or {"rhost": "10.10.10.50"},
            config=config,
            clock=lambda: 1700000000.0,
        )

    def test_plan_includes_addons_matching_open_service(self) -> None:
        plan = self._build()
        addon_names = {item.name for item in plan.items if item.kind == "addon"}
        self.assertIn("smbghost", addon_names)
        self.assertIn("httpfix", addon_names)

    def test_plan_filters_os_incompatible_addons_on_linux(self) -> None:
        plan = self._build(current_os="linux")
        addon_names = {item.name for item in plan.items if item.kind == "addon"}
        self.assertNotIn("winonly", addon_names)

    def test_plan_includes_tools_matching_open_service(self) -> None:
        plan = self._build()
        tool_names = {item.name for item in plan.items if item.kind == "tool"}
        self.assertIn("enum4linux", tool_names)
        self.assertIn("gobuster", tool_names)

    def test_tool_preview_substitutes_payload_placeholders(self) -> None:
        plan = self._build(payload={"rhost": "10.10.10.50", "lhost": "10.10.15.1"})
        previews = [item.command_preview for item in plan.items if item.kind == "tool"]
        self.assertTrue(any("10.10.10.50" in p for p in previews))
        self.assertFalse(any("{ip}" in p for p in previews))

    def test_plan_excludes_already_executed_addons(self) -> None:
        engine = _seed_engine(
            self.sessions,
            self.addons,
            self.tools,
            SMB_NMAP_XML,
            history_rows="ts,tool,command\n1,smbghost,smbghost\n",
        )
        plan = build_recon_plan(
            target="10.10.10.50",
            engine=engine,
            payload={"rhost": "10.10.10.50"},
            config=ReconPlanConfig(
                sessions_dir=str(self.sessions),
                command_index_path=str(self.command_index),
            ),
            clock=lambda: 1700000000.0,
        )
        addon_names = {item.name for item in plan.items if item.kind == "addon"}
        self.assertNotIn("smbghost", addon_names)

    def test_plan_includes_phase_priority_command_suggestions(self) -> None:
        plan = self._build(payload={"rhost": "10.10.10.50", "phase": "enum"})
        command_names = [item.name for item in plan.items if item.kind == "command"]
        self.assertIn("enum4linux", command_names)
        self.assertIn("gobuster", command_names)

    def test_plan_skips_command_layer_when_index_missing(self) -> None:
        engine = _seed_engine(self.sessions, self.addons, self.tools, SMB_NMAP_XML)
        config = ReconPlanConfig(
            sessions_dir=str(self.sessions),
            command_index_path=str(self.root / "missing.json"),
        )
        plan = build_recon_plan(
            target="10.10.10.50",
            engine=engine,
            payload={"rhost": "10.10.10.50"},
            config=config,
            clock=lambda: 1700000000.0,
        )
        kinds = {item.kind for item in plan.items}
        self.assertNotIn("command", kinds)

    def test_plan_uses_payload_target_when_argument_missing(self) -> None:
        engine = _seed_engine(self.sessions, self.addons, self.tools, SMB_NMAP_XML)
        plan = build_recon_plan(
            target=None,
            engine=engine,
            payload={"rhost": "10.10.10.50"},
            config=ReconPlanConfig(
                sessions_dir=str(self.sessions),
                command_index_path=str(self.command_index),
            ),
            clock=lambda: 1700000000.0,
        )
        self.assertEqual(plan.target, "10.10.10.50")

    def test_empty_scan_returns_empty_plan(self) -> None:
        engine = _seed_engine(self.sessions, self.addons, self.tools, EMPTY_NMAP_XML)
        plan = build_recon_plan(
            target="10.10.10.50",
            engine=engine,
            payload={"rhost": "10.10.10.50"},
            config=ReconPlanConfig(
                sessions_dir=str(self.sessions),
                command_index_path=str(self.root / "no-index.json"),
            ),
            clock=lambda: 1700000000.0,
        )
        self.assertTrue(plan.is_empty)
        self.assertEqual(plan.services, ())


class RenderMarkdownSpec(unittest.TestCase):
    """Spec 2 — :func:`render_markdown` produces deterministic output."""

    def _plan_with_items(self) -> ReconPlan:
        return ReconPlan(
            target="10.10.10.50",
            platform="linux",
            phase="enum",
            services=(DiscoveredService(host="10.10.10.50", port=445, proto="tcp", service="microsoft-ds"),),
            items=(
                ReconPlanItem(
                    kind="tool",
                    name="enum4linux",
                    service="microsoft-ds:445/tcp",
                    trigger_match="microsoft-ds",
                    command_preview="enum4linux -a 10.10.10.50",
                    reason="tool triggers on smb",
                ),
            ),
            generated_at=1700000000.0,
        )

    def test_markdown_starts_with_target_header(self) -> None:
        body = render_markdown(self._plan_with_items())
        self.assertTrue(body.splitlines()[0].startswith("# Recon plan"))

    def test_markdown_renders_services_table(self) -> None:
        body = render_markdown(self._plan_with_items())
        self.assertIn("| service | port", body)
        self.assertIn("microsoft-ds", body)

    def test_markdown_renders_command_preview_block(self) -> None:
        body = render_markdown(self._plan_with_items())
        self.assertIn("```sh", body)
        self.assertIn("enum4linux -a 10.10.10.50", body)

    def test_markdown_handles_empty_plan(self) -> None:
        plan = ReconPlan(
            target="10.10.10.50",
            platform="any",
            phase="enum",
            services=(),
            items=(),
            generated_at=0.0,
        )
        body = render_markdown(plan)
        self.assertIn("No actionable items", body)


class WritePlanSpec(unittest.TestCase):
    """Spec 3 — :func:`write_plan` persists atomically with safe permissions."""

    def _plan(self, target: str = "10.10.10.50") -> ReconPlan:
        return ReconPlan(
            target=target,
            platform="any",
            phase="enum",
            services=(),
            items=(),
            generated_at=0.0,
        )

    def test_write_creates_expected_filename(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions = Path(tmp)
            path = write_plan(self._plan(), sessions_dir=sessions)
            self.assertEqual(path.name, "recon_plan_10.10.10.50.md")
            self.assertTrue(path.exists())

    def test_write_sanitises_target_for_filename(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_plan(self._plan(target="../etc/passwd"), sessions_dir=tmp)
            self.assertIn("recon_plan_", path.name)
            self.assertNotIn("/", path.name)

    def test_write_sets_restrictive_permissions(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_plan(self._plan(), sessions_dir=tmp)
            mode = path.stat().st_mode & 0o777
            self.assertEqual(mode & 0o077, 0)

    def test_write_overwrites_existing_plan(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions = Path(tmp)
            path = write_plan(self._plan(), sessions_dir=sessions)
            self.assertTrue(path.exists())
            path_again = write_plan(self._plan(), sessions_dir=sessions)
            self.assertEqual(path, path_again)


class RenderRichSpec(unittest.TestCase):
    """Spec 4 — :func:`render_rich` works with any duck-typed console."""

    @dataclass
    class _Recorder:
        lines: list[str]

        def print(self, line: str) -> None:
            self.lines.append(line)

    def test_renders_one_line_per_item(self) -> None:
        recorder = self._Recorder(lines=[])
        plan = ReconPlan(
            target="10.10.10.50",
            platform="any",
            phase="enum",
            services=(),
            items=(
                ReconPlanItem("tool", "enum4linux", "microsoft-ds:445/tcp", "microsoft-ds", "", "reason"),
                ReconPlanItem("addon", "smbghost", "microsoft-ds:445/tcp", "microsoft-ds", "", "reason"),
            ),
            generated_at=0.0,
        )
        render_rich(plan, recorder)
        self.assertEqual(len(recorder.lines), 3)
        self.assertIn("enum4linux", recorder.lines[1])

    def test_renders_friendly_message_when_empty(self) -> None:
        recorder = self._Recorder(lines=[])
        plan = ReconPlan(
            target="10.10.10.50",
            platform="any",
            phase="enum",
            services=(),
            items=(),
            generated_at=0.0,
        )
        render_rich(plan, recorder)
        self.assertEqual(len(recorder.lines), 1)
        self.assertIn("empty", recorder.lines[0].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
