"""Contracts for the single Lazy autonomous orchestrator.

Every loop subsystem depends on these Protocols, never on concrete
classes. The orchestrator (LazyLoopEngine.run/run_round) invokes all
subsystems, so a human runs ONE command and the engine invokes the
ten operator-visible steps internally.
"""

from __future__ import annotations

from typing import Protocol


class IFrontier(Protocol):
    """Pending-intent queue with atomic claim."""

    def pending(self) -> list:
        """Return pending intents ordered by priority."""
        ...

    def claim_next(self) -> object | None:
        """Atomically claim highest-priority intent or None."""
        ...

    def release(self, node_id: int, state: str = "pending") -> bool:
        """Return a running intent to a new state."""
        ...


class IPlanner(Protocol):
    """Sole intent generator."""

    def plan(self, triggers: list[dict] | None = None) -> list:
        """Emit 0..N intents from current situation."""
        ...


class IWorker(Protocol):
    """Executes exactly one claimed intent."""

    def execute(self, intent, executor=None) -> dict:
        """Run intent to completion and write facts back."""
        ...


class IGuard(Protocol):
    """Safety boundary for every tool call."""

    def check(self, tool: str, command: str) -> dict:
        """Return allow/ask/deny decision and audit it."""
        ...


class IEnricher(Protocol):
    """DNS/HTTP enrichment feeding the planner."""

    def enrich(self, value: str) -> dict:
        """Enrich one asset synchronously."""
        ...


class IRetester(Protocol):
    """Replay finding evidence to a verdict."""

    def retest(self, finding_id: int, executor=None) -> dict:
        """Return verdict for one finding."""
        ...


class ICompactor(Protocol):
    """Fold stale nodes into digests."""

    def compact(self, threshold: int = 50) -> dict:
        """Digest cold facts beyond threshold."""
        ...


class IBudget(Protocol):
    """Three-level budget: rounds, toolcalls, task deadline."""

    def check(self, task_id: str) -> dict:
        """Return ok/exceeded decision with reason."""
        ...

    def record_toolcall(self, task_id: str, intent_id: int = 0) -> None:
        """Count one executed tool call."""
        ...


class IRuntime(Protocol):
    """Observable runtime: abort cause, workers, heartbeat."""

    def heartbeat(self, task_id: str) -> dict:
        """Return live runtime snapshot."""
        ...

    def abort(self, task_id: str, cause: str, detail: str = "") -> bool:
        """Stamp abort cause like typed AbortCause."""
        ...


class IFinding(Protocol):
    """Finding lifecycle: report, status, severity-ranked list."""

    def report(self, name: str, summary: str = "", poc: str = "",
               severity: str = "", vulnclass: str = "",
               intent_id: int = 0, asset_ids: list[int] | None = None,
               traffic_refs: list[str] | None = None) -> object:
        """Register a deduplicated finding with severity and evidence."""
        ...

    def set_status(self, finding_id: int, status: str) -> bool:
        """Transition finding disposition."""
        ...

    def ranked(self) -> list:
        """Return findings critical-first."""
        ...


class INotifier(Protocol):
    """Finding event fan-out: finding_created / finding_status_changed."""

    def emit(self, task_id: str, event: str, data: dict) -> int:
        """Fan out one event; returns deliveries."""
        ...


class ITrigger(Protocol):
    """Event/interval triggers evaluated once per round like the scheduler."""

    def add(self, kind: str, arg: str = "", every_sec: float = 0.0) -> dict:
        """Register a trigger."""
        ...

    def due(self, task_id: str, graph: object, activity: object) -> list[dict]:
        """Evaluate and fire due triggers."""
        ...


class ILlmPool(Protocol):
    """Optional LLM chain with failover; empty reply when unconfigured."""

    def complete(self, prompt: str, max_tokens: int = 800) -> str:
        """Fail over across members and return text or empty string."""
        ...


class IToolCatalog(Protocol):
    """Per-agent tool bindings."""

    def bindings(self, agent: str = "") -> dict:
        """Return bindings for one agent or the whole table."""
        ...

    def bind(self, agent: str, tool: str) -> list[str]:
        """Opt a tool into an agent lane."""
        ...


__all__ = ["IFrontier", "IPlanner", "IWorker", "IGuard", "IEnricher",
           "IRetester", "ICompactor", "IBudget", "IRuntime",
           "IFinding", "INotifier", "ITrigger", "ILlmPool", "IToolCatalog"]
