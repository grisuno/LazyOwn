"""Spec coverage for :mod:`cli.lazynmap_post`.

The post-scan helper composes three side effects (plan, world model,
event). Each test isolates one of them so a regression points to the
specific responsibility. Fixtures touch only ``tmp_path``.
"""

from __future__ import annotations

import json
import textwrap
import unittest
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.exploration import ANY_OS, ExplorationConfig, ExplorationEngine
from cli.lazynmap_post import PostScanConfig, PostScanResult, run_post_scan
from cli.recon_plan import ReconPlanConfig

_NMAP_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<nmaprun>
  <host>
    <address addr="10.10.10.5" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="445">
        <state state="open"/>
        <service name="microsoft-ds"/>
      </port>
    </ports>
  </host>
</nmaprun>
"""


def _seed_addon(addons: Path) -> None:
    addons.mkdir(parents=True, exist_ok=True)
    (addons / "smbghost.yaml").write_text(
        textwrap.dedent(
            """\
            name: smbghost
            description: smb fixture
            enabled: true
            os: any
            trigger: [microsoft-ds]
            tool:
              name: smbghost
              repo_url: https://example.invalid/smbghost.git
              install_path: external/.exploit/smbghost
              execute_command: ./smbghost
            category: 03. Exploitation
            """
        ),
        encoding="utf-8",
    )


def _seed_environment(tmp: Path) -> tuple[Path, Path, Path]:
    sessions = tmp / "sessions"
    addons = tmp / "lazyaddons"
    tools = tmp / "tools"
    sessions.mkdir()
    tools.mkdir()
    _seed_addon(addons)
    (sessions / "scan_10.10.10.5.nmap.xml").write_text(_NMAP_XML, encoding="utf-8")
    (sessions / "LazyOwn_session_report.csv").write_text("ts,tool,command\n1,lazynmap,lazynmap\n", encoding="utf-8")
    return sessions, addons, tools


def _make_engine(sessions: Path, addons: Path, tools: Path) -> ExplorationEngine:
    config = ExplorationConfig(
        sessions_dir=str(sessions),
        lazyaddons_dir=str(addons),
        tools_dir=str(tools),
    )
    return ExplorationEngine(config=config, current_os=ANY_OS)


@dataclass
class _ConsoleRecorder:
    lines: list[str]

    def print(self, line: str) -> None:
        self.lines.append(line)


class PostScanOutputSpec(unittest.TestCase):
    """Spec 1 — successful run writes plan, world model and event."""

    def test_writes_plan_world_model_and_event(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            cfg = PostScanConfig(sessions_dir=str(sessions))
            plan_cfg = ReconPlanConfig(
                sessions_dir=str(sessions),
                command_index_path=str(Path(tmp) / "no-index.json"),
            )
            result = run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                console=_ConsoleRecorder(lines=[]),
                config=cfg,
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=plan_cfg,
                clock=lambda: 1700000000.0,
            )
            self.assertIsInstance(result, PostScanResult)
            self.assertFalse(result.skipped)
            self.assertIsNotNone(result.plan)
            self.assertTrue((sessions / "recon_plan_10.10.10.5.md").exists())
            self.assertTrue(result.world_model_updated)
            self.assertTrue((sessions / "world_model.json").exists())
            self.assertTrue(result.event_emitted)
            self.assertTrue((sessions / "autonomous_events.jsonl").exists())

    def test_world_model_is_merged_not_overwritten(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            (sessions / "world_model.json").write_text(
                json.dumps({"campaign_id": "abc", "phase": "recon"}),
                encoding="utf-8",
            )
            cfg = PostScanConfig(sessions_dir=str(sessions))
            run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                console=None,
                config=cfg,
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            wm = json.loads((sessions / "world_model.json").read_text(encoding="utf-8"))
            self.assertEqual(wm.get("campaign_id"), "abc")
            self.assertEqual(wm.get("phase"), "enum")
            self.assertEqual(wm.get("target"), "10.10.10.5")

    def test_event_record_carries_target_and_counts(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            cfg = PostScanConfig(sessions_dir=str(sessions))
            run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                console=None,
                config=cfg,
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            events_text = (sessions / "autonomous_events.jsonl").read_text(encoding="utf-8").strip()
            record = json.loads(events_text.splitlines()[-1])
            self.assertEqual(record["type"], "lazynmap.recon_plan")
            self.assertEqual(record["payload"]["target"], "10.10.10.5")
            self.assertGreaterEqual(record["payload"]["item_count"], 1)
            self.assertGreaterEqual(record["payload"]["service_count"], 1)
            self.assertEqual(record["payload"]["phase"], "enum")

    def test_console_receives_plan_preview_lines(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            recorder = _ConsoleRecorder(lines=[])
            run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                console=recorder,
                config=PostScanConfig(sessions_dir=str(sessions)),
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            self.assertGreaterEqual(len(recorder.lines), 1)
            self.assertTrue(any("Recon plan" in line for line in recorder.lines))


class PostScanToggleSpec(unittest.TestCase):
    """Spec 2 — operator toggle short-circuits every side effect."""

    def test_disabled_payload_skips_all_writes(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            cfg = PostScanConfig(sessions_dir=str(sessions))
            result = run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5", "enable_recon_plan": False},
                console=None,
                config=cfg,
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            self.assertTrue(result.skipped)
            self.assertFalse((sessions / "recon_plan_10.10.10.5.md").exists())
            self.assertFalse((sessions / "world_model.json").exists())
            self.assertFalse((sessions / "autonomous_events.jsonl").exists())

    def test_string_falsy_toggle_is_respected(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, addons, tools = _seed_environment(Path(tmp))
            result = run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5", "enable_recon_plan": "false"},
                console=None,
                config=PostScanConfig(sessions_dir=str(sessions)),
                engine_factory=lambda: _make_engine(sessions, addons, tools),
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            self.assertTrue(result.skipped)


class PostScanResilienceSpec(unittest.TestCase):
    """Spec 3 — failures inside one branch never break the others."""

    def test_engine_failure_still_emits_event_and_updates_world_model(self) -> None:
        with TemporaryDirectory() as tmp:
            sessions, _addons, _tools = _seed_environment(Path(tmp))

            def _broken_factory() -> ExplorationEngine:
                raise RuntimeError("simulated catalog failure")

            cfg = PostScanConfig(sessions_dir=str(sessions))
            result = run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                console=_ConsoleRecorder(lines=[]),
                config=cfg,
                engine_factory=_broken_factory,
                plan_config=ReconPlanConfig(
                    sessions_dir=str(sessions),
                    command_index_path=str(Path(tmp) / "no.json"),
                ),
                clock=lambda: 1700000000.0,
            )
            self.assertFalse(result.skipped)
            self.assertIsNone(result.plan)
            self.assertTrue(result.world_model_updated)
            self.assertTrue(result.event_emitted)


if __name__ == "__main__":
    unittest.main(verbosity=2)
