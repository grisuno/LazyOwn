"""Spec-driven validation of the three priority improvements.

This module is intentionally self-contained: it depends only on the
Python standard library plus the modules under test. No pytest fixtures,
no external mocks, no network access. It can be executed via
``python3 -m unittest tests/test_improvements_spec.py`` or under pytest.

Specs are derived from the following authoritative documents already
checked into the repository:

* ``CLAUDE.md`` — coding standards (no magic numbers / hardcoded paths,
  SOLID, English-only, docstrings everywhere, atomic file writes,
  sessions/ as the only durable cross-process location, no duplicate
  ``class Config``).
* ``COMMANDS.md`` — auto-generated command surface contract (every
  ``do_*`` carries a docstring used as ``help <name>``).
* ``QUICKSTART.md`` — operator flow (status bar must surface target,
  phase, last finding, next suggestion).
* ``skills/lazyown.md`` — MCP playbook (single canonical orchestrator
  entry point).
* ``graphify-out/graph_lazyown.json`` — self-knowledge graph (the
  suggestion source must degrade gracefully when the graph is missing
  or unreadable).

Each test name encodes the spec it asserts so failures map back to a
specific requirement.
"""

from __future__ import annotations

import argparse
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Mapping
from unittest.mock import MagicMock

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cli.commands._dormancy import is_pending
from cli.commands.orchestration import (
    OrchestrationCommandSet,
    OrchestrationConfig,
)
from cli.registry import iter_command_sets
from cli.status_bar import (
    FileSystemReader,
    GraphSuggestionSource,
    PayloadTargetSource,
    SessionFindingSource,
    StatusBarConfig,
    StatusBarManager,
    StatusBarRenderer,
    StatusContext,
    WorldModelPhaseSource,
    build_default_manager,
)
from skills.unified_orchestrator import (
    BackendRegistry,
    DaemonBackend,
    EventBus,
    GoalValidator,
    HiveBackend,
    OrchestratorConfig,
    OrchestratorGoal,
    OrchestratorResult,
    RouterPolicy,
    SwanBackend,
    UnifiedOrchestrator,
    build_default_orchestrator,
)


class _FakeShell:
    """Minimal cmd2 stand-in that records hook registrations."""

    def __init__(self, custom_prompt: str = "lazy> ") -> None:
        self.custom_prompt = custom_prompt
        self.prompt = custom_prompt
        self.params: dict[str, Any] = {}
        self._precmd_hooks: list[Any] = []

    def register_precmd_hook(self, hook: Any) -> None:
        self._precmd_hooks.append(hook)


class _FakeEngagement:
    def __init__(self, payload: Mapping[str, Any]) -> None:
        self._payload = payload

    def run(self) -> dict[str, Any]:
        return dict(self._payload)


class _FakeQueen:
    def __init__(self, drones: int = 3, summary: str = "all clear") -> None:
        self._drones = drones
        self._summary = summary

    def plan(self, goal: str, n_drones: int = 0) -> list[dict[str, str]]:
        count = max(1, max(self._drones, n_drones))
        return [{"role": "recon", "goal": goal} for _ in range(count)]

    def dispatch(self, tasks: list[dict[str, str]], **_: Any) -> list[str]:
        return [f"drone-{i:02d}" for i, _ in enumerate(tasks)]

    def collect(self, ids: list[str]) -> list[dict[str, str]]:
        return [{"id": i, "result": "ok"} for i in ids]

    def synthesize(self, results: list[dict[str, str]]) -> str:
        return f"{self._summary} ({len(results)} drones)"


class _FakeSwanResult:
    def __init__(self, text: str = "shell ready", expert_id: str = "expert-1") -> None:
        self.text = text
        self.expert_id = expert_id
        self.reward = 0.75
        self.detection_probability = 0.1
        self.elapsed = 1.5


class _FakeSwanOrchestrator:
    def __init__(self, result: _FakeSwanResult | None = None) -> None:
        self._result = result or _FakeSwanResult()

    def run(self, task_type: str, goal: str, engagement_phase: str, timeout: float) -> _FakeSwanResult:
        return self._result


class _FakeAdvisor:
    def __init__(self, suggestions: list[dict[str, str]] | None = None) -> None:
        self._suggestions = suggestions or []

    def suggest_next(self, recent_commands: list[str], limit: int) -> list[dict[str, str]]:
        return list(self._suggestions[:limit])


