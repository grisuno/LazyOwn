"""Deterministic replay of past autonomous-daemon runs.

The autonomous daemon (``skills/autonomous_daemon.py``) emits structured
events to ``sessions/autonomous_events.jsonl``. This module reads that
log back and reproduces the recorded decision sequence in two flavours:

* ``trace`` — pure analysis, no command is re-executed. The recorded
  decisions are validated against the deterministic
  ``decision_seed`` stored with each ``STEP_START`` event, surfacing
  any divergence (for example a selector chain that was edited
  between the original run and the replay attempt).
* ``execute`` — same sequence, but each recorded command is rerun
  through the existing :class:`ICommandRunner` chain so the operator
  can compare current output against the recorded snippet. The
  runner chain is **the same** the live daemon uses, so the harness
  layers (permissions, hooks) still apply.

Replay never bypasses the operator approval flow; it stops at the same
checkpoints the live daemon would.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional


REPLAY_MODE_TRACE: str = "trace"
REPLAY_MODE_EXECUTE: str = "execute"
SUPPORTED_REPLAY_MODES: tuple = (REPLAY_MODE_TRACE, REPLAY_MODE_EXECUTE)

STEP_START_TYPE: str = "STEP_START"
STEP_DONE_TYPE: str = "STEP_DONE"
OUTPUT_SNIPPET_LIMIT: int = 280

LAZYOWN_DIR: Path = Path(
    os.environ.get(
        "LAZYOWN_DIR",
        str(Path(__file__).resolve().parent.parent),
    )
)
SESSIONS_DIR: Path = LAZYOWN_DIR / "sessions"
DEFAULT_EVENTS_FILE: Path = SESSIONS_DIR / "autonomous_events.jsonl"

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReplayStep:
    """One reproduced decision in a replay run.

    Attributes:
        event_id: ``id`` of the source ``STEP_START`` event.
        step: Step counter inside the parent objective.
        objective_id: Identifier of the parent objective.
        command: Command that was recorded.
        source: Name of the selector that produced the decision.
        reason: Free-form rationale recorded by the daemon.
        recorded_decision_seed: Decision seed stored at recording time.
        replayed_success: ``None`` in trace mode, ``True``/``False``
            once :meth:`ReplayDispatcher.execute` has run the command.
        replayed_output_snippet: Trimmed output from the replayed run,
            ``None`` in trace mode.
    """

    event_id: str
    step: int
    objective_id: str
    command: str
    source: str
    reason: str
    recorded_decision_seed: Optional[str]
    replayed_success: Optional[bool] = None
    replayed_output_snippet: Optional[str] = None


@dataclass(frozen=True)
class ReplayDivergence:
    """Marker emitted when a replayed step does not match the recording."""

    event_id: str
    step: int
    field: str
    recorded: Any
    recomputed: Any


@dataclass
class ReplayReport:
    """Final outcome of a :class:`ReplayDispatcher` call.

    Attributes:
        mode: ``"trace"`` or ``"execute"``.
        events_seen: Total ``STEP_START`` events considered, before any
            filtering.
        from_event_id: Inclusive lower bound used during the run.
        to_event_id: Inclusive upper bound used during the run.
        steps: Reproduced steps, in chronological order.
        divergences: Detected divergences (empty when the recording is
            consistent).
    """

    mode: str
    events_seen: int
    from_event_id: Optional[str]
    to_event_id: Optional[str]
    steps: List[ReplayStep] = field(default_factory=list)
    divergences: List[ReplayDivergence] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return the report as a JSON-serialisable dictionary."""

        return {
            "mode": self.mode,
            "events_seen": self.events_seen,
            "from_event_id": self.from_event_id,
            "to_event_id": self.to_event_id,
            "steps": [asdict(s) for s in self.steps],
            "divergences": [asdict(d) for d in self.divergences],
        }


