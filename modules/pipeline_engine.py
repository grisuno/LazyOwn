"""
modules/pipeline_engine.py — Declarative YAML pipelines for LazyOwn
====================================================================

Pillar 3: composition without code. Operators describe a kill-chain (or
any other ordered sequence of LazyOwn commands) as a YAML document under
``pipelines/`` and run it with ``pipeline run <name>``. Pipelines may call
other pipelines so larger playbooks compose from smaller building blocks.

The engine is intentionally minimal: it never calls ``eval`` or executes
template code. Variable interpolation is restricted to a safe dotted-path
resolver over a typed StepContext, and conditional execution is a strict
truthy check on the resolved value. Each step runs through the existing
LazyOwn command runner (the same one the autonomous daemon uses) so the
333+ commands remain the canonical implementation.

Layered architecture (SOLID):

  - PipelineLoader     : parses YAML + validates schema. No execution.
  - TemplateResolver   : safe ``{{ scope.path.to.value }}`` substitution.
  - ConditionEvaluator : truthy check on a resolved template.
  - StepValidator      : ``validate:`` predicate (substring or ``re:`` regex).
  - StepDerivers       : per-command output parsers (has_exploit, findings,
                         services, ttl, ports, ...). Pluggable registry so
                         new commands extend the engine without changes.
  - IStepRunner        : execution contract for one step.
  - LazyOwnStepRunner  : default runner wrapping the daemon command runner.
  - RunArtifactStore   : persists every run under sessions/pipelines/.
  - INarrator          : optional narrator (default: engagement_hooks).
  - PipelineEngine     : orchestrates the plan. Detects nested-pipeline
                         cycles, enforces depth limits, honours on_success
                         and on_failure semantics.

Security:
  - No template-language code execution.
  - YAML loaded with ``yaml.safe_load``.
  - Pipeline names normalised and verified against a whitelist regex so
    operators cannot escape ``pipelines/`` via traversal.
  - Artifact paths constructed with ``Path.resolve`` and a containment
    check; writes refuse paths outside the run directory.
"""

from __future__ import annotations

import datetime
import json
import logging
import os
import re
import shutil
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import yaml


_LAZYOWN_DIR = Path(os.environ.get(
    "LAZYOWN_DIR",
    str(Path(__file__).resolve().parent.parent),
))
PIPELINES_DIR = _LAZYOWN_DIR / "pipelines"
SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
RUNS_DIR = SESSIONS_DIR / "pipelines"
PAYLOAD_FILE = _LAZYOWN_DIR / "payload.json"

_VALID_PIPELINE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")
_TEMPLATE_RE = re.compile(r"\{\{\s*([^{}]+?)\s*\}\}")
_STEP_TIMEOUT_DEFAULT_S = 120
_DEFAULT_MAX_NESTING = 4

_log = logging.getLogger("pipeline_engine")
_IO_LOCK = threading.Lock()


# ─────────────────────────────────────────────────────────────────────────────
# Errors
# ─────────────────────────────────────────────────────────────────────────────


class PipelineError(Exception):
    """Base error class for pipeline engine failures."""


class PipelineSchemaError(PipelineError):
    """YAML structure does not match the documented schema."""


class PipelineNotFoundError(PipelineError):
    """Requested pipeline name does not resolve to a YAML file."""


class PipelineCycleError(PipelineError):
    """Nested pipeline call would form an execution cycle."""


# ─────────────────────────────────────────────────────────────────────────────
# Value objects
# ─────────────────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class PipelineStep:
    """One declared step inside a pipeline spec.

    Attributes:
        index: Position in the plan (0-based).
        name: Step identifier used for the steps.<name> scope. Defaults
              to the command/pipeline name when not specified.
        command: LazyOwn shell command to execute. Mutually exclusive
                 with pipeline.
        pipeline: Nested pipeline to invoke. Mutually exclusive with
                  command.
        args: Optional argument string appended after the command.
        input_from: Template resolved to the args (overrides args when
                    truthy after resolution).
        validate: Optional ``validate:`` predicate.
        condition: Optional ``condition:`` template. Falsy ->
                   step is skipped.
        on_success: Optional follow-up command executed only when this
                    step succeeded. The hook is itself a LazyOwn command
                    name with no args.
        on_failure: One of stop|continue|skip. Defaults to stop.
        timeout_s: Per-step timeout.
        with_inputs: Free-form dict of step-level template values
                     accessible via ``inputs.X`` inside the same step.
    """

    index: int
    name: str
    command: str = ""
    pipeline: str = ""
    args: str = ""
    input_from: str = ""
    validate: str = ""
    condition: str = ""
    on_success: str = ""
    on_failure: str = "stop"
    timeout_s: int = _STEP_TIMEOUT_DEFAULT_S
    with_inputs: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PipelineSpec:
    """A loaded, schema-validated pipeline document."""

    name: str
    description: str
    target: str
    steps: Tuple[PipelineStep, ...]
    source_path: Path