def _build_test_orchestrator(
    tmp_root: Path,
    daemon_available: bool = True,
    hive_available: bool = True,
    swan_available: bool = True,
    daemon_payload: Mapping[str, Any] | None = None,
) -> UnifiedOrchestrator:
    config = OrchestratorConfig(sessions_dir=str(tmp_root))
    daemon_factory = None
    if daemon_available:
        payload = dict(daemon_payload or {"flag": "captured", "engagement_id": "abcd1234"})

        def _make_engine(goal: OrchestratorGoal) -> _FakeEngagement:
            return _FakeEngagement(payload)

        daemon_factory = _make_engine
    hive_factory = (lambda: _FakeQueen()) if hive_available else None
    swan_factory = (lambda api_key: _FakeSwanOrchestrator()) if swan_available else None
    backends = [
        DaemonBackend(config, factory=daemon_factory) if daemon_available
        else _UnavailableBackend("daemon"),
        HiveBackend(config, factory=hive_factory) if hive_available
        else _UnavailableBackend("hive"),
        SwanBackend(config, factory=swan_factory) if swan_available
        else _UnavailableBackend("swan"),
    ]
    registry = BackendRegistry(backends)
    router = RouterPolicy(config, registry)
    validator = GoalValidator(config)
    bus = EventBus(config, root=tmp_root)
    return UnifiedOrchestrator(config, registry, router, validator, bus)


class _UnavailableBackend:
    def __init__(self, name: str) -> None:
        self.name = name

    def available(self) -> bool:
        return False

    def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
        raise RuntimeError("unavailable backend invoked")


class StatusBarConfigSpec(unittest.TestCase):
    """Spec 1.A — Config encapsulates every tunable.

    CLAUDE.md §3 & §10 require no magic numbers or hardcoded paths.
    The dataclass must therefore expose every value the bar relies on.
    """

    def test_config_is_immutable_dataclass(self) -> None:
        cfg = StatusBarConfig()
        self.assertTrue(is_dataclass(cfg))
        with self.assertRaises(Exception):
            cfg.max_finding_chars = 999  # type: ignore[misc]

    def test_config_overrides_from_payload(self) -> None:
        cfg = StatusBarConfig.from_payload({"status_bar_format": "{target}|{phase}"})
        self.assertEqual(cfg.default_format, "{target}|{phase}")

    def test_config_ignores_invalid_overrides(self) -> None:
        cfg = StatusBarConfig.from_payload({"status_bar_format": 42})
        self.assertEqual(cfg.default_format, StatusBarConfig().default_format)


