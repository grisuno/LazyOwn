"""Unified next-best-action engine: the single source of truth for "what next".

Before this module the framework carried four independent "what should I run
next" brains that never spoke to each other:

* the graphify proximity walk (:meth:`cli.graph_advisor.GraphAdvisor.suggest_next`),
* the learned transition policy (:class:`skills.lazyown_policy.LazyOwnPolicyIntegration`),
* the nmap trigger-matched recon plan (:func:`cli.recon_plan.build_recon_plan`),
* the static kill-chain adjacency tables in :mod:`cli.reactive_hints`.

Each surface (the ``recommend_next`` CLI verb, the inline push hints, the MCP
tool) wired a different subset by hand, so the operator saw three unmerged lists
and had to synthesise them mentally. This module collapses them into one logical
chain of thought.

The fusion model has two tiers, mirroring the natural granularity of the inputs:

* **Concrete-action signals** (graph, recon plan, kill-chain) propose individual
  commands / addons / tools, each with a signal-local weight.
* **Category-prior signals** (policy) propose kill-chain *categories* with a
  confidence. These do not name a command; instead they up- or down-weight every
  concrete action that belongs to the category.

:class:`RecommendationEngine` normalises every signal, multiplies each concrete
action by its category prior, merges duplicates across signals (carrying the full
provenance), and returns a single ranked list of :class:`Recommendation`.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py`` (Dependency Inversion):
      consumers depend on this module, never the reverse.
    - Every signal is a :class:`RecommendationSignal`; adding a sixth brain means
      writing one adapter and registering it (Open/Closed). The engine never
      changes.
    - Each signal owns its own failure handling: a signal that raises or whose
      backend is absent contributes nothing instead of breaking the chain, so the
      engine is always available (graceful degradation).
    - No magic numbers: every weight, floor and span lives in
      :class:`EngineWeights`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol, Sequence, runtime_checkable

SOURCE_GRAPH = "graph"
SOURCE_POLICY = "policy"
SOURCE_RECON = "recon"
SOURCE_KILLCHAIN = "killchain"

KIND_COMMAND = "command"
KIND_ADDON = "addon"
KIND_TOOL = "tool"
KIND_CATEGORY = "category"
KIND_NOTE = "note"

_DEFAULT_COMMAND_INDEX = "cli/command_index.json"
_DEFAULT_SESSIONS_DIR = "sessions"
_DEFAULT_LIMIT = 5


@dataclass(frozen=True)
class EngineWeights:
    """Immutable fusion parameters shared by every recommendation run.

    Attributes:
        signal_weights: Global multiplier per concrete-action signal. The recon
            plan ranks highest because it is grounded in a real scan of the
            target; the graph walk and the static kill-chain tables are advisory.
        category_prior_floor: Lowest multiplier a concrete action can receive
            from a cold policy category. Never zero, so a single signal can still
            surface an action the policy has not yet learned to favour.
        category_prior_span: Width added on top of the floor for a maximally
            confident policy category. ``floor + span`` is the hottest prior.
        neutral_prior: Multiplier applied to actions whose category carries no
            policy signal at all.
        category_recommendation_weight: Score assigned to a standalone strategic
            category recommendation so it ranks below concrete actions of similar
            confidence while remaining visible.
    """

    signal_weights: Mapping[str, float] = field(
        default_factory=lambda: {
            SOURCE_RECON: 1.0,
            SOURCE_GRAPH: 0.6,
            SOURCE_KILLCHAIN: 0.5,
        }
    )
    category_prior_floor: float = 0.6
    category_prior_span: float = 0.8
    neutral_prior: float = 1.0
    category_recommendation_weight: float = 0.45


@dataclass(frozen=True)
class RecommendationContext:
    """Everything a signal needs to produce proposals for one decision.

    Attributes:
        target: Active rhost (or ``None`` to let scan-backed signals fall back to
            the most recent artefact in ``sessions/``).
        payload: ``payload.json`` mapping; signals read phase, creds and OS hints.
        recent_commands: Ordered command verbs already executed this session,
            most recent last. Seeds the graph walk and the kill-chain adjacency.
        phase: Resolved kill-chain phase, used by the recon plan and as a
            category fallback.
        limit: Maximum number of fused recommendations the caller wants.
    """

    target: str | None
    payload: Mapping[str, Any]
    recent_commands: Sequence[str]
    phase: str
    limit: int = _DEFAULT_LIMIT


@dataclass(frozen=True)
class Proposal:
    """A single raw suggestion emitted by one signal, before fusion.

    Attributes:
        action: Command / addon / tool identifier, or a category name when
            ``kind`` is :data:`KIND_CATEGORY`.
        kind: One of the ``KIND_*`` constants.
        weight: Signal-local importance in ``[0, 1]``. Normalised against the
            signal's own maximum before the global weight is applied.
        reason: One-line English justification shown to the operator.
        category: Kill-chain category the action belongs to, when the signal
            already knows it. Empty lets the engine resolve it from the command
            index.
        command_preview: Best-effort copy-paste command string, when available.
        mitre: Optional MITRE ATT&CK technique id.
    """

    action: str
    kind: str
    weight: float
    reason: str
    category: str = ""
    command_preview: str = ""
    mitre: str = ""


@dataclass(frozen=True)
class Recommendation:
    """A fused, ranked next action with full provenance.

    Attributes:
        action: The suggested command / addon / tool / category.
        kind: One of the ``KIND_*`` constants.
        score: Fused score after normalisation, global weighting and category
            priors. Higher is better; values are not bounded to ``[0, 1]`` once
            multiple signals reinforce the same action.
        category: Resolved kill-chain category, or empty when unknown.
        sources: Names of every signal that contributed, in registration order.
        reasons: One provenance line per contributing signal.
        command_preview: Copy-paste command when any signal supplied one.
        mitre: MITRE technique id when any signal supplied one.
    """

    action: str
    kind: str
    score: float
    category: str
    sources: tuple[str, ...]
    reasons: tuple[str, ...]
    command_preview: str = ""
    mitre: str = ""


@runtime_checkable
class RecommendationSignal(Protocol):
    """Contract every recommendation brain must satisfy to join the chain.

    Implementations must be side-effect free beyond reading their own backend and
    must never raise out of :meth:`propose`; an unavailable backend returns an
    empty list so the engine degrades gracefully.
    """

    name: str

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return zero or more :class:`Proposal` objects for ``ctx``."""
        ...


