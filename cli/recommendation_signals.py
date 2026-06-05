"""Concrete :class:`cli.recommendation.RecommendationSignal` adapters.

Each adapter wraps one of the framework's pre-existing "what next" brains and
translates its native output into the common :class:`cli.recommendation.Proposal`
currency so :class:`cli.recommendation.RecommendationEngine` can fuse them. The
heavy backends (the graphify index, the policy store, the nmap reader) are
imported lazily inside each adapter, which keeps the core engine module free of
optional third-party dependencies and lets a missing backend degrade to an empty
proposal list instead of an import error.

The :func:`build_default_engine` factory wires the four deterministic signals in
priority order and is the single entry point every consumer (the ``recommend_next``
CLI verb, the inline push hints, the MCP tool) should call.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Mapping, Sequence

from cli.recommendation import (
    KIND_ADDON,
    KIND_COMMAND,
    KIND_TOOL,
    SOURCE_GRAPH,
    SOURCE_KILLCHAIN,
    SOURCE_POLICY,
    SOURCE_RECON,
    CategoryResolver,
    EngineWeights,
    Proposal,
    RecommendationContext,
    RecommendationEngine,
)

_TRANSCRIPT_FILE = "LazyOwn_session_report.csv"
_TRANSCRIPT_COLUMNS = ("command", "tool", "name")
_DEFAULT_RECENT_WINDOW = 10
_RANK_FLOOR = 0.2
_KIND_BY_RECON = {"addon": KIND_ADDON, "tool": KIND_TOOL, "command": KIND_COMMAND}


def _rank_weight(index: int, total: int) -> float:
    """Map a zero-based rank to a descending weight in ``(_RANK_FLOOR, 1]``.

    Signals whose backend emits an ordered list without numeric scores (the
    recon plan, the static kill-chain tables) use this so a stable, position-based
    importance feeds the engine's per-signal normalisation.

    Args:
        index: Zero-based position in the ordered list.
        total: Length of the ordered list.

    Returns:
        ``1.0`` for the first item, decaying linearly to ``_RANK_FLOOR``.
    """
    if total <= 1:
        return 1.0
    span = 1.0 - _RANK_FLOOR
    return 1.0 - span * (index / (total - 1))


class GraphSignal:
    """Adapt :meth:`cli.graph_advisor.GraphAdvisor.suggest_next` into proposals."""

    name = SOURCE_GRAPH

    def __init__(self, advisor: Any) -> None:
        """Store the graph advisor facade.

        Args:
            advisor: Any object exposing ``suggest_next(recent_commands, limit)``
                and returning summary dicts carrying ``label``/``id`` and
                ``score`` keys.
        """
        self._advisor = advisor

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return graph-adjacent command proposals for ``ctx``."""
        if self._advisor is None:
            return []
        suggestions = self._advisor.suggest_next(
            recent_commands=list(ctx.recent_commands), limit=max(ctx.limit * 2, ctx.limit)
        )
        proposals: list[Proposal] = []
        for item in suggestions:
            action = str(item.get("label") or item.get("id") or "").strip()
            if not action:
                continue
            proposals.append(
                Proposal(
                    action=action,
                    kind=KIND_COMMAND,
                    weight=float(item.get("score", 0.0) or 0.0),
                    reason="graph-adjacent to recent activity",
                )
            )
        return proposals