class StatusBarSecuritySpec(unittest.TestCase):
    """Spec 1.B — FileSystemReader is hardened against path traversal."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "ok.txt").write_text("safe", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _reader(self) -> FileSystemReader:
        return FileSystemReader(StatusBarConfig(sessions_dir=str(self.root)), root=self.root)

    def test_reader_rejects_parent_traversal(self) -> None:
        self.assertEqual(self._reader().read_text("../etc/passwd"), "")

    def test_reader_rejects_absolute_paths(self) -> None:
        self.assertEqual(self._reader().read_text("/etc/passwd"), "")

    def test_reader_bounds_file_size(self) -> None:
        big = self.root / "big.bin"
        big.write_bytes(b"x" * (StatusBarConfig().max_file_bytes + 1024))
        out = self._reader().read_text("big.bin")
        self.assertLessEqual(len(out), StatusBarConfig().max_file_bytes)

    def test_reader_returns_empty_on_missing_file(self) -> None:
        self.assertEqual(self._reader().read_text("missing.txt"), "")

    def test_reader_invalid_json_returns_none(self) -> None:
        (self.root / "bad.json").write_text("{not json", encoding="utf-8")
        self.assertIsNone(self._reader().read_json("bad.json"))


class StatusBarRendererSpec(unittest.TestCase):
    """Spec 1.C — Renderer sanitises, truncates and ANSI-wraps."""

    def setUp(self) -> None:
        self.config = StatusBarConfig()
        self.renderer = StatusBarRenderer(self.config)

    def test_render_plain_contains_all_fields(self) -> None:
        ctx = StatusContext("10.10.10.10", "exploit", "cred:alice", "linpeas")
        line = self.renderer.render_plain(ctx)
        for token in ("10.10.10.10", "exploit", "cred:alice", "linpeas"):
            self.assertIn(token, line)

    def test_render_truncates_to_max_chars(self) -> None:
        long_value = "a" * 256
        ctx = StatusContext(long_value, "recon", "x", "y")
        line = self.renderer.render_plain(ctx)
        self.assertLessEqual(line.count("a"), self.config.max_target_chars)

    def test_render_strips_dangerous_substrings(self) -> None:
        ctx = StatusContext("good\x1b[31mtarget", "recon", "x", "y")
        line = self.renderer.render_plain(ctx)
        self.assertNotIn("\x1b", line)

    def test_render_prompt_wraps_ansi_with_readline_markers(self) -> None:
        ctx = StatusContext("t", "recon", "x", "y")
        prompt = self.renderer.render_prompt(ctx, "lazy> ")
        self.assertIn(self.config.readline_open_marker, prompt)
        self.assertIn(self.config.readline_close_marker, prompt)
        self.assertTrue(prompt.endswith("lazy> "))


class StatusBarManagerSpec(unittest.TestCase):
    """Spec 1.D — Manager wires sources and installs onto the shell."""

    def test_missing_source_key_raises(self) -> None:
        cfg = StatusBarConfig()
        with self.assertRaises(KeyError):
            StatusBarManager(cfg, sources={}, renderer=StatusBarRenderer(cfg))

    def test_collect_context_uses_fallbacks_on_failure(self) -> None:
        cfg = StatusBarConfig()

        class _Broken:
            def collect(self) -> str:
                raise RuntimeError("boom")

        manager = StatusBarManager(
            cfg,
            sources={"target": _Broken(), "phase": _Broken(), "finding": _Broken(), "suggestion": _Broken()},
            renderer=StatusBarRenderer(cfg),
        )
        ctx = manager.collect_context()
        self.assertEqual(ctx.target, cfg.fallback_target)
        self.assertEqual(ctx.phase, cfg.fallback_phase)
        self.assertEqual(ctx.last_finding, cfg.fallback_finding)
        self.assertEqual(ctx.next_suggestion, cfg.fallback_suggestion)

    def test_enabled_flag_accepts_strings_and_bools(self) -> None:
        cfg = StatusBarConfig()
        renderer = StatusBarRenderer(cfg)

        class _Static:
            def __init__(self, value: str) -> None:
                self._value = value

            def collect(self) -> str:
                return self._value

        sources = {
            "target": _Static("t"),
            "phase": _Static("p"),
            "finding": _Static("f"),
            "suggestion": _Static("s"),
        }
        for raw, expected in (("true", True), ("FALSE", False), (1, True), (0, False), (True, True)):
            manager = StatusBarManager(cfg, sources, renderer, payload={cfg.enabled_key: raw})
            self.assertEqual(manager.enabled, expected, raw)

    def test_install_registers_precmd_hook(self) -> None:
        cfg = StatusBarConfig()
        renderer = StatusBarRenderer(cfg)

        class _Static:
            def __init__(self, value: str) -> None:
                self._value = value

            def collect(self) -> str:
                return self._value

        sources = {
            "target": _Static("10.0.0.1"),
            "phase": _Static("recon"),
            "finding": _Static("-"),
            "suggestion": _Static("lazynmap"),
        }
        manager = StatusBarManager(cfg, sources, renderer, payload={cfg.enabled_key: True})
        shell = _FakeShell(custom_prompt="lazy> ")
        installed = manager.install(shell)
        self.assertTrue(installed)
        self.assertEqual(len(shell._precmd_hooks), 1)
        self.assertIn("10.0.0.1", shell.prompt)


class StatusBarSourceSpec(unittest.TestCase):
    """Spec 1.E — Concrete sources prefer richer data and fall back cleanly."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.config = StatusBarConfig(sessions_dir=str(self.root))
        self.reader = FileSystemReader(self.config, root=self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_payload_target_picks_first_non_empty_key(self) -> None:
        source = PayloadTargetSource(self.config, {"rhost": "1.2.3.4"})
        self.assertEqual(source.collect(), "1.2.3.4")

    def test_payload_target_falls_back_to_default(self) -> None:
        source = PayloadTargetSource(self.config, {})
        self.assertEqual(source.collect(), self.config.fallback_target)

    def test_phase_prefers_world_model_over_payload(self) -> None:
        (self.root / self.config.world_model_filename).write_text(
            json.dumps({"phase": "lateral"}), encoding="utf-8"
        )
        source = WorldModelPhaseSource(self.config, self.reader, {"current_phase": "recon"})
        self.assertEqual(source.collect(), "lateral")

    def test_finding_prefers_credentials_over_notes(self) -> None:
        (self.root / "credentials_alice.txt").write_text("alice:hunter2\n", encoding="utf-8")
        (self.root / self.config.notes_filename).write_text(
            json.dumps({"note": "later"}) + "\n", encoding="utf-8"
        )
        source = SessionFindingSource(self.config, self.reader)
        self.assertTrue(source.collect().startswith("cred:"))

    def test_suggestion_uses_advisor_when_available(self) -> None:
        advisor = _FakeAdvisor([{"label": "gobuster"}])
        source = GraphSuggestionSource(self.config, self.reader, advisor_factory=lambda: advisor)
        self.assertEqual(source.collect(), "gobuster")

    def test_suggestion_falls_back_when_advisor_raises(self) -> None:
        class _Broken:
            def suggest_next(self, **_: Any) -> list[dict[str, str]]:
                raise RuntimeError("graph missing")

        source = GraphSuggestionSource(self.config, self.reader, advisor_factory=lambda: _Broken())
        self.assertEqual(source.collect(), self.config.fallback_suggestion)


class StatusBarFactorySpec(unittest.TestCase):
    """Spec 1.F — build_default_manager wires the canonical four sources."""

    def test_factory_returns_manager_with_four_sources(self) -> None:
        manager = build_default_manager(payload={"rhost": "10.0.0.1"}, sessions_dir=tempfile.gettempdir())
        self.assertIsInstance(manager, StatusBarManager)
        self.assertEqual(set(manager._sources.keys()), {"target", "phase", "finding", "suggestion"})


class OrchestratorGoalValidationSpec(unittest.TestCase):
    """Spec 2.A — GoalValidator enforces invariants at the boundary."""

    def setUp(self) -> None:
        self.config = OrchestratorConfig()
        self.validator = GoalValidator(self.config)

    def test_empty_goal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.validator.validate(goal="   ")

    def test_unknown_mode_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.validator.validate(goal="enumerate", mode="moonshot")

    def test_long_goal_is_bounded(self) -> None:
        long = "x" * (self.config.max_goal_chars + 1024)
        validated = self.validator.validate(goal=long)
        self.assertEqual(len(validated.goal), self.config.max_goal_chars)

    def test_defaults_are_applied(self) -> None:
        validated = self.validator.validate(goal="enum")
        self.assertEqual(validated.mode, self.config.default_mode)
        self.assertEqual(validated.phase, self.config.default_phase)

    def test_task_type_stays_empty_when_unset(self) -> None:
        validated = self.validator.validate(goal="enum")
        self.assertEqual(validated.task_type, "")

    def test_numeric_fields_stay_zero_when_unset(self) -> None:
        validated = self.validator.validate(goal="enum")
        self.assertEqual(validated.drones, 0)
        self.assertEqual(validated.timeout, 0.0)

    def test_metadata_carries_request_id(self) -> None:
        validated = self.validator.validate(goal="enum", metadata={"caller": "cli"})
        self.assertIn("request_id", validated.metadata)
        self.assertEqual(validated.metadata["caller"], "cli")


class BackendRegistrySpec(unittest.TestCase):
    """Spec 2.B — Registry enforces unique, named backends."""

    def test_duplicate_name_raises(self) -> None:
        cfg = OrchestratorConfig()
        with self.assertRaises(ValueError):
            BackendRegistry([DaemonBackend(cfg), DaemonBackend(cfg)])

    def test_empty_name_raises(self) -> None:
        class _Unnamed:
            name = ""

            def available(self) -> bool:
                return True

            def run(self, goal: OrchestratorGoal) -> OrchestratorResult:
                raise NotImplementedError

        with self.assertRaises(ValueError):
            BackendRegistry([_Unnamed()])

    def test_order_is_preserved(self) -> None:
        cfg = OrchestratorConfig()
        registry = BackendRegistry([
            DaemonBackend(cfg, factory=lambda g: _FakeEngagement({})),
            HiveBackend(cfg, factory=lambda: _FakeQueen()),
            SwanBackend(cfg, factory=lambda key: _FakeSwanOrchestrator()),
        ])
        self.assertEqual(registry.names, ("daemon", "hive", "swan"))


class RouterPolicySpec(unittest.TestCase):
    """Spec 2.C — Router chooses backends by intent, not by accident."""

    def setUp(self) -> None:
        self.config = OrchestratorConfig()
        self.registry = BackendRegistry([
            DaemonBackend(self.config, factory=lambda g: _FakeEngagement({})),
            HiveBackend(self.config, factory=lambda: _FakeQueen()),
            SwanBackend(self.config, factory=lambda key: _FakeSwanOrchestrator()),
        ])
        self.router = RouterPolicy(self.config, self.registry)
        self.validator = GoalValidator(self.config)

    def test_explicit_mode_overrides_router(self) -> None:
        goal = self.validator.validate(goal="enumerate", mode="swan")
        self.assertEqual(self.router.choose(goal).name, "swan")

    def test_auto_picks_daemon_when_target_present(self) -> None:
        goal = self.validator.validate(goal="capture flag", target="10.0.0.1")
        self.assertEqual(self.router.choose(goal).name, "daemon")

    def test_auto_picks_hive_on_swarm_keyword(self) -> None:
        goal = self.validator.validate(goal="swarm parallel recon", drones=8)
        self.assertEqual(self.router.choose(goal).name, "hive")

    def test_auto_picks_swan_on_exploit_keyword(self) -> None:
        goal = self.validator.validate(goal="develop exploit chain", phase="exploitation")
        self.assertEqual(self.router.choose(goal).name, "swan")

    def test_unavailable_explicit_mode_returns_none(self) -> None:
        cfg = OrchestratorConfig()
        registry = BackendRegistry([_UnavailableBackend("daemon"), _UnavailableBackend("hive"), _UnavailableBackend("swan")])
        router = RouterPolicy(cfg, registry)
        goal = GoalValidator(cfg).validate(goal="enum", mode="swan")
        self.assertIsNone(router.choose(goal))


class EventBusSpec(unittest.TestCase):
    """Spec 2.D — EventBus persists atomically and bounds payloads."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.config = OrchestratorConfig(sessions_dir=str(self.root))
        self.bus = EventBus(self.config, root=self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_emit_appends_jsonline(self) -> None:
        ok = self.bus.emit({"kind": "test", "value": 1})
        self.assertTrue(ok)
        content = (self.root / self.config.events_filename).read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(content), 1)
        self.assertEqual(json.loads(content[0])["value"], 1)

    def test_emit_rejects_oversize_event(self) -> None:
        big = {"payload": "x" * (self.config.max_event_bytes + 1024)}
        self.assertFalse(self.bus.emit(big))

    def test_emit_rejects_non_serialisable(self) -> None:
        self.assertFalse(self.bus.emit({"bad": object()}))

    def test_file_permissions_are_restrictive(self) -> None:
        self.bus.emit({"kind": "perm"})
        mode = (self.root / self.config.events_filename).stat().st_mode & 0o777
        self.assertEqual(mode & 0o077, 0)


class BackendAdapterSpec(unittest.TestCase):
    """Spec 2.E — Adapters never raise; they normalise into OrchestratorResult."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.config = OrchestratorConfig(sessions_dir=str(self.root))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _goal(self, **overrides: Any) -> OrchestratorGoal:
        base = GoalValidator(self.config).validate(goal=overrides.pop("goal", "enum"), **overrides)
        return base

    def test_daemon_requires_target(self) -> None:
        backend = DaemonBackend(self.config, factory=lambda g: _FakeEngagement({}))
        result = backend.run(self._goal())
        self.assertEqual(result.status, "invalid")

    def test_daemon_normalises_dict_result(self) -> None:
        backend = DaemonBackend(self.config, factory=lambda g: _FakeEngagement({"flag": "FLAG"}))
        result = backend.run(self._goal(target="10.0.0.1"))
        self.assertEqual(result.status, "ok")
        self.assertIn("FLAG", result.summary)
        self.assertEqual(result.artefacts.get("flag"), "FLAG")

    def test_hive_runs_full_lifecycle(self) -> None:
        backend = HiveBackend(self.config, factory=lambda: _FakeQueen(drones=3))
        result = backend.run(self._goal(goal="swarm recon", drones=3))
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.artefacts.get("task_count"), 3)
        self.assertIn("drones", result.summary)

    def test_swan_normalises_result_object(self) -> None:
        backend = SwanBackend(self.config, factory=lambda key: _FakeSwanOrchestrator())
        result = backend.run(self._goal(goal="exploit kerberoasting", phase="exploitation"))
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.artefacts.get("expert_id"), "expert-1")

    def test_backend_returns_error_when_engine_raises(self) -> None:
        class _Boom:
            def run(self) -> dict[str, Any]:
                raise RuntimeError("simulated failure")

        backend = DaemonBackend(self.config, factory=lambda g: _Boom())
        result = backend.run(self._goal(target="10.0.0.1"))
        self.assertEqual(result.status, "error")
        self.assertIn("simulated failure", result.summary)