@dataclass
class StepResult:
    """Outcome of executing a single PipelineStep."""

    step_index: int
    step_name: str
    command: str
    args: str
    started_ts: str
    finished_ts: str
    output: str = ""
    success: bool = False
    skipped: bool = False
    skipped_reason: str = ""
    error: str = ""
    derived: Dict[str, Any] = field(default_factory=dict)
    nested_run_id: str = ""

    def to_context(self) -> Dict[str, Any]:
        """Render the step result as a dict for template lookups."""
        merged: Dict[str, Any] = {
            "command":   self.command,
            "args":      self.args,
            "output":    self.output,
            "success":   self.success,
            "skipped":   self.skipped,
            "started":   self.started_ts,
            "finished":  self.finished_ts,
        }
        # Derived fields are flattened so {{ previous.has_exploit }} works.
        for key, value in (self.derived or {}).items():
            if key not in merged:
                merged[key] = value
        return merged


@dataclass
class PipelineRun:
    """Aggregate result returned by PipelineEngine.run."""

    run_id: str
    pipeline: str
    target: str
    started_ts: str
    finished_ts: str
    success: bool
    steps: List[StepResult] = field(default_factory=list)
    nested_runs: List[str] = field(default_factory=list)
    error: str = ""
    artifacts_dir: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-friendly representation of the full run."""
        return {
            "run_id":        self.run_id,
            "pipeline":      self.pipeline,
            "target":        self.target,
            "started_ts":    self.started_ts,
            "finished_ts":   self.finished_ts,
            "success":       self.success,
            "error":         self.error,
            "artifacts_dir": self.artifacts_dir,
            "nested_runs":   list(self.nested_runs),
            "steps":         [asdict(s) for s in self.steps],
        }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _new_run_id() -> str:
    return uuid.uuid4().hex[:10]


def _is_valid_pipeline_name(name: str) -> bool:
    if not isinstance(name, str):
        return False
    return bool(_VALID_PIPELINE_NAME_RE.match(name))


def _load_payload() -> Dict[str, Any]:
    try:
        return json.loads(PAYLOAD_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# Template resolver — safe dotted-path substitution, no eval
# ─────────────────────────────────────────────────────────────────────────────


class TemplateResolver:
    """Resolves ``{{ scope.path.to.value }}`` against a context dict.

    Supported lookups:
      ``previous.<field>`` — most recent non-skipped step result.
      ``steps.<name>.<field>`` — explicit named step lookup.
      ``payload.<key>`` — value from payload.json (read at call time).
      ``inputs.<key>`` — step-level ``with_inputs`` values.
      ``findings.<key>`` — aggregated derived values across the run.

    Unknown paths resolve to empty string; the engine never raises on a
    bad template. Lists are stringified with ``" ".join`` so they slot
    cleanly into command-line argument strings.
    """

    def __init__(self, context: Dict[str, Any]) -> None:
        self._context = context

    def render(self, template: str) -> str:
        if not template or "{{" not in template:
            return template

        def _replace(match: "re.Match[str]") -> str:
            path = match.group(1).strip()
            value = self.resolve(path)
            return self._stringify(value)

        return _TEMPLATE_RE.sub(_replace, template)

    def resolve(self, dotted_path: str) -> Any:
        """Return the value at dotted_path or None when not found."""
        if not dotted_path:
            return None
        parts = [p for p in dotted_path.split(".") if p]
        if not parts:
            return None
        node: Any = self._context
        for part in parts:
            if isinstance(node, dict) and part in node:
                node = node[part]
            elif isinstance(node, dict) and part.isdigit():
                idx = int(part)
                values = list(node.values())
                node = values[idx] if 0 <= idx < len(values) else None
            elif isinstance(node, list) and part.isdigit():
                idx = int(part)
                node = node[idx] if 0 <= idx < len(node) else None
            else:
                return None
            if node is None:
                return None
        return node

    @staticmethod
    def _stringify(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (list, tuple, set)):
            return " ".join(str(v) for v in value)
        if isinstance(value, dict):
            return json.dumps(value, default=str)
        return str(value)


class ConditionEvaluator:
    """Truthy check on a resolved template expression."""

    @staticmethod
    def is_truthy(rendered: str) -> bool:
        if rendered is None:
            return False
        text = rendered.strip().lower()
        if not text:
            return False
        if text in ("false", "0", "no", "off", "none", "null", "[]", "{}"):
            return False
        return True


class StepValidator:
    """Implements the ``validate:`` predicate for one step.

    Forms:
      ``ttl=64``       → output must contain the substring "ttl=64".
      ``re:^ttl=\\d+`` → output must match the trailing Python regex.
      ``empty``        → output trimmed must be empty.
      ``non_empty``    → output trimmed must be non-empty.
    """

    @staticmethod
    def validate(predicate: str, output: str) -> bool:
        if not predicate:
            return True
        predicate = predicate.strip()
        text = output or ""
        if predicate.startswith("re:"):
            try:
                pattern = re.compile(predicate[3:].strip())
            except re.error:
                return False
            return bool(pattern.search(text))
        if predicate == "empty":
            return not text.strip()
        if predicate == "non_empty":
            return bool(text.strip())
        return predicate in text


# ─────────────────────────────────────────────────────────────────────────────
# Step derivers — extract structured fields from raw command output
# ─────────────────────────────────────────────────────────────────────────────


class StepDerivers:
    """Per-command output parsers producing structured derived fields.

    Each deriver returns a dict of additional keys merged into
    ``StepResult.derived``. The set of derivers is intentionally small
    and uses defensive parsing — a deriver never raises and always
    returns a dict.

    Extension: register a new deriver via ``StepDerivers.register``.
    """

    _registry: Dict[str, Callable[[str], Dict[str, Any]]] = {}

    @classmethod
    def register(
        cls, command: str, deriver: Callable[[str], Dict[str, Any]]
    ) -> None:
        """Bind a deriver to a top-level command name (case-insensitive)."""
        if not isinstance(command, str) or not command:
            return
        cls._registry[command.lower().strip()] = deriver

    @classmethod
    def derive(cls, command: str, output: str) -> Dict[str, Any]:
        """Run the registered deriver for command on output, defensive."""
        if not command:
            return {}
        cmd_name = command.strip().split()[0].lower() if command.strip() else ""
        deriver = cls._registry.get(cmd_name)
        if deriver is None:
            return {}
        try:
            result = deriver(output or "")
            return result if isinstance(result, dict) else {}
        except Exception as exc:
            _log.debug("deriver %s failed: %s", cmd_name, exc)
            return {}


def _derive_ping(output: str) -> Dict[str, Any]:
    """Extract ttl, alive flag from ping output."""
    text = output or ""
    ttl_match = re.search(r"ttl=(\d+)", text, re.IGNORECASE)
    received = re.search(r"(\d+)\s+received", text, re.IGNORECASE)
    return {
        "ttl":      int(ttl_match.group(1)) if ttl_match else None,
        "alive":    bool(ttl_match) or (received and int(received.group(1)) > 0),
        "findings": {
            "ttl":   int(ttl_match.group(1)) if ttl_match else None,
            "alive": bool(ttl_match),
        },
    }


def _derive_lazynmap(output: str) -> Dict[str, Any]:
    """Extract open ports and service names from nmap output."""
    text = output or ""
    ports: List[int] = []
    services: List[str] = []
    for match in re.finditer(
        r"^(\d+)/(tcp|udp)\s+open\s+(\S+)", text, re.MULTILINE,
    ):
        try:
            ports.append(int(match.group(1)))
        except ValueError:
            continue
        services.append(match.group(3))
    has_open = bool(ports)
    return {
        "has_open_ports": has_open,
        "open_ports_count": len(ports),
        "findings": {
            "ports":    ports,
            "services": services,
        },
    }


def _derive_searchsploit(output: str) -> Dict[str, Any]:
    """Detect whether searchsploit returned an exploit candidate.

    Looks for explicit exploit identifiers (CVE-YYYY-N or an
    ``exploit/<category>`` path) rather than any occurrence of the
    word "exploit", so phrasing like "No exploits found" correctly
    resolves to ``has_exploit=False``.
    """
    text = output or ""
    if re.search(r"\bno\b[^.\n]*\bexploits?\s+found\b", text, re.I):
        has_exploit = False
    else:
        has_exploit = bool(re.search(r"cve-\d{4}-\d+|exploit/\w", text, re.I))
    return {
        "has_exploit": has_exploit,
        "findings": {"exploits_present": has_exploit},
    }


def _derive_auto_populate(output: str) -> Dict[str, Any]:
    """Auto-populate signals: domain discovered, services injected."""
    text = output or ""
    return {
        "discovered_domain": bool(re.search(r"domain\s*[:=]", text, re.I)),
        "findings": {"populated": True},
    }


def _derive_facts_show(output: str) -> Dict[str, Any]:
    """facts_show emits 'found' lines per fact."""
    text = output or ""
    found = bool(re.search(r"\bfound\b|fact:", text, re.I))
    return {
        "has_facts": found,
        "findings": {"facts_present": found},
    }


# Bind the built-ins at import time. Operators can register additional
# derivers from their own modules by importing the engine and calling
# StepDerivers.register.
StepDerivers.register("ping", _derive_ping)
StepDerivers.register("lazynmap", _derive_lazynmap)
StepDerivers.register("rustscan", _derive_lazynmap)
StepDerivers.register("masscan", _derive_lazynmap)
StepDerivers.register("nmap", _derive_lazynmap)
StepDerivers.register("searchsploit", _derive_searchsploit)
StepDerivers.register("auto_populate", _derive_auto_populate)
StepDerivers.register("facts_show", _derive_facts_show)


# ─────────────────────────────────────────────────────────────────────────────
# Step runner — wraps the existing LazyOwn command runner
# ─────────────────────────────────────────────────────────────────────────────


class IStepRunner(ABC):
    """Execution contract for one resolved step."""

    @abstractmethod
    def run(
        self, command: str, args: str, target: str, timeout_s: int,
    ) -> Tuple[str, bool, str]:
        """Execute one command. Return (output, success, error_text)."""


class LazyOwnStepRunner(IStepRunner):
    """Default runner reusing the autonomous-daemon command runner factory.

    Each invocation prefixes the command with an ``assign rhost <target>``
    line so steps that read payload.json[rhost] always see the pipeline's
    target value, mirroring the autonomous daemon and EngageOrchestrator
    contract.
    """

    def __init__(self, runner: Any = None) -> None:
        if runner is None:
            try:
                from autonomous_daemon import _build_default_runner
                runner = _build_default_runner()
            except Exception as exc:
                raise PipelineError(
                    f"could not build default LazyOwn runner: {exc}"
                )
        self._runner = runner

    def run(
        self, command: str, args: str, target: str, timeout_s: int,
    ) -> Tuple[str, bool, str]:
        line = command if not args else f"{command} {args}"
        prelude = f"assign rhost {target}\n" if target else ""
        try:
            output = self._runner.run(prelude + line, timeout=timeout_s)
        except Exception as exc:
            return "", False, str(exc)
        success = _heuristic_success(line, output)
        return output, success, ""


def _heuristic_success(command: str, output: str) -> bool:
    if not output:
        return False
    low = output.lower()
    failure_markers = (
        "error", "failed", "no such", "command not found",
        "traceback", "refused", "timed out", "timeout",
    )
    success_markers = (
        "found", "success", "open", "hash", "discovered",
        "credential", "uid=", "started", "listening", "ttl=", "received",
    )
    if any(m in low for m in success_markers):
        return True
    if any(m in low for m in failure_markers):
        return False
    return len(output.strip()) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Loader — YAML + schema validation
# ─────────────────────────────────────────────────────────────────────────────


class PipelineLoader:
    """Loads pipeline YAML files into :class:`PipelineSpec` objects.

    SOLID:
      - SRP: parses and validates; never executes.
      - LSP: any custom YAML-source backend can subclass and override
        ``_read``.
      - Security: yaml.safe_load only; pipeline name validated.
    """

    SUPPORTED_EXTENSIONS = (".yaml", ".yml")

    def __init__(self, pipelines_dir: Optional[Path] = None) -> None:
        self._dir = pipelines_dir or PIPELINES_DIR

    @property
    def pipelines_dir(self) -> Path:
        return self._dir

    def list(self) -> List[str]:
        """Return every pipeline name discoverable in pipelines_dir."""
        if not self._dir.exists():
            return []
        out: List[str] = []
        for entry in sorted(self._dir.iterdir()):
            if entry.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue
            name = entry.stem
            if _is_valid_pipeline_name(name):
                out.append(name)
        return out

    def resolve_path(self, name: str) -> Path:
        """Return the absolute path to the YAML file for the given name."""
        if not _is_valid_pipeline_name(name):
            raise PipelineNotFoundError(f"invalid pipeline name: {name!r}")
        base = self._dir.resolve()
        for ext in self.SUPPORTED_EXTENSIONS:
            candidate = (self._dir / f"{name}{ext}").resolve()
            try:
                candidate.relative_to(base)
            except ValueError:
                raise PipelineNotFoundError(
                    f"pipeline path escapes pipelines dir: {name}"
                )
            if candidate.exists():
                return candidate
        raise PipelineNotFoundError(
            f"pipeline {name!r} not found in {self._dir}"
        )

    def _read(self, path: Path) -> Dict[str, Any]:
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            raise PipelineSchemaError(f"invalid YAML in {path.name}: {exc}")
        if not isinstance(data, dict):
            raise PipelineSchemaError(
                f"{path.name}: top-level document must be a mapping"
            )
        return data

    def load(self, name: str) -> PipelineSpec:
        """Parse the YAML file for name and return a validated spec."""
        path = self.resolve_path(name)
        raw = self._read(path)
        return self._validate(raw, name=name, source=path)

    def _validate(
        self, raw: Dict[str, Any], name: str, source: Path,
    ) -> PipelineSpec:
        steps_raw = raw.get("steps", [])
        if not isinstance(steps_raw, list) or not steps_raw:
            raise PipelineSchemaError(f"{name}: steps must be a non-empty list")

        steps: List[PipelineStep] = []
        used_names: set = set()
        for i, item in enumerate(steps_raw):
            if not isinstance(item, dict):
                raise PipelineSchemaError(
                    f"{name}: step #{i} must be a mapping"
                )
            command = str(item.get("command", "") or "").strip()
            pipeline = str(item.get("pipeline", "") or "").strip()
            if command and pipeline:
                raise PipelineSchemaError(
                    f"{name}: step #{i} may not specify both command and pipeline"
                )
            if not command and not pipeline:
                raise PipelineSchemaError(
                    f"{name}: step #{i} requires command or pipeline"
                )
            step_name = str(item.get("name", "") or "").strip()
            if not step_name:
                step_name = (command or pipeline).split()[0]
            base_name = step_name
            disambig = 2
            while step_name in used_names:
                step_name = f"{base_name}_{disambig}"
                disambig += 1
            used_names.add(step_name)
            on_failure = str(item.get("on_failure", "stop") or "stop").lower()
            if on_failure not in ("stop", "continue", "skip"):
                raise PipelineSchemaError(
                    f"{name}: step #{i} on_failure must be stop|continue|skip"
                )
            timeout_value = item.get("timeout_s", _STEP_TIMEOUT_DEFAULT_S)
            try:
                timeout_s = max(1, int(timeout_value))
            except (TypeError, ValueError):
                raise PipelineSchemaError(
                    f"{name}: step #{i} timeout_s must be an integer"
                )
            with_inputs = item.get("with_inputs", {}) or {}
            if not isinstance(with_inputs, dict):
                raise PipelineSchemaError(
                    f"{name}: step #{i} with_inputs must be a mapping"
                )
            steps.append(PipelineStep(
                index=i,
                name=step_name,
                command=command,
                pipeline=pipeline,
                args=str(item.get("args", "") or ""),
                input_from=str(item.get("input_from", "") or ""),
                validate=str(item.get("validate", "") or ""),
                condition=str(item.get("condition", "") or ""),
                on_success=str(item.get("on_success", "") or ""),
                on_failure=on_failure,
                timeout_s=timeout_s,
                with_inputs=dict(with_inputs),
            ))

        declared_name = str(raw.get("name", "") or name).strip()
        if declared_name != name:
            # Allow drift between file name and declared name as long as
            # the declared name is itself safe; the loader keys on the
            # file name. The mismatch is surfaced as info to the operator
            # via the spec.name field, which is the declared value.
            if not _is_valid_pipeline_name(declared_name):
                raise PipelineSchemaError(
                    f"{name}: declared name {declared_name!r} is not safe"
                )
        return PipelineSpec(
            name=declared_name,
            description=str(raw.get("description", "") or ""),
            target=str(raw.get("target", "") or ""),
            steps=tuple(steps),
            source_path=source,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Artifact store
# ─────────────────────────────────────────────────────────────────────────────


class RunArtifactStore:
    """Persists pipeline runs under sessions/pipelines/<pipeline>__<runid>/.

    Writes:
      - plan.yaml      : the frozen spec used by the run
      - step_<n>.json  : one record per executed step
      - summary.json   : aggregate PipelineRun
    """

    def __init__(self, runs_dir: Optional[Path] = None) -> None:
        self._runs_dir = (runs_dir or RUNS_DIR).resolve()

    @property
    def runs_dir(self) -> Path:
        return self._runs_dir

    def open_run(self, pipeline_name: str, run_id: str) -> Path:
        """Create and return the directory for this run."""
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", pipeline_name)[:80] or "pipeline"
        safe_runid = re.sub(r"[^A-Za-z0-9._-]+", "_", run_id)[:32] or "run"
        run_dir = (self._runs_dir / f"{safe_name}__{safe_runid}").resolve()
        try:
            run_dir.relative_to(self._runs_dir)
        except ValueError:
            raise PipelineError(f"refused run dir outside runs_dir: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def write_plan(self, run_dir: Path, spec: PipelineSpec) -> None:
        try:
            plan_path = (run_dir / "plan.yaml").resolve()
            plan_path.relative_to(run_dir.resolve())
        except ValueError:
            return
        try:
            shutil.copyfile(str(spec.source_path), str(plan_path))
        except Exception:
            try:
                plan_path.write_text(
                    yaml.safe_dump({"name": spec.name, "steps": []}, sort_keys=False),
                    encoding="utf-8",
                )
            except Exception:
                pass

    def write_step(self, run_dir: Path, result: StepResult) -> None:
        try:
            step_path = (run_dir / f"step_{result.step_index:03d}.json").resolve()
            step_path.relative_to(run_dir.resolve())
        except ValueError:
            return
        try:
            step_path.write_text(
                json.dumps(asdict(result), indent=2, default=str, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    def write_summary(self, run_dir: Path, run: PipelineRun) -> None:
        try:
            summary_path = (run_dir / "summary.json").resolve()
            summary_path.relative_to(run_dir.resolve())
        except ValueError:
            return
        try:
            summary_path.write_text(
                json.dumps(run.to_dict(), indent=2, default=str, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Narrator adapter — wraps EngagementNarrator if available
# ─────────────────────────────────────────────────────────────────────────────


class INarratorAdapter(ABC):
    """Optional narration interface used by the engine."""

    @abstractmethod
    def narrate(
        self,
        kind: str,
        target: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> None:
        """Emit one narration event."""


class _SilentNarrator(INarratorAdapter):
    def narrate(self, *args, **kwargs) -> None:
        return None


class EngagementNarratorAdapter(INarratorAdapter):
    """Bridges to modules.engagement_hooks.EngagementNarrator when present."""

    def __init__(self, narrator: Any = None) -> None:
        if narrator is None:
            try:
                from engagement_hooks import get_default_narrator
                narrator = get_default_narrator()
            except Exception:
                narrator = None
        self._narrator = narrator

    def narrate(
        self,
        kind: str,
        target: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> None:
        if self._narrator is None:
            return
        try:
            self._narrator.narrate(
                kind=kind,
                target=target,
                message=message,
                payload=payload or {},
                severity=severity,
            )
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────────────────────────────────────


class PipelineEngine:
    """Executes a PipelineSpec against the LazyOwn runtime.

    Construction:

        engine = PipelineEngine()              # production defaults
        engine = PipelineEngine(runner=mock,   # test injection
                                narrator=...,
                                artifact_store=...,
                                loader=...)

    Execution:

        run = engine.run("linux-initial-access", target="10.10.11.5")

    Nested pipelines reuse the same engine instance, threading the
    nesting stack through ``run`` to detect cycles.
    """

    def __init__(
        self,
        runner: Optional[IStepRunner] = None,
        loader: Optional[PipelineLoader] = None,
        artifact_store: Optional[RunArtifactStore] = None,
        narrator: Optional[INarratorAdapter] = None,
        max_nesting: int = _DEFAULT_MAX_NESTING,
    ) -> None:
        self._runner = runner or LazyOwnStepRunner()
        self._loader = loader or PipelineLoader()
        self._store = artifact_store or RunArtifactStore()
        self._narrator = narrator or EngagementNarratorAdapter()
        self._max_nesting = max(1, int(max_nesting))

    @property
    def loader(self) -> PipelineLoader:
        return self._loader

    def validate(self, name: str) -> PipelineSpec:
        """Load and validate without executing. Raises on schema errors."""
        return self._loader.load(name)

    def run(
        self,
        name: str,
        target: str = "",
        nesting_stack: Optional[Tuple[str, ...]] = None,
    ) -> PipelineRun:
        """Execute the pipeline. Returns a fully-populated PipelineRun."""
        stack = tuple(nesting_stack or ())
        if name in stack:
            raise PipelineCycleError(
                f"nested pipeline cycle detected: {' -> '.join(stack + (name,))}"
            )
        if len(stack) >= self._max_nesting:
            raise PipelineError(
                f"max nesting depth {self._max_nesting} exceeded at {name}"
            )

        spec = self._loader.load(name)
        effective_target = target or spec.target or _load_payload().get("rhost", "")

        run_id = _new_run_id()
        run_dir = self._store.open_run(spec.name, run_id)
        self._store.write_plan(run_dir, spec)

        run = PipelineRun(
            run_id=run_id,
            pipeline=spec.name,
            target=effective_target,
            started_ts=_now_iso(),
            finished_ts="",
            success=True,
            artifacts_dir=str(run_dir),
        )

        self._narrator.narrate(
            kind="PIPELINE_START",
            target=effective_target,
            message=f"pipeline {spec.name} run={run_id} steps={len(spec.steps)}",
            payload={
                "run_id":   run_id,
                "pipeline": spec.name,
                "nesting":  list(stack),
            },
        )

        step_results: Dict[str, StepResult] = {}
        derived_findings: Dict[str, Any] = {}

        try:
            for step in spec.steps:
                ctx = self._build_context(
                    spec=spec,
                    target=effective_target,
                    step_results=step_results,
                    derived_findings=derived_findings,
                    current_step=step,
                )
                resolver = TemplateResolver(ctx)

                if step.condition:
                    rendered = resolver.render(step.condition)
                    if not ConditionEvaluator.is_truthy(rendered):
                        result = self._make_skipped(
                            step, reason=f"condition false: {step.condition}",
                        )
                        run.steps.append(result)
                        step_results[step.name] = result
                        self._store.write_step(run_dir, result)
                        self._narrate_step(result, effective_target)
                        continue

                if step.pipeline:
                    result = self._run_nested(
                        step=step,
                        resolver=resolver,
                        target=effective_target,
                        stack=stack + (spec.name,),
                        run=run,
                    )
                else:
                    result = self._run_command(
                        step=step,
                        resolver=resolver,
                        target=effective_target,
                    )

                run.steps.append(result)
                step_results[step.name] = result
                self._merge_findings(derived_findings, result)
                self._store.write_step(run_dir, result)
                self._narrate_step(result, effective_target)

                if not result.success and not result.skipped:
                    if step.on_failure == "stop":
                        run.success = False
                        detail = result.error or "see step output"
                        run.error = (
                            f"step {step.name} failed: {detail}"
                        )
                        break
                    if step.on_failure == "skip":
                        continue

                if result.success and step.on_success and not result.skipped:
                    hook = self._run_hook(
                        step.on_success, effective_target, step.timeout_s,
                    )
                    run.steps.append(hook)
                    self._store.write_step(run_dir, hook)
                    self._narrate_step(hook, effective_target)
        except PipelineError as exc:
            run.success = False
            run.error = str(exc)
        finally:
            run.finished_ts = _now_iso()
            self._store.write_summary(run_dir, run)
            self._narrator.narrate(
                kind="PIPELINE_DONE",
                target=effective_target,
                message=(
                    f"pipeline {spec.name} run={run_id} success={run.success} "
                    f"steps={len(run.steps)}"
                ),
                payload={
                    "run_id":  run_id,
                    "success": run.success,
                    "error":   run.error,
                },
                severity="info" if run.success else "warning",
            )
        return run

    # ── Step execution helpers ────────────────────────────────────────────

    def _run_command(
        self,
        step: PipelineStep,
        resolver: TemplateResolver,
        target: str,
    ) -> StepResult:
        resolved_args = step.args
        if step.input_from:
            resolved_args = resolver.render(step.input_from)
        elif step.args:
            resolved_args = resolver.render(step.args)

        started = _now_iso()
        self._narrator.narrate(
            kind="PIPELINE_STEP_START",
            target=target,
            message=f"step {step.name} -> {step.command} {resolved_args}".strip(),
            payload={"step": step.name, "command": step.command, "args": resolved_args},
        )

        output, success, error = self._runner.run(
            command=step.command,
            args=resolved_args,
            target=target,
            timeout_s=step.timeout_s,
        )

        if step.validate:
            valid = StepValidator.validate(step.validate, output)
            if not valid:
                success = False
                error = error or f"validation failed: {step.validate}"

        derived = StepDerivers.derive(step.command, output)

        return StepResult(
            step_index=step.index,
            step_name=step.name,
            command=step.command,
            args=resolved_args,
            started_ts=started,
            finished_ts=_now_iso(),
            output=output,
            success=success,
            skipped=False,
            error=error,
            derived=derived,
        )

    def _run_nested(
        self,
        step: PipelineStep,
        resolver: TemplateResolver,
        target: str,
        stack: Tuple[str, ...],
        run: PipelineRun,
    ) -> StepResult:
        started = _now_iso()
        self._narrator.narrate(
            kind="PIPELINE_NESTED_START",
            target=target,
            message=f"nested pipeline {step.pipeline} from step {step.name}",
            payload={"pipeline": step.pipeline, "stack": list(stack)},
        )
        try:
            nested_run = self.run(step.pipeline, target=target, nesting_stack=stack)
        except PipelineError as exc:
            return StepResult(
                step_index=step.index,
                step_name=step.name,
                command=f"pipeline:{step.pipeline}",
                args="",
                started_ts=started,
                finished_ts=_now_iso(),
                output="",
                success=False,
                skipped=False,
                error=str(exc),
            )
        run.nested_runs.append(nested_run.run_id)
        derived = {
            "nested_pipeline": step.pipeline,
            "nested_run_id":   nested_run.run_id,
            "nested_success":  nested_run.success,
            "nested_steps":    len(nested_run.steps),
        }
        return StepResult(
            step_index=step.index,
            step_name=step.name,
            command=f"pipeline:{step.pipeline}",
            args="",
            started_ts=started,
            finished_ts=_now_iso(),
            output=json.dumps({"nested_run_id": nested_run.run_id}),
            success=nested_run.success,
            skipped=False,
            error=nested_run.error,
            derived=derived,
            nested_run_id=nested_run.run_id,
        )

    def _run_hook(
        self, hook_command: str, target: str, timeout_s: int,
    ) -> StepResult:
        started = _now_iso()
        output, success, error = self._runner.run(
            command=hook_command,
            args="",
            target=target,
            timeout_s=timeout_s,
        )
        return StepResult(
            step_index=-1,
            step_name=f"on_success:{hook_command}",
            command=hook_command,
            args="",
            started_ts=started,
            finished_ts=_now_iso(),
            output=output,
            success=success,
            skipped=False,
            error=error,
            derived=StepDerivers.derive(hook_command, output),
        )

    @staticmethod
    def _make_skipped(step: PipelineStep, reason: str) -> StepResult:
        now = _now_iso()
        return StepResult(
            step_index=step.index,
            step_name=step.name,
            command=step.command or f"pipeline:{step.pipeline}",
            args=step.args,
            started_ts=now,
            finished_ts=now,
            output="",
            success=True,
            skipped=True,
            skipped_reason=reason,
        )

    def _build_context(
        self,
        spec: PipelineSpec,
        target: str,
        step_results: Dict[str, StepResult],
        derived_findings: Dict[str, Any],
        current_step: PipelineStep,
    ) -> Dict[str, Any]:
        previous_ctx: Dict[str, Any] = {}
        if step_results:
            latest_name = next(reversed(step_results))
            previous_ctx = step_results[latest_name].to_context()
        return {
            "previous": previous_ctx,
            "steps":    {n: r.to_context() for n, r in step_results.items()},
            "payload":  _load_payload(),
            "inputs":   dict(current_step.with_inputs),
            "findings": dict(derived_findings),
            "pipeline": {
                "name":   spec.name,
                "target": target,
            },
        }

    @staticmethod
    def _merge_findings(
        derived_findings: Dict[str, Any], result: StepResult,
    ) -> None:
        derived = result.derived or {}
        more = derived.get("findings", {})
        if isinstance(more, dict):
            for key, value in more.items():
                derived_findings[key] = value

    def _narrate_step(self, result: StepResult, target: str) -> None:
        if result.skipped:
            self._narrator.narrate(
                kind="PIPELINE_STEP_SKIPPED",
                target=target,
                message=f"step {result.step_name} skipped: {result.skipped_reason}",
                payload={"step": result.step_name, "reason": result.skipped_reason},
            )
            return
        if result.success:
            self._narrator.narrate(
                kind="PIPELINE_STEP_DONE",
                target=target,
                message=f"step {result.step_name} succeeded",
                payload={
                    "step":    result.step_name,
                    "command": result.command,
                    "derived": result.derived,
                },
            )
        else:
            self._narrator.narrate(
                kind="PIPELINE_STEP_FAILED",
                target=target,
                message=f"step {result.step_name} failed: {result.error or 'see output'}",
                payload={
                    "step":    result.step_name,
                    "command": result.command,
                    "error":   result.error,
                    "tail":    (result.output or "")[-200:],
                },
                severity="warning",
            )


# ─────────────────────────────────────────────────────────────────────────────
# Public entry points (used by CLI / MCP / daemon subcommand)
# ─────────────────────────────────────────────────────────────────────────────


_default_engine_lock = threading.Lock()
_default_engine: Optional[PipelineEngine] = None


def get_default_engine() -> PipelineEngine:
    """Process-wide default engine for production callers."""
    global _default_engine
    with _default_engine_lock:
        if _default_engine is None:
            _default_engine = PipelineEngine()
        return _default_engine


def mcp_pipeline_run(
    name: str, target: str = "", background: bool = False,
) -> str:
    """Public MCP / CLI entry: run a pipeline.

    Returns a JSON string with either the full PipelineRun dict (when
    ``background=False``) or an immediate ``{status: started, run_id}``
    response (when ``background=True``).
    """
    if not _is_valid_pipeline_name(name):
        return json.dumps({"status": "error", "message": f"invalid pipeline name: {name!r}"})

    if not background:
        try:
            engine = get_default_engine()
            run = engine.run(name=name, target=target)
            return json.dumps({"status": "ok", "run": run.to_dict()}, indent=2, default=str)
        except PipelineError as exc:
            return json.dumps({"status": "error", "message": str(exc)})

    run_id = _new_run_id()

    def _worker() -> None:
        try:
            engine = get_default_engine()
            engine.run(name=name, target=target)
        except Exception as exc:
            _log.error("pipeline background run failed: %s", exc)

    thread = threading.Thread(
        target=_worker, name=f"pipeline-{run_id}", daemon=True,
    )
    thread.start()
    return json.dumps({
        "status":   "started",
        "run_id":   run_id,
        "pipeline": name,
        "message": (
            "Pipeline started in background. "
            "Poll progress with lazyown_pipeline_status."
        ),
    }, indent=2)


def mcp_pipeline_list() -> str:
    """Return the list of available pipelines under pipelines/."""
    try:
        names = PipelineLoader().list()
        return json.dumps({
            "status":    "ok",
            "count":     len(names),
            "pipelines": names,
            "dir":       str(PIPELINES_DIR),
        }, indent=2)
    except Exception as exc:
        return json.dumps({"status": "error", "message": str(exc)})


def mcp_pipeline_validate(name: str) -> str:
    """Validate a pipeline's YAML schema without executing it."""
    try:
        spec = PipelineLoader().load(name)
    except PipelineError as exc:
        return json.dumps({"status": "error", "message": str(exc)})
    return json.dumps({
        "status":      "ok",
        "name":        spec.name,
        "description": spec.description,
        "target":      spec.target,
        "step_count":  len(spec.steps),
        "steps":       [
            {
                "index":      s.index,
                "name":       s.name,
                "command":    s.command,
                "pipeline":   s.pipeline,
                "condition":  s.condition,
                "on_failure": s.on_failure,
            }
            for s in spec.steps
        ],
    }, indent=2)