class CategoryResolver:
    """Map a concrete command to its kill-chain category.

    The lookup is built once from ``cli/command_index.json`` (its
    ``category_to_commands`` / ``phase_to_commands`` sections) and consulted by
    the engine to decide which policy prior applies to each concrete action. The
    loader is injected so tests run without touching the real index.
    """

    def __init__(
        self,
        index_path: str = _DEFAULT_COMMAND_INDEX,
        loader: Callable[[Path], Mapping[str, Any] | None] | None = None,
    ) -> None:
        """Build the resolver from the command index.

        Args:
            index_path: Path to ``command_index.json``.
            loader: Injected reader returning the parsed index or ``None``.
        """
        self._command_to_category: dict[str, str] = {}
        read = loader or _load_command_index
        data = read(Path(index_path))
        if not data:
            return
        for section in ("category_to_commands", "phase_to_commands"):
            mapping = data.get(section)
            if not isinstance(mapping, Mapping):
                continue
            for category, commands in mapping.items():
                if not isinstance(commands, (list, tuple)):
                    continue
                for command in commands:
                    self._command_to_category.setdefault(str(command), str(category))

    def category_for(self, action: str) -> str:
        """Return the kill-chain category for ``action`` or an empty string."""
        return self._command_to_category.get(action, "")