class PolicySignal:
    """Adapt the learned transition policy into kill-chain category priors."""

    name = SOURCE_POLICY

    def __init__(self, policy: Any) -> None:
        """Store the policy integration facade.

        Args:
            policy: Object exposing ``get_recommendations(target)`` returning
                dicts with ``category``, ``confidence`` and ``reason`` keys.
        """
        self._policy = policy

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return category-prior proposals for ``ctx``."""
        if self._policy is None:
            return []
        target = ctx.target or ""
        recs = self._policy.get_recommendations(target)
        proposals: list[Proposal] = []
        for rec in recs or []:
            category = str(rec.get("category", "")).strip()
            if not category:
                continue
            proposals.append(
                Proposal(
                    action=category,
                    kind="category",
                    weight=float(rec.get("confidence", 0.0) or 0.0),
                    reason=str(rec.get("reason", "")),
                    category=category,
                )
            )
        return proposals


class ReconPlanSignal:
    """Adapt the nmap trigger-matched recon plan into concrete proposals."""

    name = SOURCE_RECON

    def __init__(self, engine: Any, builder: Any) -> None:
        """Store the exploration engine and the plan builder callable.

        Args:
            engine: A configured ``cli.exploration.ExplorationEngine``.
            builder: The ``cli.recon_plan.build_recon_plan`` callable.
        """
        self._engine = engine
        self._builder = builder

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return trigger-matched addon/tool/command proposals for ``ctx``."""
        if self._engine is None or self._builder is None:
            return []
        plan = self._builder(target=ctx.target, engine=self._engine, payload=ctx.payload)
        items = getattr(plan, "items", ())
        total = len(items)
        proposals: list[Proposal] = []
        for index, item in enumerate(items):
            kind = _KIND_BY_RECON.get(item.kind)
            if kind is None:
                continue
            proposals.append(
                Proposal(
                    action=item.name,
                    kind=kind,
                    weight=_rank_weight(index, total),
                    reason=item.reason,
                    command_preview=item.command_preview,
                )
            )
        return proposals


