"""Single execution engine for YAML orchestration chains.

``chain_registry`` resolves and validates; this module executes. It owns
step conditions, timeouts, retries, error policy, output capture and the
structured result every caller (CLI, loop, MCP) consumes. It never
retries a successful step, never hides a failure unless the YAML asked
for it, and never writes to the graph directly: sink tags travel in the
result so the outcome bus can fan them out.
"""

from __future__ import annotations

import concurrent.futures as futures
import glob
import os
import re
import shlex
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from modules.chain_registry import Chain, ChainStep, evaluate_when

_TOKEN_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_SHELL_META = re.compile(r"[;&|<>`$]")
_MAX_CAPTURE_CHARS = 2000
_DEFAULT_TIMEOUT = 300.0
_MAX_RETRIES = 5


@dataclass
class StepOutcome:
    """One executed or skipped step."""

    id: str = ""
    run: str = ""
    phase: str = ""
    status: str = "pending"
    output: str = ""
    reason: str = ""
    attempts: int = 0
    captured: str = ""
    artifacts: list[str] = field(default_factory=list)
    sinks: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def ok(self) -> bool:
        """Return True for success and dry-run steps."""
        return self.status in ("ok", "dry-run", "skipped")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "id": self.id,
            "run": self.run,
            "phase": self.phase,
            "status": self.status,
            "output": self.output,
            "reason": self.reason,
            "attempts": self.attempts,
            "captured": bool(self.captured),
            "artifacts": list(self.artifacts),
            "sinks": list(self.sinks),
            "duration_ms": round(self.duration_ms, 2),
        }


@dataclass
class ChainRunResult:
    """Structured result of one chain execution."""

    name: str = ""
    target: str = ""
    ok: bool = True
    aborted: bool = False
    reason: str = ""
    steps: list[StepOutcome] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    started_at: float = 0.0
    finished_at: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "name": self.name,
            "target": self.target,
            "ok": self.ok,
            "aborted": self.aborted,
            "reason": self.reason,
            "steps": [step.to_dict() for step in self.steps],
            "variables": dict(self.variables),
            "artifacts": list(self.artifacts),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": round(max(0.0, self.finished_at - self.started_at) * 1000, 2),
        }


def render_text(template: str, variables: dict[str, str]) -> str:
    """Substitute single-brace tokens in one pass."""
    text = str(template or "")
    for key, value in variables.items():
        text = text.replace("{" + key + "}", str(value))
    return text