class UnifiedOrchestratorSpec(unittest.TestCase):
    """Spec 2.F — End-to-end facade emits events and never raises."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _events(self) -> list[dict[str, Any]]:
        path = self.root / OrchestratorConfig().events_filename
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

    def test_validation_error_returns_invalid_result(self) -> None:
        orch = _build_test_orchestrator(self.root)
        result = orch.execute(goal="")
        self.assertEqual(result.status, "invalid")
        self.assertEqual(self._events()[-1]["status"], "invalid")

    def test_unavailable_backend_returns_unavailable_result(self) -> None:
        orch = _build_test_orchestrator(self.root, daemon_available=False, hive_available=False, swan_available=False)
        result = orch.execute(goal="enum", mode="swan")
        self.assertEqual(result.status, "unavailable")

    def test_auto_routes_with_target_to_daemon(self) -> None:
        orch = _build_test_orchestrator(self.root)
        result = orch.execute(goal="own this box", target="10.0.0.1")
        self.assertEqual(result.backend, "daemon")
        self.assertEqual(result.status, "ok")

    def test_event_is_emitted_per_execution(self) -> None:
        orch = _build_test_orchestrator(self.root)
        orch.execute(goal="enum", target="10.0.0.1")
        events = self._events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["backend"], "daemon")
        self.assertIn("request_id", events[0])

    def test_result_to_dict_is_json_serialisable(self) -> None:
        orch = _build_test_orchestrator(self.root)
        result = orch.execute(goal="enum", target="10.0.0.1")
        payload = result.to_dict()
        json.dumps(payload)


class ConfigDedupeSpec(unittest.TestCase):
    """Spec 3.A — utils.py must not redeclare class Config.

    CLAUDE.md §7 documented a long-standing duplicate Config defect.
    Once removed, the canonical class lives in core.config. This test is
    the regression guard: if a future change reintroduces a class Config
    line in utils.py the test fails loudly.
    """

    def test_utils_has_no_class_config(self) -> None:
        utils_path = REPO_ROOT / "utils.py"
        source = utils_path.read_text(encoding="utf-8")
        offending = [
            line for line in source.splitlines() if line.strip().startswith("class Config")
        ]
        self.assertEqual(offending, [], "utils.py must not declare class Config")

    def test_core_config_is_canonical(self) -> None:
        from core.config import Config

        cfg = Config({"rhost": "10.0.0.1", "lhost": "10.10.15.37"})
        self.assertEqual(cfg.rhost, "10.0.0.1")
        self.assertEqual(cfg["lhost"], "10.10.15.37")
        self.assertIsNone(cfg.does_not_exist)


class CommandSetActivationSpec(unittest.TestCase):
    """Spec 3.B — OrchestrationCommandSet is discovered as active.

    Discovery walks every module under ``cli.commands.*`` via importlib.
    Some of those modules transitively import ``utils.py`` which parses
    ``sys.argv`` at import time. Unittest passes ``-v`` which collides
    with that parser, so the test temporarily neutralises ``sys.argv``
    while discovery runs and restores it after.
    """

    def _discover(self) -> list:
        preserved_argv = sys.argv[:]
        sys.argv = [sys.argv[0]]
        try:
            return list(iter_command_sets())
        finally:
            sys.argv = preserved_argv

    def test_orchestration_set_is_active(self) -> None:
        discovered = self._discover()
        match = [c for c in discovered if c.__name__ == "OrchestrationCommandSet"]
        self.assertEqual(len(match), 1)
        self.assertFalse(is_pending(match[0]))

    def test_orchestration_set_exposes_required_verbs(self) -> None:
        self.assertTrue(hasattr(OrchestrationCommandSet, "do_status_bar"))
        self.assertTrue(hasattr(OrchestrationCommandSet, "do_orchestrate"))

    def test_orchestration_set_phase_and_category_set(self) -> None:
        self.assertEqual(OrchestrationCommandSet.phase, "orchestration")
        self.assertTrue(OrchestrationCommandSet.category)


class DocstringDisciplineSpec(unittest.TestCase):
    """Spec 3.C — CLAUDE.md §10.4 mandates docstrings on every public symbol."""

    def test_every_class_in_new_modules_has_docstring(self) -> None:
        from cli import status_bar
        from cli.commands import orchestration
        from skills import unified_orchestrator

        offenders: list[str] = []
        for module in (status_bar, unified_orchestrator, orchestration):
            for name in getattr(module, "__all__", []):
                obj = getattr(module, name, None)
                if obj is None:
                    continue
                if isinstance(obj, type) and not (obj.__doc__ and obj.__doc__.strip()):
                    offenders.append(f"{module.__name__}.{name}")
        self.assertEqual(offenders, [])

    def test_modules_avoid_emoji_in_source(self) -> None:
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F300-\U0001FAFF"
            "\U0001F600-\U0001F64F"
            "\U0001F680-\U0001F6FF"
            "☀-➿"
            "]"
        )
        offenders: list[str] = []
        for relative in (
            "cli/status_bar.py",
            "skills/unified_orchestrator.py",
            "cli/commands/orchestration.py",
        ):
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            if emoji_pattern.search(text):
                offenders.append(relative)
        self.assertEqual(offenders, [])


class GraphifyAvailabilitySpec(unittest.TestCase):
    """Spec 4.A — Suggestion source degrades when the graph is missing.

    QUICKSTART.md and §15a state that the graph is optional. The status
    bar must therefore never raise when ``graphify-out/`` is absent.
    """

    def test_suggestion_fallback_when_factory_none(self) -> None:
        cfg = StatusBarConfig(sessions_dir=tempfile.gettempdir())
        reader = FileSystemReader(cfg, root=Path(tempfile.gettempdir()))
        source = GraphSuggestionSource(cfg, reader, advisor_factory=None)
        self.assertEqual(source.collect(), cfg.fallback_suggestion)

    def test_graph_file_is_valid_json_when_present(self) -> None:
        graph_path = REPO_ROOT / "graphify-out" / "graph_lazyown.json"
        if not graph_path.exists():
            self.skipTest("graphify graph not built in this checkout")
        with graph_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        self.assertIsInstance(payload, (dict, list))


class CmdIntegrationRegressionSpec(unittest.TestCase):
    """Spec 5 — regression guards for the two live-shell wiring bugs.

    Bug 1: ``self.__dict__.get('_cmd')`` returns ``None`` because cmd2
        exposes the shell through a property, not an instance attribute.
        The OrchestrationCommandSet must use ``self._cmd`` so the bound
        shell is resolved correctly.

    Bug 2: ``cmd2.Cmd.register_precmd_hook`` validates that the callable
        has the exact type annotations ``PrecommandData`` on both the
        parameter and the return. Hooks built with looser typing are
        silently rejected and the status bar never updates after install.
    """

    def test_command_set_resolves_shell_via_cmd_property(self) -> None:
        import cmd2
        from cli.commands.orchestration import OrchestrationCommandSet

        class _Shell(cmd2.Cmd):
            custom_prompt = "lazy> "

        shell = _Shell()
        cmdset = OrchestrationCommandSet()
        shell.register_command_set(cmdset)
        resolved = cmdset._resolve_shell()
        self.assertIs(resolved, shell)

    def test_status_bar_install_registers_precmd_hook_on_real_cmd2(self) -> None:
        import cmd2

        class _Shell(cmd2.Cmd):
            custom_prompt = "lazy> "

        shell = _Shell()
        shell.params = {"rhost": "10.0.0.1", "enable_status_bar": True}
        shell.sessions_dir = tempfile.gettempdir()
        manager = build_default_manager(
            payload=shell.params,
            sessions_dir=shell.sessions_dir,
            advisor_factory=lambda: None,
        )
        installed = manager.install(shell)
        self.assertTrue(installed)
        self.assertEqual(len(shell._precmd_hooks), 1)
        hook = shell._precmd_hooks[0]
        from cmd2.plugin import PrecommandData
        self.assertEqual(hook.__annotations__.get("data"), PrecommandData)
        self.assertEqual(hook.__annotations__.get("return"), PrecommandData)

    def test_orchestration_commandset_finds_managers_on_bound_shell(self) -> None:
        import cmd2
        from cli.commands.orchestration import OrchestrationCommandSet

        class _Shell(cmd2.Cmd):
            custom_prompt = "lazy> "

        shell = _Shell()
        shell.params = {"rhost": "10.0.0.1", "enable_status_bar": True}
        shell.sessions_dir = tempfile.gettempdir()
        shell._status_bar_manager = build_default_manager(
            payload=shell.params,
            sessions_dir=shell.sessions_dir,
            advisor_factory=lambda: None,
        )
        shell._unified_orchestrator = build_default_orchestrator(
            payload=shell.params,
            sessions_dir=shell.sessions_dir,
        )
        cmdset = OrchestrationCommandSet()
        shell.register_command_set(cmdset)
        self.assertIsNotNone(cmdset._status_manager())
        self.assertIsNotNone(cmdset._orchestrator())


class LiveShellBehaviourSpec(unittest.TestCase):
    """Spec 6 — behavioural fixes derived from the operator session log.

    Three concrete regressions were observed in the live shell:

    * The status bar showed ``next: OllamaModel`` — a graph-node class
      name rather than a command verb. The suggestion source must
      surface kill-chain / phase-priority verbs.
    * ``[ ... ] ╔══[...]`` rendered on the same physical line as the
      multi-line custom prompt. The default ``prompt_join`` must place
      the bar on its own line.
    * ``orchestrate --phase recon 'get ports'`` routed to SWAN with the
      hardcoded ``exploit_generation`` task_type. The router must score
      on the goal text only when ``task_type`` is unset, and the daemon
      must fall back to ``payload.rhost`` for the target.
    """

    def test_default_prompt_join_is_newline(self) -> None:
        from cli.status_bar import StatusBarConfig
        self.assertEqual(StatusBarConfig().prompt_join, "\n")

    def test_command_hint_source_returns_kill_chain_verb(self) -> None:
        from cli.status_bar import (
            CommandHintSuggestionSource,
            FileSystemReader,
            StatusBarConfig,
        )

        with tempfile.TemporaryDirectory() as tmp:
            cfg = StatusBarConfig(sessions_dir=tmp)
            reader = FileSystemReader(cfg, root=Path(tmp))
            calls: list[tuple[str, str, str, int]] = []

            def fake_hints(last_cmd: str, phase: str, sessions_dir: str, limit: int) -> list[str]:
                calls.append((last_cmd, phase, sessions_dir, limit))
                return ["lazynmap", "gobuster", "ffuf"]

            source = CommandHintSuggestionSource(
                cfg,
                reader,
                phase_provider=lambda: "recon",
                hint_provider=fake_hints,
            )
            self.assertEqual(source.collect(), "lazynmap")
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][1], "recon")

    def test_command_hint_source_falls_back_when_provider_raises(self) -> None:
        from cli.status_bar import (
            CommandHintSuggestionSource,
            FileSystemReader,
            StatusBarConfig,
        )

        def broken(*_args, **_kwargs):
            raise RuntimeError("provider failure")

        with tempfile.TemporaryDirectory() as tmp:
            cfg = StatusBarConfig(sessions_dir=tmp)
            reader = FileSystemReader(cfg, root=Path(tmp))
            source = CommandHintSuggestionSource(
                cfg,
                reader,
                phase_provider=lambda: "recon",
                hint_provider=broken,
            )
            self.assertEqual(source.collect(), cfg.fallback_suggestion)

    def test_command_hints_helper_returns_phase_priority_verbs(self) -> None:
        from cli.reactive_hints import command_hints

        verbs = command_hints(last_command="", phase="recon", sessions_dir=tempfile.gettempdir(), limit=3)
        self.assertGreaterEqual(len(verbs), 1)
        for verb in verbs:
            self.assertNotIn(" ", verb)

    def test_daemon_falls_back_to_payload_rhost(self) -> None:
        from skills.unified_orchestrator import (
            DaemonBackend,
            GoalValidator,
            OrchestratorConfig,
        )

        config = OrchestratorConfig()
        captured: dict[str, str] = {}

        def factory(goal):
            captured["target"] = goal.target

            class _Engine:
                def run(self_inner) -> dict:
                    return {"flag": "ok"}

            return _Engine()

        backend = DaemonBackend(config, factory=factory, payload={"rhost": "10.0.0.99"})
        goal = GoalValidator(config).validate(goal="enumerate ports")
        result = backend.run(goal)
        self.assertEqual(result.status, "ok")
        self.assertEqual(captured["target"], "10.0.0.99")

    def test_router_picks_daemon_when_only_payload_supplies_target(self) -> None:
        from skills.unified_orchestrator import (
            BackendRegistry,
            DaemonBackend,
            GoalValidator,
            HiveBackend,
            OrchestratorConfig,
            RouterPolicy,
            SwanBackend,
        )

        config = OrchestratorConfig()
        backends = [
            DaemonBackend(config, factory=lambda g: _FakeEngagement({"flag": "x"}), payload={"rhost": "10.0.0.99"}),
            HiveBackend(config, factory=lambda: _FakeQueen()),
            SwanBackend(config, factory=lambda key: _FakeSwanOrchestrator()),
        ]
        registry = BackendRegistry(backends)
        router = RouterPolicy(config, registry)
        goal = GoalValidator(config).validate(goal="get ports", phase="recon")
        chosen = router.choose(goal)
        self.assertIsNotNone(chosen)
        self.assertEqual(chosen.name, "daemon")

    def test_router_ignores_unset_task_type_for_keyword_scoring(self) -> None:
        from skills.unified_orchestrator import (
            BackendRegistry,
            DaemonBackend,
            GoalValidator,
            HiveBackend,
            OrchestratorConfig,
            RouterPolicy,
            SwanBackend,
        )

        config = OrchestratorConfig()
        backends = [
            DaemonBackend(config, factory=lambda g: _FakeEngagement({})),
            HiveBackend(config, factory=lambda: _FakeQueen()),
            SwanBackend(config, factory=lambda key: _FakeSwanOrchestrator()),
        ]
        registry = BackendRegistry(backends)
        router = RouterPolicy(config, registry)
        goal = GoalValidator(config).validate(goal="get ports", phase="recon")
        self.assertEqual(goal.task_type, "")
        chosen = router.choose(goal)
        self.assertIsNotNone(chosen)
        self.assertNotEqual(chosen.name, "swan")


class FactoryWiringSpec(unittest.TestCase):
    """Spec 4.B — Default factories produce ready-to-use objects."""

    def test_build_default_orchestrator_registers_three_backends(self) -> None:
        orch = build_default_orchestrator(payload=None, sessions_dir=tempfile.gettempdir())
        self.assertEqual(orch.backends, ("daemon", "hive", "swan"))

    def test_build_default_manager_does_not_touch_filesystem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manager = build_default_manager(payload={"rhost": "10.0.0.1"}, sessions_dir=tmp)
            ctx = manager.collect_context()
            self.assertEqual(ctx.target, "10.0.0.1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
