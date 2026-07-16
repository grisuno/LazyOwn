"""Caldera-style operation lifecycle: create, start, pause, resume, stop, status.

Operations are persistent, time-bounded adversary emulations that wrap
the existing :class:`modules.playbook_engine.PlaybookEngine` and bridge
its output into the :class:`modules.world_model.WorldModel` and
:class:`modules.obs_parser.ObsParser` fact store.

Each operation has:
- A name and target
- A list of steps (PlaybookStep from playbook_engine)
- A status (planned, running, paused, completed, stopped, failed)
- An event log (timeline)
- A produced-facts index
- A TTP coverage map (technique_id -> status)

Operations persist to ``sessions/operations/<id>.json`` so they survive
shell restarts and can be resumed across shifts.
"""

from __future__ import annotations

import builtins
import json
import logging
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger("operation")

_BASE_DIR     = Path(__file__).parent.parent
_OPS_DIR      = _BASE_DIR / "sessions" / "operations"
_OPS_DIR.mkdir(parents=True, exist_ok=True)


class OperationStatus(StrEnum):
    PLANNED   = "planned"
    RUNNING   = "running"
    PAUSED    = "paused"
    COMPLETED = "completed"
    STOPPED   = "stopped"
    FAILED    = "failed"


@dataclass
class OpEvent:
    timestamp: str
    step_index: int
    step_name: str
    status: str
    summary: str
    findings_count: int = 0
    error: str = ""


@dataclass
class OperationStep:
    step_index: int
    name: str
    technique_id: str
    tactic: str
    command: str
    description: str = ""
    status: str = "pending"
    started_at: str = ""
    finished_at: str = ""
    output_excerpt: str = ""
    findings_count: int = 0
    error: str = ""