class EventLogReader:
    """Parse ``autonomous_events.jsonl`` into in-memory events.

    Malformed lines are skipped with a debug log entry so a single
    truncated line never blocks an entire replay. The reader does not
    perform any filtering on its own; slicing by event id lives in
    :class:`ReplayDispatcher`.
    """

    def __init__(self, path: Path = DEFAULT_EVENTS_FILE) -> None:
        """Initialise the reader.

        Args:
            path: Source JSONL file. Defaults to
                :data:`DEFAULT_EVENTS_FILE`.
        """

        self._path = path

    @property
    def path(self) -> Path:
        """Return the source path."""

        return self._path

    def read(self) -> List[Dict[str, Any]]:
        """Return every event in the log, oldest first.

        Returns:
            A list of decoded events. Empty when the file does not
            exist or cannot be read.
        """

        events: List[Dict[str, Any]] = []
        if not self._path.exists():
            return events
        try:
            with self._path.open("r", encoding="utf-8") as handle:
                for raw in handle:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        events.append(json.loads(raw))
                    except json.JSONDecodeError as exc:
                        _log.debug("event decode error: %s", exc)
        except OSError as exc:
            _log.debug("event read error: %s", exc)
        return events

    def slice(
        self,
        events: List[Dict[str, Any]],
        from_event_id: Optional[str] = None,
        to_event_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Return the inclusive subrange of *events* by ``id``.

        Args:
            events: Source list as returned by :meth:`read`.
            from_event_id: Inclusive lower bound. ``None`` keeps the
                beginning of the log.
            to_event_id: Inclusive upper bound. ``None`` keeps the end
                of the log.

        Returns:
            A subrange of *events*. When both bounds are ``None`` the
            input list is returned unchanged.
        """

        if from_event_id is None and to_event_id is None:
            return list(events)
        started = from_event_id is None
        sliced: List[Dict[str, Any]] = []
        for event in events:
            event_id = event.get("id")
            if not started and event_id == from_event_id:
                started = True
            if started:
                sliced.append(event)
                if to_event_id is not None and event_id == to_event_id:
                    break
        return sliced


class ReplayDispatcher:
    """Drive a replay run over a parsed event log.

    Depends on a :class:`EventLogReader` for input and (in execute
    mode) on a runner exposing a ``run(command, timeout) -> str``
    interface compatible with
    :class:`skills.autonomous_daemon.ICommandRunner`.
    """

    def __init__(
        self,
        reader: Optional[EventLogReader] = None,
        seed_fn: Optional[Callable[[str, int, str], str]] = None,
    ) -> None:
        """Initialise the dispatcher.

        Args:
            reader: Source reader. Defaults to a fresh
                :class:`EventLogReader` against
                :data:`DEFAULT_EVENTS_FILE`.
            seed_fn: Decision-seed function. Defaults to
                :func:`autonomous_daemon.compute_decision_seed`. Injected
                in tests.
        """

        self._reader = reader or EventLogReader()
        self._seed_fn = seed_fn or self._default_seed_fn()

    @staticmethod
    def _default_seed_fn() -> Callable[[str, int, str], str]:
        """Resolve the canonical decision-seed implementation.

        Returns:
            The :func:`compute_decision_seed` from
            :mod:`skills.autonomous_daemon`. A no-op function is
            returned when the module cannot be imported (for example
            in stand-alone unit tests of this module).
        """

        try:
            from autonomous_daemon import compute_decision_seed
        except ImportError:
            try:
                from skills.autonomous_daemon import compute_decision_seed
            except ImportError:
                _log.debug("autonomous_daemon unavailable; seed checks disabled")
                return lambda objective_id, step_n, source: ""
        return compute_decision_seed

    def _collect_step_events(
        self,
        from_event_id: Optional[str],
        to_event_id: Optional[str],
    ) -> tuple:
        """Return ``(events_seen, step_events_in_range)``.

        Args:
            from_event_id: Inclusive lower bound by event id.
            to_event_id: Inclusive upper bound by event id.
        """

        all_events = self._reader.read()
        in_range = self._reader.slice(all_events, from_event_id, to_event_id)
        step_events = [
            event for event in in_range
            if event.get("type") == STEP_START_TYPE
        ]
        return len(step_events), step_events

    def _build_step(
        self,
        event: Dict[str, Any],
        divergences: List[ReplayDivergence],
    ) -> Optional[ReplayStep]:
        """Convert a ``STEP_START`` event into a :class:`ReplayStep`.

        Args:
            event: Raw event dictionary.
            divergences: Mutable accumulator for divergence markers.

        Returns:
            A populated :class:`ReplayStep`, or ``None`` when the event
            payload is missing required fields.
        """

        payload = event.get("payload") or {}
        if not isinstance(payload, dict):
            return None
        command = str(payload.get("command", ""))
        if not command:
            return None
        objective_id = str(
            payload.get("objective_id")
            or payload.get("engagement_id")
            or ""
        )
        step_n = int(payload.get("step", payload.get("attempt", 0)) or 0)
        source = str(payload.get("source", ""))
        recorded_seed = payload.get("decision_seed")
        recomputed_seed = self._seed_fn(objective_id, step_n, source)
        if (
            recorded_seed
            and recomputed_seed
            and recorded_seed != recomputed_seed
        ):
            divergences.append(
                ReplayDivergence(
                    event_id=str(event.get("id", "")),
                    step=step_n,
                    field="decision_seed",
                    recorded=recorded_seed,
                    recomputed=recomputed_seed,
                )
            )
        return ReplayStep(
            event_id=str(event.get("id", "")),
            step=step_n,
            objective_id=objective_id,
            command=command,
            source=source,
            reason=str(payload.get("reason", "")),
            recorded_decision_seed=(
                str(recorded_seed) if recorded_seed else None
            ),
        )

    def trace(
        self,
        from_event_id: Optional[str] = None,
        to_event_id: Optional[str] = None,
    ) -> ReplayReport:
        """Replay the recorded decision sequence without executing it.

        Args:
            from_event_id: Inclusive lower bound on event id.
            to_event_id: Inclusive upper bound on event id.

        Returns:
            A :class:`ReplayReport` populated with one step per
            ``STEP_START`` event in the requested range.
        """

        events_seen, step_events = self._collect_step_events(
            from_event_id, to_event_id
        )
        divergences: List[ReplayDivergence] = []
        steps: List[ReplayStep] = []
        for event in step_events:
            step = self._build_step(event, divergences)
            if step is not None:
                steps.append(step)
        return ReplayReport(
            mode=REPLAY_MODE_TRACE,
            events_seen=events_seen,
            from_event_id=from_event_id,
            to_event_id=to_event_id,
            steps=steps,
            divergences=divergences,
        )

    def execute(
        self,
        from_event_id: Optional[str] = None,
        to_event_id: Optional[str] = None,
        runner: Optional[Any] = None,
        timeout: int = 60,
    ) -> ReplayReport:
        """Replay the recorded sequence and re-run each command.

        Args:
            from_event_id: Inclusive lower bound on event id.
            to_event_id: Inclusive upper bound on event id.
            runner: Runner exposing ``run(command, timeout) -> str``.
                Defaults to the same chain
                :class:`skills.autonomous_daemon.CommandRunnerChain`
                uses live, so the harness layers (permissions, hooks)
                still apply.
            timeout: Per-command timeout in seconds.

        Returns:
            A :class:`ReplayReport` whose steps carry the freshly
            captured output snippets and a recomputed success flag.
        """

        events_seen, step_events = self._collect_step_events(
            from_event_id, to_event_id
        )
        divergences: List[ReplayDivergence] = []
        resolved_runner = runner or self._default_runner()
        steps: List[ReplayStep] = []
        for event in step_events:
            step = self._build_step(event, divergences)
            if step is None:
                continue
            output, success = self._invoke_runner(
                resolved_runner, step.command, timeout
            )
            steps.append(
                ReplayStep(
                    event_id=step.event_id,
                    step=step.step,
                    objective_id=step.objective_id,
                    command=step.command,
                    source=step.source,
                    reason=step.reason,
                    recorded_decision_seed=step.recorded_decision_seed,
                    replayed_success=success,
                    replayed_output_snippet=output[:OUTPUT_SNIPPET_LIMIT],
                )
            )
        return ReplayReport(
            mode=REPLAY_MODE_EXECUTE,
            events_seen=events_seen,
            from_event_id=from_event_id,
            to_event_id=to_event_id,
            steps=steps,
            divergences=divergences,
        )

    @staticmethod
    def _default_runner() -> Any:
        """Build the same runner chain the live daemon uses.

        Returns:
            A :class:`CommandRunnerChain` composed of the MCP and PTY
            runners, falling back to a stub that raises when the daemon
            module is not importable.

        Raises:
            ImportError: If the daemon module is not importable in the
                current environment and no runner was injected.
        """

        try:
            from autonomous_daemon import (
                CommandRunnerChain,
                MCPCommandRunner,
                PTYCommandRunner,
            )
        except ImportError:
            from skills.autonomous_daemon import (
                CommandRunnerChain,
                MCPCommandRunner,
                PTYCommandRunner,
            )
        return CommandRunnerChain([MCPCommandRunner(), PTYCommandRunner()])

    @staticmethod
    def _invoke_runner(
        runner: Any,
        command: str,
        timeout: int,
    ) -> tuple:
        """Run *command* through *runner* and report success heuristically.

        Args:
            runner: Object exposing ``run(command, timeout) -> str``.
            command: Command line to execute.
            timeout: Timeout in seconds.

        Returns:
            ``(output_text, success_bool)``.
        """

        try:
            raw = runner.run(command, timeout)
        except Exception as exc:
            return f"[runner error] {exc}", False
        text = raw or ""
        lowered = text.lower()
        failed_markers = (
            "[timeout]",
            "[run error]",
            "traceback",
            "command not found",
        )
        success = not any(marker in lowered for marker in failed_markers)
        return text, success


def replay(
    from_event_id: Optional[str] = None,
    to_event_id: Optional[str] = None,
    mode: Literal["trace", "execute"] = REPLAY_MODE_TRACE,
    events_path: Optional[Path] = None,
    runner: Optional[Any] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """Convenience entry point used by the MCP tool layer.

    Args:
        from_event_id: Inclusive lower bound on event id.
        to_event_id: Inclusive upper bound on event id.
        mode: ``"trace"`` (default) or ``"execute"``.
        events_path: Override for the JSONL source file. Defaults to
            :data:`DEFAULT_EVENTS_FILE`.
        runner: Optional runner injection used only in ``"execute"`` mode.
        timeout: Per-command timeout in seconds, ``"execute"`` mode only.

    Returns:
        Serialised :class:`ReplayReport` dictionary.

    Raises:
        ValueError: If *mode* is not one of :data:`SUPPORTED_REPLAY_MODES`.
    """

    if mode not in SUPPORTED_REPLAY_MODES:
        raise ValueError(
            f"unsupported replay mode {mode!r}; "
            f"expected one of {SUPPORTED_REPLAY_MODES}"
        )
    reader = EventLogReader(events_path or DEFAULT_EVENTS_FILE)
    dispatcher = ReplayDispatcher(reader=reader)
    if mode == REPLAY_MODE_EXECUTE:
        report = dispatcher.execute(
            from_event_id=from_event_id,
            to_event_id=to_event_id,
            runner=runner,
            timeout=timeout,
        )
    else:
        report = dispatcher.trace(
            from_event_id=from_event_id,
            to_event_id=to_event_id,
        )
    return report.to_dict()
