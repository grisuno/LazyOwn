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
import json
from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from cli.recommendation import (
    KIND_ADDON,
    KIND_COMMAND,
    KIND_TOOL,
    SOURCE_GRAPH,
    SOURCE_GAP,
    SOURCE_KILLCHAIN,
    SOURCE_POLICY,
    SOURCE_RECON,
    CategoryResolver,
    EngineWeights,
    Proposal,
    Recommendation,
    RecommendationContext,
    RecommendationEngine,
)

_TRANSCRIPT_FILE = "LazyOwn_session_report.csv"
_TRANSCRIPT_COLUMNS = ("command", "tool", "name")
_DEFAULT_RECENT_WINDOW = 10
_RANK_FLOOR = 0.2
_KIND_BY_RECON = {"addon": KIND_ADDON, "tool": KIND_TOOL, "command": KIND_COMMAND}
SOURCE_PLAYBOOK = "playbook"
SOURCE_TOPOLOGY = "topology"

_PLAYBOOK_DESCRIPTION_MAX = 80
_GAP_WEIGHT_PRIVESC = 0.95
_GAP_WEIGHT_PRIVESC_UNKNOWN_OS = 0.90
_GAP_WEIGHT_CRED_DUMP = 0.95
_GAP_WEIGHT_ENUM = 0.85
_GAP_WEIGHT_LATERAL = 0.90
_GAP_OWNED_CRED_CAP = 2
_TOPOLOGY_HOST_MULTIPLIER = 2.0
_TOPOLOGY_CRED_MULTIPLIER = 1.5
_TOPOLOGY_NEIGHBOR_CAP = 8

_ENUM_COMMANDS = frozenset({"gobuster", "ffuf", "enum4linux", "nikto", "whatweb", "feroxbuster", "kerbrute"})