class RecommendationEngine:
    """Fuse every registered signal into one ranked recommendation list.

    The engine holds no per-call state; :meth:`recommend` is pure with respect to
    the injected signals and resolver, which is what lets the CLI verb, the push
    hints and the MCP tool share a single instance without coupling.
    """

    def __init__(
        self,
        signals: Sequence[RecommendationSignal],
        resolver: CategoryResolver | None = None,
        weights: EngineWeights | None = None,
    ) -> None:
        """Wire the engine with its signals and fusion parameters.

        Args:
            signals: Concrete-action and category-prior signals to fuse.
            resolver: Command-to-category resolver. Built from the default index
                when omitted.
            weights: Fusion parameters. Defaults to :class:`EngineWeights`.
        """
        self._signals = list(signals)
        self._resolver = resolver or CategoryResolver()
        self._weights = weights or EngineWeights()

    def recommend(self, ctx: RecommendationContext) -> list[Recommendation]:
        """Return the fused, ranked recommendations for ``ctx``.

        Args:
            ctx: The decision context shared with every signal.

        Returns:
            Up to ``ctx.limit`` :class:`Recommendation` objects, ordered by fused
            score descending and action name ascending for determinism.
        """
        collected: list[tuple[str, list[Proposal]]] = []
        for signal in self._signals:
            collected.append((signal.name, self._safe_propose(signal, ctx)))

        priors = self._build_category_priors(collected)
        fused = self._fuse_concrete_actions(collected, priors)
        fused.extend(self._category_recommendations(collected, fused))

        fused.sort(key=lambda rec: (-rec.score, rec.action))
        return fused[: ctx.limit]

    @staticmethod
    def _safe_propose(signal: RecommendationSignal, ctx: RecommendationContext) -> list[Proposal]:
        """Call ``signal.propose`` swallowing any failure into an empty list."""
        try:
            return list(signal.propose(ctx))
        except Exception:
            return []

    def _build_category_priors(self, collected: Sequence[tuple[str, list[Proposal]]]) -> dict[str, float]:
        """Translate policy category proposals into per-category multipliers."""
        priors: dict[str, float] = {}
        floor = self._weights.category_prior_floor
        span = self._weights.category_prior_span
        for _name, proposals in collected:
            for proposal in proposals:
                if proposal.kind != KIND_CATEGORY:
                    continue
                confidence = _clamp01(proposal.weight)
                prior = floor + span * confidence
                key = proposal.action
                priors[key] = max(priors.get(key, prior), prior)
        return priors

    def _fuse_concrete_actions(
        self,
        collected: Sequence[tuple[str, list[Proposal]]],
        priors: Mapping[str, float],
    ) -> list[Recommendation]:
        """Merge concrete proposals across signals into ranked recommendations."""
        accumulator: dict[str, _Accumulator] = {}
        for name, proposals in collected:
            concrete = [p for p in proposals if p.kind != KIND_CATEGORY]
            if not concrete:
                continue
            global_weight = self._weights.signal_weights.get(name, 0.0)
            if global_weight <= 0.0:
                continue
            peak = max((_non_negative(p.weight) for p in concrete), default=0.0)
            if peak <= 0.0:
                continue
            for proposal in concrete:
                normalised = _non_negative(proposal.weight) / peak
                category = proposal.category or self._resolver.category_for(proposal.action)
                prior = priors.get(category, self._weights.neutral_prior)
                contribution = global_weight * normalised * prior
                slot = accumulator.get(proposal.action)
                if slot is None:
                    slot = _Accumulator(action=proposal.action, kind=proposal.kind, category=category)
                    accumulator[proposal.action] = slot
                slot.add(name, contribution, proposal)
        return [slot.build() for slot in accumulator.values()]

    def _category_recommendations(
        self,
        collected: Sequence[tuple[str, list[Proposal]]],
        concrete: Sequence[Recommendation],
    ) -> list[Recommendation]:
        """Surface strategic categories that no concrete action already covers."""
        covered = {rec.category for rec in concrete if rec.category}
        out: list[Recommendation] = []
        seen: set[str] = set()
        base = self._weights.category_recommendation_weight
        for name, proposals in collected:
            for proposal in proposals:
                if proposal.kind != KIND_CATEGORY:
                    continue
                if proposal.action in covered or proposal.action in seen:
                    continue
                seen.add(proposal.action)
                out.append(
                    Recommendation(
                        action=proposal.action,
                        kind=KIND_CATEGORY,
                        score=base * _clamp01(proposal.weight),
                        category=proposal.action,
                        sources=(name,),
                        reasons=(proposal.reason,),
                    )
                )
        return out


@dataclass
class _Accumulator:
    """Mutable fusion slot collecting every contribution to one action."""

    action: str
    kind: str
    category: str
    score: float = 0.0
    sources: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    command_preview: str = ""
    mitre: str = ""

    def add(self, source: str, contribution: float, proposal: Proposal) -> None:
        """Fold one signal's proposal into the running total."""
        self.score += contribution
        if source not in self.sources:
            self.sources.append(source)
        if proposal.reason:
            self.reasons.append(f"[{source}] {proposal.reason}")
        if not self.command_preview and proposal.command_preview:
            self.command_preview = proposal.command_preview
        if not self.mitre and proposal.mitre:
            self.mitre = proposal.mitre

    def build(self) -> Recommendation:
        """Freeze the slot into an immutable :class:`Recommendation`."""
        return Recommendation(
            action=self.action,
            kind=self.kind,
            score=round(self.score, 4),
            category=self.category,
            sources=tuple(self.sources),
            reasons=tuple(self.reasons),
            command_preview=self.command_preview,
            mitre=self.mitre,
        )


def _clamp01(value: float) -> float:
    """Clamp ``value`` into the closed unit interval.

    Used for probability-like inputs such as a policy category confidence.
    """
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)


def _non_negative(value: float) -> float:
    """Floor ``value`` at zero, preserving its scale for peak normalisation.

    Concrete-action signals (the graph walk in particular) emit unbounded
    positive importances; clamping them to one before normalisation would
    collapse their relative ranking, so only the negative tail is removed.
    """
    return float(value) if value > 0.0 else 0.0


def _load_command_index(path: Path) -> Mapping[str, Any] | None:
    """Read ``command_index.json`` with stdlib only, returning ``None`` on error."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, Mapping) else None


__all__ = [
    "SOURCE_GRAPH",
    "SOURCE_POLICY",
    "SOURCE_RECON",
    "SOURCE_KILLCHAIN",
    "KIND_COMMAND",
    "KIND_ADDON",
    "KIND_TOOL",
    "KIND_CATEGORY",
    "KIND_NOTE",
    "EngineWeights",
    "RecommendationContext",
    "Proposal",
    "Recommendation",
    "RecommendationSignal",
    "CategoryResolver",
    "RecommendationEngine",
]