@dataclass
class Operation:
    id: str
    name: str
    target: str
    apt_name: str
    status: str = OperationStatus.PLANNED.value
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: str = ""
    finished_at: str = ""
    steps: list[OperationStep] = field(default_factory=list)
    events: list[OpEvent] = field(default_factory=list)
    facts_produced: list[dict[str, Any]] = field(default_factory=list)
    ttp_coverage: dict[str, str] = field(default_factory=dict)
    description: str = ""

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "target": self.target,
            "apt_name": self.apt_name,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "description": self.description,
            "steps": [asdict(s) for s in self.steps],
            "events": [asdict(e) for e in self.events],
            "facts_produced": self.facts_produced,
            "ttp_coverage": self.ttp_coverage,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Operation:
        op = cls(
            id=d.get("id", str(uuid.uuid4())[:8]),
            name=d.get("name", ""),
            target=d.get("target", ""),
            apt_name=d.get("apt_name", ""),
            status=d.get("status", OperationStatus.PLANNED.value),
            created_at=d.get("created_at", ""),
            started_at=d.get("started_at", ""),
            finished_at=d.get("finished_at", ""),
            description=d.get("description", ""),
        )
        op.steps = [OperationStep(**s) for s in d.get("steps", [])]
        op.events = [OpEvent(**e) for e in d.get("events", [])]
        op.facts_produced = d.get("facts_produced", [])
        op.ttp_coverage = d.get("ttp_coverage", {})
        return op

    def save(self) -> None:
        path = _OPS_DIR / f"{self.id}.json"
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

    # ------------------------------------------------------------------
    # Event helpers
    # ------------------------------------------------------------------

    def log_event(
        self,
        step_index: int,
        step_name: str,
        status: str,
        summary: str,
        findings_count: int = 0,
        error: str = "",
    ) -> None:
        ev = OpEvent(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            step_index=step_index,
            step_name=step_name,
            status=status,
            summary=summary,
            findings_count=findings_count,
            error=error,
        )
        self.events.append(ev)
        log.info("op=%s step=%d %s: %s", self.id, step_index, status, summary)

    def record_facts(self, findings: list[dict[str, Any]]) -> None:
        for f in findings:
            self.facts_produced.append({
                "produced_at": datetime.now().isoformat(timespec="seconds"),
                "step_index": len(self.facts_produced),
                **f,
            })


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class OperationManager:
    """Persistent store and executor for Operation objects."""

    def __init__(self) -> None:
        self._cache: dict[str, Operation] = {}
        self._current_id: str | None = None

    def list(self) -> builtins.list[Operation]:
        """List all persisted operations."""
        ops: list[Operation] = []
        for f in sorted(_OPS_DIR.glob("*.json")):
            try:
                with open(f) as fh:
                    data = json.load(fh)
                ops.append(Operation.from_dict(data))
            except Exception as exc:
                log.warning("failed to load %s: %s", f, exc)
        return ops

    def get(self, op_id: str) -> Operation | None:
        path = _OPS_DIR / f"{op_id}.json"
        if not path.exists():
            return None
        with open(path) as f:
            return Operation.from_dict(json.load(f))

    def create(
        self,
        name: str,
        target: str,
        apt_name: str = "",
        description: str = "",
    ) -> Operation:
        """Create a new planned operation."""
        op = Operation(
            id=str(uuid.uuid4())[:8],
            name=name,
            target=target,
            apt_name=apt_name or "LazyOwn_auto",
            description=description,
        )
        op.log_event(-1, "create", "ok", f"operation {op.id} created for target {target}")
        op.save()
        return op

    def plan_from_apt(
        self,
        op: Operation,
        playbook_yaml_path: str | None = None,
    ) -> Operation:
        """Populate steps from an APT playbook YAML (or fall back to a derived MITRE playbook).

        Args:
            op: The operation to populate.
            playbook_yaml_path: Path to a playbook YAML. If ``None``,
                derives a playbook from the MITRE STIX2 store.
        """
        from modules.apt_playbooks import AptPlaybook
        from modules.playbook_engine import PlaybookEngine

        steps: list[OperationStep] = []

        if playbook_yaml_path and Path(playbook_yaml_path).is_file():
            try:
                with open(playbook_yaml_path) as f:
                    data = yaml.safe_load(f)
                pb = AptPlaybook.from_dict(data)
                for i, phase in enumerate(pb.phases):
                    steps.append(OperationStep(
                        step_index=i,
                        name=phase.name or "",
                        technique_id=phase.technique_id or "",
                        tactic=phase.name or "",
                        command="",
                        description=phase.description or "",
                    ))
            except Exception as exc:
                log.warning("failed to parse playbook yaml: %s", exc)
        else:
            engine = PlaybookEngine()
            try:
                pb = engine.derive(op.target, phase=None, apt_name=op.apt_name)
                for i, st in enumerate(pb.steps):
                    steps.append(OperationStep(
                        step_index=i,
                        name=st.name,
                        technique_id=st.technique_id,
                        tactic=st.tactic,
                        command=st.command,
                        description=st.description,
                    ))
            except Exception as exc:
                log.warning("planner derive failed: %s", exc)

        op.steps = steps
        for st in op.steps:
            op.ttp_coverage[st.technique_id] = "pending"
        op.log_event(
            -1, "plan", "ok",
            f"planned {len(steps)} steps from {'YAML' if playbook_yaml_path else 'MITRE derive'}"
        )
        op.save()
        return op

    def start(self, op_id: str, executor: Callable[[str, str], str] | None = None) -> Operation:
        """Start or resume a planned operation.

        Args:
            op_id: The operation ID.
            executor: Optional callable ``(command, host) -> output``.
                Defaults to a no-op for safe dry-runs.
        """
        op = self.get(op_id)
        if op is None:
            raise ValueError(f"operation {op_id} not found")
        if op.status == OperationStatus.COMPLETED.value:
            raise ValueError(f"operation {op_id} already completed")
        if op.status != OperationStatus.PAUSED.value:
            op.status = OperationStatus.RUNNING.value
            op.started_at = datetime.now().isoformat(timespec="seconds")
        else:
            op.status = OperationStatus.RUNNING.value
        op.save()

        from modules.obs_parser import get_parser
        from modules.world_model import get_world_model
        parser = get_parser()
        wm = get_world_model()

        for step in op.steps:
            if step.status == "completed":
                continue
            if op.status != OperationStatus.RUNNING.value:
                break

            step.status = "running"
            step.started_at = datetime.now().isoformat(timespec="seconds")
            op.log_event(step.step_index, step.name, "started", f"technique {step.technique_id}")
            op.save()

            try:
                if executor is None:
                    output = ""
                else:
                    output = executor(step.command, op.target)
                step.output_excerpt = output[:200]
                obs = parser.parse(output, tool=step.name, host=op.target)
                step.findings_count = len(obs.findings)
                wm.update_from_findings(obs.findings)
                facts = [
                    {"type": f.type.value, "value": f.value, "host": f.host, "confidence": f.confidence}
                    for f in obs.findings
                ]
                op.record_facts(facts)
                op.ttp_coverage[step.technique_id] = "tested"
                step.status = "completed"
                step.finished_at = datetime.now().isoformat(timespec="seconds")
                op.log_event(
                    step.step_index, step.name, "completed",
                    f"{len(obs.findings)} findings",
                    findings_count=len(obs.findings),
                )
            except Exception as exc:
                step.status = "failed"
                step.error = str(exc)
                op.ttp_coverage[step.technique_id] = "failed"
                op.log_event(
                    step.step_index, step.name, "failed", str(exc)[:120], error=str(exc),
                )
                op.status = OperationStatus.FAILED.value
            op.save()

        if op.status == OperationStatus.RUNNING.value:
            op.status = OperationStatus.COMPLETED.value
            op.finished_at = datetime.now().isoformat(timespec="seconds")
            op.log_event(-1, "complete", "ok", f"{len(op.facts_produced)} total facts")
            op.save()
        return op

    def pause(self, op_id: str) -> Operation:
        op = self.get(op_id)
        if op is None:
            raise ValueError(f"operation {op_id} not found")
        op.status = OperationStatus.PAUSED.value
        op.log_event(-1, "pause", "ok", "operation paused by operator")
        op.save()
        return op

    def resume(self, op_id: str, executor: Callable[[str, str], str] | None = None) -> Operation:
        op = self.get(op_id)
        if op is None:
            raise ValueError(f"operation {op_id} not found")
        if op.status != OperationStatus.PAUSED.value:
            raise ValueError(f"operation {op_id} is not paused")
        return self.start(op_id, executor=executor)

    def stop(self, op_id: str) -> Operation:
        op = self.get(op_id)
        if op is None:
            raise ValueError(f"operation {op_id} not found")
        op.status = OperationStatus.STOPPED.value
        op.finished_at = datetime.now().isoformat(timespec="seconds")
        op.log_event(-1, "stop", "ok", "operation stopped by operator")
        op.save()
        return op

    def status(self, op_id: str) -> dict[str, Any]:
        """Return a structured status dict for an operation."""
        op = self.get(op_id)
        if op is None:
            return {"error": f"operation {op_id} not found"}
        completed = sum(1 for s in op.steps if s.status == "completed")
        failed    = sum(1 for s in op.steps if s.status == "failed")
        pending   = sum(1 for s in op.steps if s.status == "pending")
        running   = sum(1 for s in op.steps if s.status == "running")
        return {
            "id": op.id,
            "name": op.name,
            "target": op.target,
            "apt_name": op.apt_name,
            "status": op.status,
            "created_at": op.created_at,
            "started_at": op.started_at,
            "finished_at": op.finished_at,
            "steps": {
                "total": len(op.steps),
                "completed": completed,
                "failed": failed,
                "pending": pending,
                "running": running,
            },
            "facts_produced": len(op.facts_produced),
            "ttp_coverage": op.ttp_coverage,
        }

    def timeline(self, op_id: str) -> builtins.list[dict[str, Any]]:
        op = self.get(op_id)
        if op is None:
            return []
        return [asdict(e) for e in op.events]

    def report(self, op_id: str) -> str:
        op = self.get(op_id)
        if op is None:
            return f"operation {op_id} not found"
        lines = [
            f"=== Operation {op.id}: {op.name} ===",
            f"Target       : {op.target}",
            f"Threat actor : {op.apt_name}",
            f"Status       : {op.status}",
            f"Created      : {op.created_at}",
            f"Started      : {op.started_at}",
            f"Finished     : {op.finished_at}",
            "",
            f"Steps ({len(op.steps)}):",
        ]
        for s in op.steps:
            mark = {
                "completed": "[x]",
                "failed":    "[!]",
                "running":   "[*]",
                "pending":   "[ ]",
            }.get(s.status, "[?]")
            lines.append(
                f"  {mark} {s.step_index:>3}. [{s.technique_id:<10}] {s.name:<30} "
                f"({s.findings_count} findings)"
            )
        lines.append("")
        lines.append(f"TTP coverage ({len(op.ttp_coverage)} techniques):")
        for tid, status in op.ttp_coverage.items():
            lines.append(f"  {tid:<10} {status}")
        lines.append("")
        lines.append(f"Facts produced: {len(op.facts_produced)}")
        for f in op.facts_produced[:10]:
            lines.append(f"  {f.get('type','?'):<14} {f.get('value','')}")
        if len(op.facts_produced) > 10:
            lines.append(f"  ... and {len(op.facts_produced) - 10} more")
        lines.append("")
        lines.append(f"Events: {len(op.events)}")
        return "\n".join(lines)


def get_manager() -> OperationManager:
    """Return a fresh :class:`OperationManager`."""
    return OperationManager()


__all__ = [
    "Operation",
    "OperationManager",
    "OperationStatus",
    "OpEvent",
    "OperationStep",
    "get_manager",
]