class ChainRunner:
    """Execute one chain with per-step policy and structured outcomes."""

    def __init__(
        self,
        chain: Chain,
        tokens: dict[str, str] | None = None,
        shell: Any = None,
        executor: Callable[[str], str] | None = None,
        default_timeout: float = _DEFAULT_TIMEOUT,
        dry_run: bool = False,
        on_step: Callable[[StepOutcome], None] | None = None,
        retry_backoff: float = 0.5,
    ) -> None:
        """Bind the chain, the execution primitive and operator switches."""
        self.chain = chain
        self.tokens = {str(key): str(value) for key, value in (tokens or {}).items()}
        self.shell = shell
        self.executor = executor
        self.default_timeout = max(1.0, float(default_timeout or _DEFAULT_TIMEOUT))
        self.dry_run = bool(dry_run)
        self.on_step = on_step
        self.retry_backoff = max(0.0, float(retry_backoff))

    def run(self) -> ChainRunResult:
        """Execute the chain in order and return every step outcome."""
        started = time.time()
        variables = {**self.chain.defaults, **self.chain.vars, **self.tokens}
        result = ChainRunResult(
            name=self.chain.name,
            target=str(self.tokens.get("target", "") or ""),
            started_at=started,
        )
        captured_keys: set[str] = set()
        for step in self.chain.steps:
            outcome = self._run_step(step, variables, captured_keys)
            result.steps.append(outcome)
            for artifact in outcome.artifacts:
                if artifact and artifact not in result.artifacts:
                    result.artifacts.append(artifact)
            if outcome.captured:
                variables[step.capture] = outcome.captured
                captured_keys.add(step.capture)
            if self.on_step is not None:
                try:
                    self.on_step(outcome)
                except Exception:
                    pass
            if not outcome.ok and not step.continue_on_error:
                result.ok = False
                result.aborted = True
                result.reason = f"{outcome.id}: {outcome.reason or 'failed'}"
                break
        result.ok = all(step.ok for step in result.steps) and not result.aborted
        result.variables = dict(variables)
        result.finished_at = time.time()
        return result

    def _render_command(self, template: str, variables: dict[str, str], captured_keys: set[str]) -> str:
        """Render a command, quoting values produced by earlier captures.

        Captured output is untrusted (banners, HTTP bodies, tool output).
        Raw shell steps receive it single-quoted so shell metacharacters
        cannot escape into the operator host. cmd2 verbs keep the raw
        string because the verb owns its own argument handling.
        """
        text = str(template or "")
        quote = not self._is_verb(text)
        for key, value in variables.items():
            replacement = shlex.quote(str(value)) if quote and key in captured_keys else str(value)
            text = text.replace("{" + key + "}", replacement)
        return text

    def _run_step(
        self, step: ChainStep, variables: dict[str, str], captured_keys: set[str] | None = None
    ) -> StepOutcome:
        """Resolve and run one step according to its policy."""
        captured = captured_keys or set()
        rendered = self._render_command(step.run, variables, captured)
        outcome = StepOutcome(
            id=step.identifier,
            run=rendered,
            phase=step.phase,
            artifacts=list(step.artifacts),
            sinks=list(step.sinks),
        )
        if step.when and not evaluate_when(step.when, variables):
            outcome.status = "skipped"
            outcome.reason = "when false"
            return outcome
        skip_path = render_text(step.skip_if_exists, variables) if step.skip_if_exists else ""
        if skip_path and os.path.exists(skip_path):
            outcome.status = "skipped"
            outcome.reason = f"exists: {skip_path}"
            return outcome
        if step.resolve_newest_glob and step.resolve_newest_as:
            matches = sorted(glob.glob(render_text(step.resolve_newest_glob, variables)), key=os.path.getmtime)
            if not matches:
                outcome.status = "skipped"
                outcome.reason = "no newest match"
                return outcome
            variables[step.resolve_newest_as] = os.path.abspath(matches[-1])
            rendered = self._render_command(step.run, variables, captured)
            outcome.run = rendered
        unresolved = _TOKEN_RE.search(rendered)
        if unresolved:
            outcome.status = "skipped"
            outcome.reason = f"unresolved token: {unresolved.group(0)}"
            return outcome
        outcome.run = rendered
        if self.dry_run:
            outcome.status = "dry-run"
            return outcome
        started = time.time()
        attempts = 0
        attempts_allowed = max(0, min(_MAX_RETRIES, int(step.retries or 0))) + 1
        while attempts < attempts_allowed:
            attempts += 1
            ok, output, reason = self._execute(rendered, step.timeout)
            outcome.attempts = attempts
            outcome.output = output
            outcome.reason = reason
            if ok and step.expect and step.expect not in output:
                ok = False
                outcome.reason = f"expected text missing: {step.expect[:80]}"
            if ok:
                outcome.status = "ok"
                outcome.duration_ms = (time.time() - started) * 1000
                if step.capture:
                    outcome.captured = output.strip()[:_MAX_CAPTURE_CHARS]
                outcome.artifacts = [
                    render_text(path, variables) for path in step.artifacts if render_text(path, variables)
                ]
                return outcome
            if attempts < attempts_allowed and self.retry_backoff:
                time.sleep(min(self.retry_backoff * attempts, 3.0))
        outcome.status = "timeout" if outcome.reason == "timeout" else "failed"
        outcome.duration_ms = (time.time() - started) * 1000
        return outcome

    def _execute(self, command: str, timeout: int) -> tuple[bool, str, str]:
        """Run one command with an optional timeout and return (ok, output, reason)."""
        limit = float(timeout or self.default_timeout)
        if self.executor is not None:
            return self._call(lambda: self.executor(command), limit)
        if self.shell is None:
            return False, "", "no executor or shell"
        if self._is_verb(command):
            try:
                return True, self._run_shell_verb(command), ""
            except Exception as exc:
                return False, "", str(exc)[:300]
        return self._call(lambda: self._run_raw(command, limit), limit)

    def _is_verb(self, command: str) -> bool:
        """Return True when the first token is a live cmd2 verb or alias."""
        aliases = getattr(self.shell, "aliases", {}) or {}
        try:
            token = shlex.split(command)[0]
        except (ValueError, IndexError):
            return False
        if not token or _SHELL_META.search(command):
            return False
        return callable(getattr(self.shell, f"do_{token}", None)) or token in aliases

    def _run_shell_verb(self, command: str) -> str:
        """Run a cmd2 verb on the calling thread and capture its stdout.

        LazyOwn ``do_*`` methods print through Rich and usually return
        ``None``; capturing the buffer is what makes ``capture:`` and
        ``expect:`` work for verb steps.
        """
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            result = self.shell.onecmd(command)
        text = buffer.getvalue()
        if not text.strip() and result not in (None, True, False):
            text = str(result)
        return text

    def _run_raw(self, command: str, timeout: float) -> str:
        """Run an ordinary command through the shared safe shell primitive."""
        from core.safe_exec import safe_run_shell

        completed = safe_run_shell(
            command,
            allow=True,
            reason=f"YAML chain step: {command[:80]}",
            timeout=timeout,
        )
        output = ((completed.stdout or "") + (completed.stderr or "")).strip()
        if completed.returncode != 0:
            raise RuntimeError(f"exit {completed.returncode}: {output[-300:]}")
        return output

    @staticmethod
    def _call(callback: Callable[[], Any], timeout: float) -> tuple[bool, str, str]:
        """Run a callback in a worker thread and enforce the timeout."""
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(callback)
        try:
            output = future.result(timeout=timeout)
            text = "" if output is None else str(output)
            return True, text, ""
        except (futures.TimeoutError, subprocess.TimeoutExpired):
            future.cancel()
            return False, "", "timeout"
        except Exception as exc:
            return False, "", str(exc)[:300]
        finally:
            executor.shutdown(wait=False, cancel_futures=True)


__all__ = ["ChainRunResult", "ChainRunner", "StepOutcome", "render_text"]