def _load_world_model(sessions_dir: str | Path) -> dict | None:
    """Read ``world_model.json`` from ``sessions_dir``, or ``None``.

    Shared by every signal that inspects world-model state. Returns
    ``None`` when the file is missing or malformed so signals degrade to
    an empty proposal list instead of raising.

    Args:
        sessions_dir: Directory containing ``world_model.json``.

    Returns:
        The parsed mapping, or ``None`` when unavailable.
    """
    wm_path = Path(sessions_dir) / "world_model.json"
    if not wm_path.exists():
        return None
    try:
        data = json.loads(wm_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


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

class PlaybookSignal:
    """Adapt APT playbook suggestions into concrete proposals.

    When nmap services match a known playbook profile (APT group, attack
    surface pattern), this signal suggests relevant playbook commands.
    """

    name = SOURCE_PLAYBOOK

    def __init__(self, playbook_engine: Any = None) -> None:
        """Store an optional playbook engine facade.

        Args:
            playbook_engine: Object exposing ``list_playbooks()`` returning
                a list of playbook summary dicts.
        """
        self._engine = playbook_engine

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return playbook-based proposals for the current context."""
        if self._engine is None:
            return []
        try:
            available = self._engine.list_playbooks()
        except Exception:
            available = []
        if not available:
            return []
        proposals: list[Proposal] = []
        for index, pb in enumerate(available[:ctx.limit]):
            if not isinstance(pb, dict):
                continue
            name = str(pb.get("name") or "").strip()
            desc = str(pb.get("description") or "")[: _PLAYBOOK_DESCRIPTION_MAX]
            if not name:
                continue
            proposals.append(
                Proposal(
                    action=f"playbook_run {name}",
                    kind=KIND_COMMAND,
                    weight=_rank_weight(index, len(available)),
                    reason=f"APT playbook: {desc}",
                    command_preview=f"playbook_run {name}",
                )
            )
        return proposals


class KillchainGapSignal:
    """Detect missing steps in the kill chain from world model and session state.

    Inspects ``sessions/world_model.json`` host states and session artefacts
    to identify gaps where the operator has not progressed. Each detected gap
    produces a high-confidence :class:`Proposal` for the most impactful next
    action.

    Gap detection rules (ordered by priority):
        - Host in EXPLOITED state without privesc output: recommend
          linpeas/winpeas.
        - Host in OWNED state without credential dump: recommend
          mimikatz/secretsdump/lazydump.
        - Scan XML exists but no enumeration: recommend gobuster/ffuf/enum4linux.
        - Credentials exist but no lateral movement: recommend
          crackmapexec/psexec.
    """

    name = SOURCE_GAP

    def __init__(self, sessions_dir: str = "sessions") -> None:
        self._sessions_dir = Path(sessions_dir)

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return gap-detection proposals for ``ctx``."""
        proposals: list[Proposal] = []
        try:
            wm_data = _load_world_model(self._sessions_dir)
            if not wm_data:
                return proposals
            hosts: dict[str, dict] = wm_data.get("hosts", {})
            proposals.extend(self._gap_exploited_no_privesc(hosts))
            proposals.extend(self._gap_owned_no_creds(hosts, wm_data))
            proposals.extend(self._gap_scan_no_enum(hosts, ctx.recent_commands))
            proposals.extend(self._gap_creds_no_lateral(wm_data, hosts))
        except Exception:
            pass
        return proposals

    def _gap_exploited_no_privesc(self, hosts: dict[str, dict]) -> list[Proposal]:
        proposals: list[Proposal] = []
        for ip, host in hosts.items():
            if not isinstance(host, dict):
                continue
            if host.get("state") != "exploited":
                continue
            os_hint = host.get("os_hint", "").lower()
            if "windows" in os_hint:
                proposals.append(Proposal(
                    action="winpeas", kind=KIND_COMMAND, weight=_GAP_WEIGHT_PRIVESC,
                    reason=f"Host {ip} has foothold but no privesc. Run winpeas.",
                    category="privesc",
                ))
            elif "linux" in os_hint:
                proposals.append(Proposal(
                    action="linpeas", kind=KIND_COMMAND, weight=_GAP_WEIGHT_PRIVESC,
                    reason=f"Host {ip} has foothold but no privesc. Run linpeas.",
                    category="privesc",
                ))
            else:
                proposals.append(Proposal(
                    action="linpeas", kind=KIND_COMMAND, weight=_GAP_WEIGHT_PRIVESC_UNKNOWN_OS,
                    reason=f"Host {ip} has foothold but no privesc. Enumerate with linpeas/winpeas.",
                    category="privesc",
                ))
        return proposals

    def _gap_owned_no_creds(self, hosts: dict[str, dict], wm_data: dict) -> list[Proposal]:
        proposals: list[Proposal] = []
        owned_ips = [ip for ip, h in hosts.items()
                     if isinstance(h, dict) and h.get("state") == "owned"]
        if not owned_ips:
            return proposals
        credentials = wm_data.get("credentials", [])
        if credentials:
            return proposals
        for ip in owned_ips[:_GAP_OWNED_CRED_CAP]:
            proposals.append(Proposal(
                action="lazydump", kind=KIND_COMMAND, weight=_GAP_WEIGHT_CRED_DUMP,
                reason=f"Host {ip} is owned but no credentials dumped. Run lazydump.",
                category="cred",
            ))
        return proposals

    def _gap_scan_no_enum(self, hosts: dict[str, dict], recent: Sequence[str]) -> list[Proposal]:
        proposals: list[Proposal] = []
        run_set = set(recent) if recent else set()
        has_scan = any(
            isinstance(h, dict) and h.get("state") in ("scanned", "enumerated", "exploited", "owned")
            for h in hosts.values()
        )
        if not has_scan:
            return proposals
        if run_set & _ENUM_COMMANDS:
            return proposals
        proposals.append(Proposal(
            action="gobuster", kind=KIND_COMMAND, weight=_GAP_WEIGHT_ENUM,
            reason="Nmap scan exists but no enumeration done. Start with gobuster.",
            category="enum",
        ))
        return proposals

    def _gap_creds_no_lateral(self, wm_data: dict, hosts: dict[str, dict]) -> list[Proposal]:
        proposals: list[Proposal] = []
        credentials = wm_data.get("credentials", [])
        if not credentials:
            return proposals
        has_lateral = any(
            isinstance(h, dict) and h.get("state") == "owned"
            for ip, h in hosts.items()
            if ip not in (c.get("host", "") for c in credentials if isinstance(c, dict))
        )
        if has_lateral:
            return proposals
        proposals.append(Proposal(
            action="crackmapexec", kind=KIND_COMMAND, weight=_GAP_WEIGHT_LATERAL,
            reason="Credentials captured but no lateral movement. Test with crackmapexec.",
            category="lateral",
        ))
        return proposals


class GraphTopologySignal:
    """Adapt WorldModel network graph pivot_candidates into lateral movement proposals.

    Reads the degree-centrality pivot candidates computed by the WorldModel's
    NetworkGraph and emits high-confidence proposals for lateral movement,
    credential spraying, and network topology exploration — data that was
    previously computed but never consumed by the recommendation engine.
    """

    name = SOURCE_TOPOLOGY

    def __init__(self, sessions_dir: str = "sessions") -> None:
        self._sessions_dir = Path(sessions_dir)

    def propose(self, ctx: RecommendationContext) -> list[Proposal]:
        """Return lateral movement and topology proposals from network graph."""
        proposals: list[Proposal] = []
        try:
            wm_data = _load_world_model(self._sessions_dir)
            if not wm_data:
                return proposals

            candidates = wm_data.get("pivot_candidates", [])
            if not candidates:
                graph_data = wm_data.get("network_graph", {})
                if graph_data:
                    candidates = self._compute_centrality(graph_data)

            for index, candidate in enumerate(candidates[:ctx.limit]):
                node = candidate.get("node", "")
                centrality = candidate.get("centrality", 0.0)
                neighbors = candidate.get("neighbors", [])

                if "host:" in node:
                    target_ip = node.replace("host:", "")
                    proposals.append(Proposal(
                        action=f"crackmapexec smb {target_ip}",
                        kind=KIND_COMMAND,
                        weight=min(centrality * _TOPOLOGY_HOST_MULTIPLIER, 1.0),
                        reason=f"High-centrality pivot host {target_ip} (deg={centrality:.2f}, {len(neighbors)} neighbors)",
                        category="lateral",
                        command_preview=f"crackmapexec smb {target_ip}",
                    ))
                elif "cred:" in node:
                    cred_prefix = node.replace("cred:", "")
                    proposals.append(Proposal(
                        action="credential_spray",
                        kind=KIND_COMMAND,
                        weight=min(centrality * _TOPOLOGY_CRED_MULTIPLIER, 1.0),
                        reason=f"Credential {cred_prefix} authenticates to multiple hosts — spray",
                        category="lateral",
                    ))
                elif "service:" in node:
                    svc_name = node.replace("service:", "")
                    proposals.append(Proposal(
                        action=f"enum_{svc_name}",
                        kind=KIND_TOOL,
                        weight=min(centrality, 1.0),
                        reason=f"Service {svc_name} is a network hub (deg={centrality:.2f}) — enumerate for lateral paths",
                        category="enum",
                    ))
        except Exception:
            pass
        return proposals

    @staticmethod
    def _compute_centrality(graph_data: dict) -> list[dict]:
        nodes = set(graph_data.get("nodes", []))
        relations = graph_data.get("relations", [])
        if not nodes or len(nodes) <= 1:
            return []
        adjacency: dict[str, tuple[int, list[str]]] = {}
        for rel in relations:
            src = rel.get("source", "")
            tgt = rel.get("target", "")
            if src not in adjacency:
                adjacency[src] = (0, [])
            out_count, out_neighbors = adjacency[src]
            adjacency[src] = (out_count + 1, out_neighbors + [tgt])
            nodes.add(src)
            nodes.add(tgt)
        n = len(nodes)
        denominator = 2.0 * (n - 1)
        results: list[dict] = []
        for node in nodes:
            out_deg, out_nbrs = adjacency.get(node, (0, []))
            in_deg = sum(1 for r in relations if r.get("target") == node)
            centrality = round((in_deg + out_deg) / denominator, 4) if denominator > 0 else 0.0
            results.append({
                "node": node,
                "centrality": centrality,
                "out_degree": out_deg,
                "in_degree": in_deg,
                "neighbors": out_nbrs[:_TOPOLOGY_NEIGHBOR_CAP],
            })
        results.sort(key=lambda x: -x["centrality"])
        return results


def _try_build_playbook_signal() -> PlaybookSignal | None:
    """Build a :class:`PlaybookSignal` when the APT playbook engine imports."""
    try:
        from modules.apt_playbooks import AptPlaybookEngine
        return PlaybookSignal(AptPlaybookEngine())
    except Exception:
        return None


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

    signals.append(KillchainGapSignal(sessions_dir=sessions_dir))

    playbook_signal = _try_build_playbook_signal()
    if playbook_signal is not None:
        signals.append(playbook_signal)

    topology_signal = GraphTopologySignal(sessions_dir=sessions_dir)
    signals.append(topology_signal)

    signals.append(_build_killchain_signal())

    resolver = CategoryResolver(command_index_path)
    return RecommendationEngine(signals=signals, resolver=resolver, weights=weights)


def recommend_with_evidence(
    payload: Mapping[str, Any],
    sessions_dir: str = "sessions",
    target: str | None = None,
    phase: str = "",
    limit: int = 3,
    engine: RecommendationEngine | None = None,
) -> list[Recommendation]:
    """Return fused, ranked recommendations carrying reason and score for display.

    Thin convenience over :func:`build_default_engine` and :func:`build_context`
    for the evidence-backed inline hints. An already-built ``engine`` may be
    injected so a caller on a hot path (the post-command hook) constructs the
    engine once and reuses it across commands instead of rebuilding every step.

    Args:
        payload: ``payload.json`` mapping used to resolve OS and target.
        sessions_dir: Path to ``sessions/`` for transcript and world-model reads.
        target: Explicit target; falls back to ``payload['rhost']``.
        phase: Caller-resolved kill-chain phase. When non-empty it overrides the
            phase :func:`build_context` derives from the payload, letting the
            hint reuse the shell's authoritative :class:`modules.killchain.KillChain`
            resolution.
        limit: Maximum number of recommendations to return.
        engine: Optional pre-built engine to reuse.

    Returns:
        Up to ``limit`` :class:`cli.recommendation.Recommendation` objects,
        best first. Empty when no signal produces a proposal.
    """
    active_engine = engine or build_default_engine(payload=payload, sessions_dir=sessions_dir)
    ctx = build_context(payload=payload, sessions_dir=sessions_dir, target=target, limit=limit)
    if phase:
        ctx = replace(ctx, phase=phase)
    return active_engine.recommend(ctx)


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
    "PlaybookSignal",
    "GraphTopologySignal",
    "KillchainGapSignal",
    "SOURCE_GRAPH",
    "SOURCE_POLICY",
    "SOURCE_RECON",
    "SOURCE_KILLCHAIN",
    "SOURCE_GAP",
    "SOURCE_PLAYBOOK",
    "SOURCE_TOPOLOGY",
    "read_recent_commands",
    "build_context",
    "build_default_engine",
    "recommend_with_evidence",
]