def mcp_pipeline_status(last_n: int = 5) -> str:
    """Return the N most recent pipeline runs and their summaries."""
    if not RUNS_DIR.exists():
        return json.dumps({"status": "ok", "runs": []})
    entries = sorted(
        (p for p in RUNS_DIR.iterdir() if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[: max(1, int(last_n))]
    out: List[Dict[str, Any]] = []
    for entry in entries:
        summary_path = entry / "summary.json"
        record: Dict[str, Any] = {"dir": str(entry), "summary": None}
        if summary_path.exists():
            try:
                record["summary"] = json.loads(summary_path.read_text(encoding="utf-8"))
            except Exception:
                record["summary"] = None
        out.append(record)
    return json.dumps({"status": "ok", "runs": out}, indent=2, default=str)


def cmd_pipeline(action: str, name: str = "", target: str = "", background: bool = False) -> None:
    """CLI helper bound to the ``pipeline`` daemon subcommand."""
    if action == "list":
        print(mcp_pipeline_list())
    elif action == "validate":
        print(mcp_pipeline_validate(name))
    elif action == "status":
        print(mcp_pipeline_status())
    elif action == "run":
        print(mcp_pipeline_run(name, target=target, background=background))
    else:
        print(json.dumps({"status": "error", "message": f"unknown action: {action}"}))


__all__ = [
    "PipelineError",
    "PipelineSchemaError",
    "PipelineNotFoundError",
    "PipelineCycleError",
    "PipelineStep",
    "PipelineSpec",
    "StepResult",
    "PipelineRun",
    "TemplateResolver",
    "ConditionEvaluator",
    "StepValidator",
    "StepDerivers",
    "IStepRunner",
    "LazyOwnStepRunner",
    "PipelineLoader",
    "RunArtifactStore",
    "INarratorAdapter",
    "EngagementNarratorAdapter",
    "PipelineEngine",
    "get_default_engine",
    "mcp_pipeline_run",
    "mcp_pipeline_list",
    "mcp_pipeline_validate",
    "mcp_pipeline_status",
    "cmd_pipeline",
    "PIPELINES_DIR",
    "RUNS_DIR",
]
