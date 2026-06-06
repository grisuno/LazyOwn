"""tests/test_pipeline_engine.py

Coverage for Pillar 3 (declarative pipelines):

  - TemplateResolver: dotted-path lookup, type-aware stringification,
    safe failure for missing paths, no code execution
  - ConditionEvaluator: truthy/falsy semantics for rendered templates
  - StepValidator: substring, re: prefix, empty/non_empty predicates
  - StepDerivers: per-command output parsing (ping, lazynmap, searchsploit)
  - PipelineLoader: schema validation, name traversal protection,
    file-not-found
  - PipelineEngine: sequential execution, on_success hook, condition skip,
    on_failure stop/continue, validate failure, nested pipeline call,
    cycle detection, depth limit, artifact persistence
  - mcp_pipeline_* entry points return well-formed JSON
  - Wiring: do_pipeline exists in lazyown.py, MCP exposes 4 tools,
    daemon subcommand registered
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "modules"))
sys.path.insert(0, str(REPO_ROOT / "skills"))


@pytest.fixture
def temp_lazyown(tmp_path, monkeypatch):
    """Create a self-contained LazyOwn root with pipelines/ and sessions/."""
    pipelines_dir = tmp_path / "pipelines"
    sessions_dir = tmp_path / "sessions" / "pipelines"
    pipelines_dir.mkdir(parents=True)
    sessions_dir.mkdir(parents=True)
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"rhost": "10.0.0.1", "startip": "10.0.0.0"}))

    monkeypatch.setenv("LAZYOWN_DIR", str(tmp_path))

    import importlib

    import pipeline_engine
    importlib.reload(pipeline_engine)
    pipeline_engine.PIPELINES_DIR = pipelines_dir
    pipeline_engine.RUNS_DIR = sessions_dir
    pipeline_engine.PAYLOAD_FILE = payload_file
    # Clear the cached default engine so its loader sees the temp dir.
    pipeline_engine._default_engine = None

    return {
        "root":          tmp_path,
        "pipelines_dir": pipelines_dir,
        "runs_dir":      sessions_dir,
        "payload_file":  payload_file,
        "module":        pipeline_engine,
    }


class _ScriptedRunner:
    """IStepRunner double driven by an in-memory map of cmd -> output."""

    def __init__(
        self,
        outputs: dict[str, str],
        successes: dict[str, bool] = None,
    ) -> None:
        self._outputs = outputs
        self._successes = successes or {}
        self.calls: list[tuple[str, str, str]] = []

    def run(self, command, args, target, timeout_s):
        self.calls.append((command, args, target))
        key = command
        output = self._outputs.get(key, "")
        success = self._successes.get(
            key, self._heuristic_success(output)
        )
        return output, success, ""

    @staticmethod
    def _heuristic_success(output: str) -> bool:
        if not output:
            return False
        return "fail" not in output.lower() and "error" not in output.lower()


# ---------------------------------------------------------------------------
# TemplateResolver
# ---------------------------------------------------------------------------


class TestTemplateResolver:
    def test_dotted_path_lookup(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        ctx = {"previous": {"findings": {"services": ["ssh", "http"]}}}
        r = TemplateResolver(ctx)
        assert r.render("{{ previous.findings.services }}") == "ssh http"

    def test_missing_path_renders_empty(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({"previous": {}})
        assert r.render("{{ previous.does.not.exist }}") == ""

    def test_bool_serialisation(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({"previous": {"has_exploit": True}})
        assert r.render("{{ previous.has_exploit }}") == "true"

    def test_payload_lookup(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({"payload": {"rhost": "10.10.11.5"}})
        assert r.render("{{ payload.rhost }}") == "10.10.11.5"

    def test_no_template_passes_through(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({})
        assert r.render("plain string") == "plain string"

    def test_no_code_execution(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({"previous": {}})
        # Templates that look like Python expressions render to "" — they
        # are NOT evaluated.
        assert r.render("{{ __import__('os').system('id') }}") == ""

    def test_list_index_lookup(self, temp_lazyown):
        from pipeline_engine import TemplateResolver

        r = TemplateResolver({"items": ["a", "b", "c"]})
        assert r.render("{{ items.1 }}") == "b"


# ---------------------------------------------------------------------------
# ConditionEvaluator
# ---------------------------------------------------------------------------


class TestConditionEvaluator:
    @pytest.mark.parametrize("value,expected", [
        ("true", True),
        ("1", True),
        ("ssh http", True),
        ("", False),
        ("false", False),
        ("0", False),
        ("[]", False),
        ("none", False),
    ])
    def test_truthy_table(self, temp_lazyown, value, expected):
        from pipeline_engine import ConditionEvaluator

        assert ConditionEvaluator.is_truthy(value) is expected


# ---------------------------------------------------------------------------
# StepValidator
# ---------------------------------------------------------------------------


class TestStepValidator:
    def test_substring_match(self, temp_lazyown):
        from pipeline_engine import StepValidator

        assert StepValidator.validate("ttl=64", "64 bytes ttl=64 reply")
        assert not StepValidator.validate("ttl=64", "no ttl info here")

    def test_regex_match(self, temp_lazyown):
        from pipeline_engine import StepValidator

        assert StepValidator.validate(r"re:^ttl=\d+", "ttl=64 bytes")
        assert not StepValidator.validate(r"re:^ttl=\d+", "bytes ttl=64")

    def test_empty_and_non_empty(self, temp_lazyown):
        from pipeline_engine import StepValidator

        assert StepValidator.validate("empty", "")
        assert StepValidator.validate("non_empty", "x")
        assert not StepValidator.validate("non_empty", "")

    def test_no_predicate_is_pass_through(self, temp_lazyown):
        from pipeline_engine import StepValidator

        assert StepValidator.validate("", "anything")


# ---------------------------------------------------------------------------
# StepDerivers
# ---------------------------------------------------------------------------


class TestStepDerivers:
    def test_ping_derives_ttl_and_alive(self, temp_lazyown):
        from pipeline_engine import StepDerivers

        derived = StepDerivers.derive("ping", "64 bytes ttl=64 1 received")
        assert derived["ttl"] == 64
        assert derived["alive"] is True

    def test_lazynmap_derives_services(self, temp_lazyown):
        from pipeline_engine import StepDerivers

        nmap_output = (
            "Starting Nmap\n"
            "22/tcp open ssh OpenSSH 8.0\n"
            "80/tcp open http nginx\n"
        )
        derived = StepDerivers.derive("lazynmap", nmap_output)
        assert derived["has_open_ports"] is True
        assert derived["findings"]["services"] == ["ssh", "http"]
        assert derived["findings"]["ports"] == [22, 80]

    def test_searchsploit_has_exploit(self, temp_lazyown):
        from pipeline_engine import StepDerivers

        out_match = "Found exploit/linux/ssh CVE-2024-1234"
        out_none = "No results"
        assert StepDerivers.derive("searchsploit", out_match)["has_exploit"] is True
        assert StepDerivers.derive("searchsploit", out_none)["has_exploit"] is False

    def test_unknown_command_returns_empty(self, temp_lazyown):
        from pipeline_engine import StepDerivers

        assert StepDerivers.derive("doesnotexist", "anything") == {}

    def test_register_custom_deriver(self, temp_lazyown):
        from pipeline_engine import StepDerivers

        StepDerivers.register("xyzcmd", lambda out: {"len": len(out)})
        assert StepDerivers.derive("xyzcmd", "abcd")["len"] == 4


# ---------------------------------------------------------------------------
# PipelineLoader
# ---------------------------------------------------------------------------


def _write_pipeline(pipelines_dir: Path, name: str, data: dict) -> Path:
    path = pipelines_dir / f"{name}.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


class TestPipelineLoader:
    def test_load_basic_pipeline(self, temp_lazyown):
        from pipeline_engine import PipelineLoader

        _write_pipeline(temp_lazyown["pipelines_dir"], "p1", {
            "name": "p1",
            "steps": [{"command": "ping"}],
        })
        spec = PipelineLoader(temp_lazyown["pipelines_dir"]).load("p1")
        assert spec.name == "p1"
        assert len(spec.steps) == 1
        assert spec.steps[0].command == "ping"
        assert spec.steps[0].name == "ping"

    def test_missing_pipeline_raises(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineNotFoundError

        with pytest.raises(PipelineNotFoundError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("nope")

    def test_invalid_name_rejected(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineNotFoundError

        with pytest.raises(PipelineNotFoundError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("../etc/passwd")

    def test_both_command_and_pipeline_rejected(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineSchemaError

        _write_pipeline(temp_lazyown["pipelines_dir"], "bad", {
            "steps": [{"command": "ping", "pipeline": "other"}],
        })
        with pytest.raises(PipelineSchemaError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("bad")

    def test_neither_command_nor_pipeline_rejected(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineSchemaError

        _write_pipeline(temp_lazyown["pipelines_dir"], "bad", {
            "steps": [{"args": "-x"}],
        })
        with pytest.raises(PipelineSchemaError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("bad")

    def test_empty_steps_rejected(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineSchemaError

        _write_pipeline(temp_lazyown["pipelines_dir"], "empty", {
            "name": "empty", "steps": [],
        })
        with pytest.raises(PipelineSchemaError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("empty")

    def test_invalid_on_failure_rejected(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineSchemaError

        _write_pipeline(temp_lazyown["pipelines_dir"], "bad", {
            "steps": [{"command": "ping", "on_failure": "halt"}],
        })
        with pytest.raises(PipelineSchemaError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("bad")

    def test_list_returns_sorted_names(self, temp_lazyown):
        from pipeline_engine import PipelineLoader

        _write_pipeline(temp_lazyown["pipelines_dir"], "zeta", {"steps": [{"command": "x"}]})
        _write_pipeline(temp_lazyown["pipelines_dir"], "alpha", {"steps": [{"command": "x"}]})
        names = PipelineLoader(temp_lazyown["pipelines_dir"]).list()
        assert names == sorted(names)
        assert "alpha" in names and "zeta" in names

    def test_invalid_yaml_raises_schema_error(self, temp_lazyown):
        from pipeline_engine import PipelineLoader, PipelineSchemaError

        path = temp_lazyown["pipelines_dir"] / "broken.yaml"
        path.write_text("not: yaml: [unclosed")
        with pytest.raises(PipelineSchemaError):
            PipelineLoader(temp_lazyown["pipelines_dir"]).load("broken")


# ---------------------------------------------------------------------------
# PipelineEngine — execution
# ---------------------------------------------------------------------------


@pytest.fixture
def silent_engine_kwargs(temp_lazyown):
    """Return engine constructor kwargs with a silent narrator + temp dirs."""
    from pipeline_engine import (
        INarratorAdapter,
        PipelineLoader,
        RunArtifactStore,
    )

    class _SilentNarrator(INarratorAdapter):
        def __init__(self):
            self.events: list[dict] = []

        def narrate(self, kind, target, message, payload=None, severity="info"):
            self.events.append({"kind": kind, "message": message})

    return {
        "loader":         PipelineLoader(temp_lazyown["pipelines_dir"]),
        "artifact_store": RunArtifactStore(temp_lazyown["runs_dir"]),
        "narrator":       _SilentNarrator(),
    }


class TestPipelineEngineExecution:
    def test_runs_steps_in_order_and_persists_artifacts(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "name": "p",
            "steps": [
                {"command": "ping"},
                {"command": "lazynmap"},
            ],
        })
        runner = _ScriptedRunner({
            "ping":     "1 received ttl=64",
            "lazynmap": "22/tcp open ssh",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("p", target="10.0.0.1")
        assert run.success
        assert len(run.steps) == 2
        assert [s.command for s in run.steps] == ["ping", "lazynmap"]
        assert all(s.success for s in run.steps)

        run_dir = Path(run.artifacts_dir)
        assert (run_dir / "plan.yaml").exists()
        assert (run_dir / "summary.json").exists()
        assert (run_dir / "step_000.json").exists()
        assert (run_dir / "step_001.json").exists()

    def test_validate_failure_marks_step_failed(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "ping", "validate": "ttl=64", "on_failure": "stop"},
                {"command": "lazynmap"},
            ],
        })
        runner = _ScriptedRunner({
            "ping":     "no ttl",  # validate fails
            "lazynmap": "22/tcp open",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("p", target="10.0.0.1")
        assert not run.success
        # second step must not execute
        assert len(run.steps) == 1
        assert run.steps[0].success is False
        assert "validation failed" in run.steps[0].error

    def test_condition_false_skips_step(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "searchsploit", "name": "search"},
                {"command": "lazypwn",
                 "condition": "{{ steps.search.has_exploit }}",
                 "on_failure": "continue"},
            ],
        })
        runner = _ScriptedRunner({
            "searchsploit": "No exploits found",  # has_exploit is False
            "lazypwn":      "should not run",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("p", target="10.0.0.1")
        # Second step skipped
        skipped = [s for s in run.steps if s.skipped]
        assert len(skipped) == 1
        assert skipped[0].step_name == "lazypwn"
        # The runner was never invoked for lazypwn
        invoked = [c[0] for c in runner.calls]
        assert "lazypwn" not in invoked

    def test_condition_true_runs_step(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "searchsploit", "name": "search"},
                {"command": "lazypwn",
                 "condition": "{{ steps.search.has_exploit }}"},
            ],
        })
        runner = _ScriptedRunner({
            "searchsploit": "exploit/linux/foo CVE-2024-1",
            "lazypwn":      "shell opened",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("p", target="10.0.0.1")
        invoked = [c[0] for c in runner.calls]
        assert "lazypwn" in invoked
        assert run.success

    def test_on_success_hook_runs(self, temp_lazyown, silent_engine_kwargs):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "lazynmap", "on_success": "auto_populate"},
            ],
        })
        runner = _ScriptedRunner({
            "lazynmap":      "22/tcp open ssh",
            "auto_populate": "domain: x.htb",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("p", target="10.0.0.1")
        assert any(s.step_name == "on_success:auto_populate" for s in run.steps)

    def test_on_failure_continue_keeps_going(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "searchsploit", "on_failure": "continue"},
                {"command": "lazynmap"},
            ],
        })
        runner = _ScriptedRunner({
            "searchsploit": "",  # fails
            "lazynmap":     "22/tcp open",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        engine.run("p", target="10.0.0.1")
        # Second step still ran
        invoked = [c[0] for c in runner.calls]
        assert invoked == ["searchsploit", "lazynmap"]

    def test_input_from_replaces_args(self, temp_lazyown, silent_engine_kwargs):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [
                {"command": "lazynmap"},
                {"command": "searchsploit",
                 "input_from": "{{ previous.findings.services }}"},
            ],
        })
        runner = _ScriptedRunner({
            "lazynmap":     "22/tcp open ssh\n80/tcp open http",
            "searchsploit": "ok",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        engine.run("p", target="10.0.0.1")
        # The searchsploit call must have received the resolved args
        searchsploit_call = [c for c in runner.calls if c[0] == "searchsploit"][0]
        assert "ssh" in searchsploit_call[1]
        assert "http" in searchsploit_call[1]


# ---------------------------------------------------------------------------
# Nested pipelines + cycle detection
# ---------------------------------------------------------------------------


class TestNestedPipelines:
    def test_nested_pipeline_runs_and_records_run_id(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        _write_pipeline(temp_lazyown["pipelines_dir"], "child", {
            "steps": [{"command": "ping"}],
        })
        _write_pipeline(temp_lazyown["pipelines_dir"], "parent", {
            "steps": [
                {"pipeline": "child", "name": "recon"},
                {"command": "lazynmap"},
            ],
        })
        runner = _ScriptedRunner({
            "ping":     "1 received ttl=64",
            "lazynmap": "22/tcp open ssh",
        })
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("parent", target="10.0.0.1")
        assert run.success
        recon_step = [s for s in run.steps if s.step_name == "recon"][0]
        assert recon_step.command == "pipeline:child"
        assert recon_step.success
        assert recon_step.nested_run_id  # populated
        assert run.nested_runs and recon_step.nested_run_id in run.nested_runs

    def test_cycle_is_detected(self, temp_lazyown, silent_engine_kwargs):
        from pipeline_engine import PipelineEngine

        # parent calls child, child calls parent -> cycle
        _write_pipeline(temp_lazyown["pipelines_dir"], "parent", {
            "steps": [{"pipeline": "child", "name": "into_child"}],
        })
        _write_pipeline(temp_lazyown["pipelines_dir"], "child", {
            "steps": [{"pipeline": "parent", "name": "back_to_parent"}],
        })
        runner = _ScriptedRunner({})
        engine = PipelineEngine(runner=runner, **silent_engine_kwargs)
        run = engine.run("parent", target="10.0.0.1")
        # The nested call must produce a failed step (not crash the engine).
        nested = [s for s in run.steps if s.step_name == "into_child"][0]
        assert nested.success is False
        assert "cycle" in nested.error.lower()

    def test_depth_limit_enforced(
        self, temp_lazyown, silent_engine_kwargs
    ):
        from pipeline_engine import PipelineEngine

        # Build a chain p1 -> p2 -> p3 with max_nesting=2 so the third
        # level is refused even though no cycle exists.
        _write_pipeline(temp_lazyown["pipelines_dir"], "p1", {
            "steps": [{"pipeline": "p2", "name": "to_p2"}],
        })
        _write_pipeline(temp_lazyown["pipelines_dir"], "p2", {
            "steps": [{"pipeline": "p3", "name": "to_p3"}],
        })
        _write_pipeline(temp_lazyown["pipelines_dir"], "p3", {
            "steps": [{"command": "ping"}],
        })
        runner = _ScriptedRunner({"ping": "ttl=64 received"})
        engine = PipelineEngine(
            runner=runner, max_nesting=2, **silent_engine_kwargs,
        )
        run = engine.run("p1", target="10.0.0.1")
        # The p3 invocation must have been refused
        deep_failure = any(
            "max nesting depth" in (s.error or "") for s in run.steps
        )
        nested = engine.loader.list()
        assert "p3" in nested  # sanity check
        assert deep_failure


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


class TestMcpEntryPoints:
    def test_list_returns_json(self, temp_lazyown):
        from pipeline_engine import mcp_pipeline_list

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [{"command": "ping"}],
        })
        result = json.loads(mcp_pipeline_list())
        assert result["status"] == "ok"
        assert "p" in result["pipelines"]

    def test_run_rejects_invalid_name(self, temp_lazyown):
        from pipeline_engine import mcp_pipeline_run

        result = json.loads(mcp_pipeline_run("../etc/passwd"))
        assert result["status"] == "error"

    def test_validate_returns_step_list(self, temp_lazyown):
        from pipeline_engine import mcp_pipeline_validate

        _write_pipeline(temp_lazyown["pipelines_dir"], "p", {
            "steps": [{"command": "ping"}, {"command": "lazynmap"}],
        })
        result = json.loads(mcp_pipeline_validate("p"))
        assert result["status"] == "ok"
        assert result["step_count"] == 2

    def test_validate_missing_pipeline_errors(self, temp_lazyown):
        from pipeline_engine import mcp_pipeline_validate

        result = json.loads(mcp_pipeline_validate("notfound"))
        assert result["status"] == "error"

    def test_status_returns_ok_with_no_runs(self, temp_lazyown):
        from pipeline_engine import mcp_pipeline_status

        result = json.loads(mcp_pipeline_status())
        assert result["status"] == "ok"
        assert result["runs"] == []


# ---------------------------------------------------------------------------
# Wiring smoke tests
# ---------------------------------------------------------------------------


class TestWiring:
    def test_do_pipeline_exists_in_lazyown(self):
        src = (REPO_ROOT / "lazyown.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        methods = [
            n.name for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "do_pipeline"
        ]
        assert len(methods) == 1

    def test_mcp_exposes_four_pipeline_tools(self):
        src = (REPO_ROOT / "skills" / "lazyown_mcp.py").read_text(encoding="utf-8")
        for name in (
            "lazyown_pipeline_run",
            "lazyown_pipeline_list",
            "lazyown_pipeline_validate",
            "lazyown_pipeline_status",
        ):
            assert src.count(f'"{name}"') >= 1, f"{name} missing"

    def test_daemon_has_pipeline_subcommand(self):
        from autonomous_daemon import _COMMANDS

        assert "pipeline" in _COMMANDS

    def test_pipelines_dir_exists_and_has_readme(self):
        pipelines = REPO_ROOT / "pipelines"
        assert pipelines.exists()
        assert (pipelines / "README.md").exists()
        assert (pipelines / "linux-initial-access.yaml").exists()

    def test_example_pipelines_validate(self):
        import importlib

        import pipeline_engine
        importlib.reload(pipeline_engine)
        # Re-point to the actual repo pipelines/ directory (not tmp).
        pipeline_engine.PIPELINES_DIR = REPO_ROOT / "pipelines"

        loader = pipeline_engine.PipelineLoader(REPO_ROOT / "pipelines")
        for name in ("linux-initial-access", "recon-quick", "post-exploit-loop"):
            spec = loader.load(name)
            assert spec.steps, f"{name} must declare steps"