class KillChainSignal:
    """Adapt the static kill-chain adjacency tables into concrete proposals."""

    name = SOURCE_KILLCHAIN

    def __init__(
        self,
        next_table: Mapping[str, Sequence[str]],
        phase_table: Mapping[str, Sequence[str]],
    ) -> None:
        """Store the adjacency and phase-priority tables.

        Args:
            next_table: Map of command verb to its sensible follow-ups.
            phase_table: Map of kill-chain phase to its priority verbs.
        """
        self._next = next_table
        self._phase = phase_table

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return adjacency- and phase-derived proposals for ``ctx``."""
        already_run = {c for c in ctx.recent_commands}
        last = ctx.recent_commands[-1] if ctx.recent_commands else ""
        ordered: list[tuple[str, str]] = []
        seen: set[str] = set()

        for verb in self._next.get(last, ()):  # type: ignore[arg-type]
            if verb in already_run or verb in seen:
                continue
            seen.add(verb)
            ordered.append((verb, f"kill-chain follow-up after '{last}'"))

        phase_key = (ctx.phase or "recon").lower()
        for verb in self._phase.get(phase_key, self._phase.get("recon", ())):
            if verb in already_run or verb in seen or verb == last:
                continue
            seen.add(verb)
            ordered.append((verb, f"phase priority for '{phase_key}'"))

        total = len(ordered)
        return [
            Proposal(
                action=verb,
                kind=KIND_COMMAND,
                weight=_rank_weight(index, total),
                reason=reason,
            )
            for index, (verb, reason) in enumerate(ordered)
        ]


def read_recent_commands(sessions_dir: str = "sessions", window: int = _DEFAULT_RECENT_WINDOW) -> list[str]:
    """Return the last ``window`` command verbs from the session transcript.

    Args:
        sessions_dir: Path to the ``sessions/`` directory.
        window: Maximum number of trailing verbs to return.

    Returns:
        Ordered command verbs, most recent last. Empty when the transcript is
        absent or unreadable.
    """
    path = Path(sessions_dir) / _TRANSCRIPT_FILE
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, csv.Error):
        return []
    if not rows:
        return []
    column = next((c for c in _TRANSCRIPT_COLUMNS if c in rows[0]), None)
    if column is None:
        return []
    verbs: list[str] = []
    for row in rows[-window:]:
        raw = (row.get(column) or "").strip()
        if raw:
            verbs.append(raw.split()[0])
    return verbs


def build_context(
    payload: Mapping[str, Any],
    sessions_dir: str = "sessions",
    target: str | None = None,
    limit: int = 5,
) -> RecommendationContext:
    """Assemble a :class:`RecommendationContext` from live engagement state.

    Args:
        payload: ``payload.json`` mapping.
        sessions_dir: Path to ``sessions/`` for transcript reads.
        target: Explicit target. Falls back to ``payload['rhost']``.
        limit: Maximum recommendations the caller wants.

    Returns:
        A populated context shared by every signal.
    """
    resolved_target = (target or payload.get("rhost") or "").strip() or None
    phase = str(payload.get("phase", "") or "recon").lower()
    recent = read_recent_commands(sessions_dir)
    return RecommendationContext(
        target=resolved_target,
        payload=payload,
        recent_commands=recent,
        phase=phase,
        limit=limit,
    )


def build_default_engine(
    payload: Mapping[str, Any] | None = None,
    sessions_dir: str = "sessions",
    graph_path: str | None = None,
    command_index_path: str = "cli/command_index.json",
    weights: EngineWeights | None = None,
) -> RecommendationEngine:
    """Wire every available deterministic signal into one engine.

    Signals whose backend cannot be imported or constructed are skipped silently
    so the returned engine always works with whatever is present. The kill-chain
    signal is unconditional because its tables ship with the framework.

    Args:
        payload: ``payload.json`` mapping used to resolve the victim OS for the
            recon-plan signal.
        sessions_dir: Path to ``sessions/`` (currently informational; the
            collaborators resolve their own paths).
        graph_path: Optional explicit graphify graph path.
        command_index_path: Path to ``command_index.json`` for category priors.
        weights: Optional fusion-weight override.

    Returns:
        A ready :class:`RecommendationEngine`.
    """
    payload = payload or {}
    signals: list[Any] = []

    graph_signal = _try_build_graph_signal(graph_path)
    if graph_signal is not None:
        signals.append(graph_signal)

    policy_signal = _try_build_policy_signal()
    if policy_signal is not None:
        signals.append(policy_signal)

    recon_signal = _try_build_recon_signal(payload)
    if recon_signal is not None:
        signals.append(recon_signal)

    signals.append(_build_killchain_signal())

    resolver = CategoryResolver(command_index_path)
    return RecommendationEngine(signals=signals, resolver=resolver, weights=weights)


def _try_build_graph_signal(graph_path: str | None) -> GraphSignal | None:
    """Build a :class:`GraphSignal` when the graphify index is loadable."""
    try:
        from cli.graph_advisor import GraphAdvisor

        advisor = GraphAdvisor.from_path(graph_path)
        if not advisor.is_available():
            return None
        return GraphSignal(advisor)
    except Exception:
        return None


def _try_build_policy_signal() -> PolicySignal | None:
    """Build a :class:`PolicySignal` when the policy engine imports cleanly."""
    try:
        import sys

        skills_dir = str(Path("skills").resolve())
        if skills_dir not in sys.path:
            sys.path.insert(0, skills_dir)
        from lazyown_policy import LazyOwnPolicyIntegration

        return PolicySignal(LazyOwnPolicyIntegration())
    except Exception:
        return None


def _try_build_recon_signal(payload: Mapping[str, Any]) -> ReconPlanSignal | None:
    """Build a :class:`ReconPlanSignal` when the exploration stack imports."""
    try:
        from cli.exploration import ExplorationEngine, resolve_current_os
        from cli.recon_plan import build_recon_plan

        engine = ExplorationEngine(current_os=resolve_current_os(payload))
        return ReconPlanSignal(engine=engine, builder=build_recon_plan)
    except Exception:
        return None


def _build_killchain_signal() -> KillChainSignal:
    """Build the unconditional static-table :class:`KillChainSignal`."""
    from cli.reactive_hints import _KILL_CHAIN_NEXT, _PHASE_PRIORITY

    return KillChainSignal(next_table=_KILL_CHAIN_NEXT, phase_table=_PHASE_PRIORITY)


__all__ = [
    "GraphSignal",
    "PolicySignal",
    "ReconPlanSignal",
    "KillChainSignal",
    "read_recent_commands",
    "build_context",
    "build_default_engine",
]
