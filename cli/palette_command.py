"""Pure logic for the operator-facing ``palette`` command.

The CLI ``do_palette`` method on :class:`LazyOwnShell`, the C2 ``/palette``
endpoint and the MCP ``lazyown_palette`` tool all share the same parsing,
filtering and rendering pipeline implemented here. The module deliberately
exposes only deterministic, side-effect-free helpers that take a parsed
command index (a plain ``dict``) and return strings or structured rows, so
every consumer can render with its own colour scheme or transport.

Design constraints driving the shape of this module:

- Single Responsibility — three small classes split the work: argument
  parsing, query routing, output rendering.
- Open/Closed — adding a new render mode means adding a method to
  :class:`PaletteRenderer`; the dispatcher in :func:`render` does not have to
  change beyond a one-line entry.
- Dependency Inversion — every entry point accepts an ``index`` argument
  rather than reading the JSON from disk so callers can supply fixtures or
  alternate sources (in-memory builds, an MCP-cached snapshot, etc.).
- No magic values — every threshold, separator and label is a field of
  :class:`PaletteRenderConfig`, which the operator may override per call.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


class PaletteMode(Enum):
    """High-level routing modes for a parsed ``palette`` invocation."""

    OVERVIEW = "overview"
    PHASE = "phase"
    SEARCH = "search"
    DETAIL = "detail"
    NEXT = "next"


@dataclass(frozen=True)
class PaletteRenderConfig:
    """Centralised constants for parser, router and renderer.

    The defaults below are the only place where palette UX strings,
    separators and limits live. ``frozen=True`` prevents accidental mutation
    by surface-specific consumers; pass a fresh instance to override.
    """

    column_separator: str = "  "
    overview_header: str = "Command palette"
    overview_phase_header: str = "phase"
    overview_count_header: str = "commands"
    phase_header_prefix: str = "Phase: "
    phase_empty_message: str = "(no commands match)"
    search_header_prefix: str = "Search: "
    search_empty_message: str = "(no matches)"
    detail_missing_message: str = "Command not found."
    detail_label_name: str = "name"
    detail_label_phase: str = "phase"
    detail_label_category: str = "category"
    detail_label_source: str = "source"
    detail_label_summary: str = "summary"
    detail_label_calls: str = "calls"
    detail_label_related: str = "related"
    detail_label_runs: str = "runs"
    detail_label_last_seen: str = "last seen"
    detail_label_runs_after: str = "runs after"
    detail_value_unset: str = "(none)"
    detail_neighbour_separator: str = ", "
    detail_neighbour_max: int = 8
    next_header_prefix: str = "Next phase: "
    next_empty_message: str = "(no next phase configured)"
    next_unknown_phase_message: str = "Unknown phase."
    name_column_min_width: int = 4
    summary_max_chars: int = 88
    summary_truncation_marker: str = "..."
    search_default_limit: int = 50
    search_minimum_limit: int = 1
    search_flag: str = "--search"
    info_flag: str = "--info"
    next_flag: str = "--next"
    overview_phase_order: tuple[str, ...] = (
        "recon",
        "enum",
        "exploit",
        "postexp",
        "persist",
        "privesc",
        "cred",
        "lateral",
        "exfil",
        "c2",
        "report",
        "ai",
        "diagnostics",
        "plugin",
        "addon",
        "adversary",
        "misc",
        "uncategorized",
    )
    line_separator: str = "\n"

    def truncate_summary(self, summary: str | None) -> str:
        """Trim ``summary`` to :attr:`summary_max_chars` with marker suffix.

        Args:
            summary: The raw summary string from the command index.

        Returns:
            A safe single-line representation; empty string when ``summary``
            is falsy.
        """
        text = (summary or "").strip()
        if len(text) <= self.summary_max_chars:
            return text
        cutoff = max(0, self.summary_max_chars - len(self.summary_truncation_marker))
        return text[:cutoff] + self.summary_truncation_marker


@dataclass(frozen=True)
class PaletteArgs:
    """Parsed result of a single ``palette`` invocation."""

    mode: PaletteMode
    phase: str | None = None
    query: str | None = None
    target_name: str | None = None


class PaletteArgumentParser:
    """Translate a raw command line into :class:`PaletteArgs`.

    Routing rules (deterministic, in declaration order):

    1. No tokens: :attr:`PaletteMode.OVERVIEW`.
    2. ``--search <query>`` flag: :attr:`PaletteMode.SEARCH`.
    3. ``--info <name>`` flag: :attr:`PaletteMode.DETAIL`.
    4. Single token that matches a known phase: :attr:`PaletteMode.PHASE`.
    5. Single token that does not match a phase: :attr:`PaletteMode.SEARCH`
       with the token as ``query``.
    6. Two tokens with first matching a known phase: :attr:`PaletteMode.PHASE`
       with the second token as ``query``.
    7. Anything else: :attr:`PaletteMode.OVERVIEW` (the renderer falls back
       to a help-style listing).
    """

    def __init__(self, config: PaletteRenderConfig) -> None:
        self._config = config

    def parse(self, line: str, *, known_phases: Iterable[str]) -> PaletteArgs:
        """Return a :class:`PaletteArgs` for ``line``.

        Args:
            line: The raw text passed to ``do_palette`` (already stripped of
                the leading ``palette`` verb by cmd2).
            known_phases: Iterable of phase identifiers from the command
                index — used to disambiguate single-token invocations.
        """
        try:
            tokens = shlex.split(line or "")
        except ValueError:
            tokens = (line or "").split()
        phases = {p.strip().lower() for p in known_phases if isinstance(p, str)}
        if not tokens:
            return PaletteArgs(mode=PaletteMode.OVERVIEW)
        first = tokens[0]
        if first == self._config.search_flag:
            query = " ".join(tokens[1:]).strip()
            return PaletteArgs(mode=PaletteMode.SEARCH, query=query or None)
        if first == self._config.info_flag:
            name = tokens[1].strip() if len(tokens) >= 2 else ""
            return PaletteArgs(mode=PaletteMode.DETAIL, target_name=name or None)
        if first == self._config.next_flag:
            phase = tokens[1].strip().lower() if len(tokens) >= 2 else ""
            return PaletteArgs(mode=PaletteMode.NEXT, phase=phase or None)
        if first.lower() in phases:
            query = " ".join(tokens[1:]).strip() or None
            return PaletteArgs(mode=PaletteMode.PHASE, phase=first.lower(), query=query)
        return PaletteArgs(mode=PaletteMode.SEARCH, query=" ".join(tokens).strip() or None)


class PaletteIndexQuery:
    """Read-only view over the command index document.

    Wraps the JSON structure produced by ``scripts.build_command_index`` so
    callers do not depend on its concrete keys. Every method returns plain
    Python primitives (lists/dicts) — never references into the underlying
    document — so consumers can safely sort or extend the results.
    """

    def __init__(self, index: Mapping[str, Any]) -> None:
        self._index = index

    @property
    def commands(self) -> list[dict[str, Any]]:
        """Return canonical (non-duplicate) command entries."""
        rows = list(self._index.get("commands", []))
        return [row for row in rows if row.get("duplicate_of") is None]

    @property
    def phases(self) -> list[str]:
        """Return the sorted list of phase identifiers in the index."""
        return sorted(self._index.get("phase_to_commands", {}).keys())

    @property
    def phase_counts(self) -> dict[str, int]:
        """Return ``{phase: command_count}`` for every phase in the index."""
        rows = self._index.get("phase_to_commands", {})
        return {phase: len(set(names)) for phase, names in rows.items()}

    def in_phase(self, phase: str) -> list[dict[str, Any]]:
        """Return commands whose ``phase`` matches ``phase`` (case-insensitive)."""
        target = phase.strip().lower()
        return [c for c in self.commands if c.get("phase") == target]

    def search(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        """Substring search over ``name`` and ``summary`` (case-insensitive).

        Args:
            query: Free-form search term.
            limit: Maximum number of rows to return; values below 1 yield an
                empty list.
        """
        if limit < 1:
            return []
        needle = query.strip().lower()
        rows = sorted(self.commands, key=lambda c: c["name"])
        if needle:
            rows = [c for c in rows if needle in c["name"].lower() or needle in (c.get("summary") or "").lower()]
        return rows[:limit]

    def detail(self, target: str) -> dict[str, Any] | None:
        """Return the canonical entry for ``target`` or ``None``.

        Accepts both ``do_assign`` and ``assign`` forms.
        """
        normalised = target.strip()
        if not normalised:
            return None
        if not normalised.startswith("do_"):
            normalised = f"do_{normalised}"
        for row in self.commands:
            if row["name"] == normalised:
                return row
        return None

    def next_phase(self, current: str | None, *, ordering: Sequence[str]) -> str | None:
        """Return the phase that comes after ``current`` in ``ordering``.

        Args:
            current: Reference phase. ``None`` returns the first phase that
                is present in both ``ordering`` and the index.
            ordering: The kill-chain ordering — typically
                :attr:`PaletteRenderConfig.overview_phase_order`.

        Returns:
            The next phase identifier present in the index, or ``None`` when
            ``current`` is the final configured phase.
        """
        present = {phase for phase in self._index.get("phase_to_commands", {})}
        ordered = [phase for phase in ordering if phase in present]
        if not ordered:
            return None
        if current is None:
            return ordered[0]
        normalised = current.strip().lower()
        if normalised not in ordered:
            return None
        idx = ordered.index(normalised)
        if idx + 1 >= len(ordered):
            return None
        return ordered[idx + 1]


class PaletteRenderer:
    """Format query results as plain text, ready to be printed.

    Each ``render_*`` method takes already-filtered data and returns a
    multi-line string. The renderer never queries the index directly so the
    same instance can be reused across surfaces (CLI, web, MCP).
    """

    def __init__(self, config: PaletteRenderConfig) -> None:
        self._config = config

    def render_overview(self, phase_counts: Mapping[str, int]) -> str:
        """Format the multi-phase overview table."""
        cfg = self._config
        ordered = self._ordered_phases(phase_counts)
        if not ordered:
            return cfg.overview_header
        header = (cfg.overview_phase_header, cfg.overview_count_header)
        rows: list[tuple[str, str]] = [header]
        for phase in ordered:
            rows.append((phase, str(phase_counts[phase])))
        phase_width = max(cfg.name_column_min_width, max(len(r[0]) for r in rows))
        lines = [cfg.overview_header, ""]
        for label, count in rows:
            lines.append(f"{label.ljust(phase_width)}{cfg.column_separator}{count}")
        return cfg.line_separator.join(lines)

    def render_phase(self, phase: str, rows: Sequence[Mapping[str, Any]]) -> str:
        """Format a phase listing of ``(name, summary)`` pairs."""
        cfg = self._config
        header = f"{cfg.phase_header_prefix}{phase}"
        if not rows:
            return cfg.line_separator.join([header, cfg.phase_empty_message])
        return self._format_name_summary_table(header, rows)

    def render_search(self, query: str | None, rows: Sequence[Mapping[str, Any]]) -> str:
        """Format the cross-phase search result table."""
        cfg = self._config
        header = f"{cfg.search_header_prefix}{query or ''}".rstrip()
        if not rows:
            return cfg.line_separator.join([header, cfg.search_empty_message])
        return self._format_name_summary_table(header, rows)

    def render_detail(self, entry: Mapping[str, Any] | None) -> str:
        """Format the detail view for a single command entry.

        When ``entry`` carries graph-derived ``calls`` or ``related`` keys
        (attached by :func:`cli.palette_graph.enrich_detail`), those lists
        appear as additional rows so operators can see what the command
        actually invokes and which other commands work like it.
        """
        cfg = self._config
        if entry is None:
            return cfg.detail_missing_message
        labels: list[tuple[str, str]] = [
            (cfg.detail_label_name, entry.get("name", cfg.detail_value_unset)),
            (cfg.detail_label_phase, entry.get("phase", cfg.detail_value_unset)),
            (cfg.detail_label_category, entry.get("category") or cfg.detail_value_unset),
            (
                cfg.detail_label_source,
                f"{entry.get('source_file', cfg.detail_value_unset)}:{entry.get('line', cfg.detail_value_unset)}",
            ),
            (cfg.detail_label_summary, entry.get("summary") or cfg.detail_value_unset),
        ]
        calls = entry.get("calls")
        if calls:
            labels.append((cfg.detail_label_calls, self._format_neighbours(calls)))
        related = entry.get("related")
        if related:
            labels.append((cfg.detail_label_related, self._format_neighbours(related)))
        runs = entry.get("runs")
        if isinstance(runs, int) and runs > 0:
            labels.append((cfg.detail_label_runs, str(runs)))
            last_seen = entry.get("last_seen")
            if isinstance(last_seen, str) and last_seen:
                labels.append((cfg.detail_label_last_seen, last_seen))
        runs_after = entry.get("runs_after")
        if runs_after:
            labels.append((cfg.detail_label_runs_after, self._format_neighbours(runs_after)))
        width = max(cfg.name_column_min_width, max(len(label) for label, _ in labels))
        lines = [f"{label.ljust(width)}{cfg.column_separator}{value}" for label, value in labels]
        return cfg.line_separator.join(lines)

    def render_next(self, phase: str | None, rows: Sequence[Mapping[str, Any]]) -> str:
        """Format the recommended-next-phase listing."""
        cfg = self._config
        if phase is None:
            return cfg.next_empty_message
        header = f"{cfg.next_header_prefix}{phase}"
        if not rows:
            return cfg.line_separator.join([header, cfg.phase_empty_message])
        return self._format_name_summary_table(header, rows)

    def _format_neighbours(self, values: Sequence[str]) -> str:
        """Join graph-derived neighbour labels with the configured separator."""
        cfg = self._config
        trimmed = list(values)[: cfg.detail_neighbour_max]
        return cfg.detail_neighbour_separator.join(trimmed) if trimmed else cfg.detail_value_unset

    def _ordered_phases(self, phase_counts: Mapping[str, int]) -> list[str]:
        cfg = self._config
        present = set(phase_counts)
        ordered: list[str] = [p for p in cfg.overview_phase_order if p in present]
        ordered.extend(sorted(p for p in present if p not in cfg.overview_phase_order))
        return ordered

    def _format_name_summary_table(self, header: str, rows: Sequence[Mapping[str, Any]]) -> str:
        cfg = self._config
        names = [str(r.get("name", "")) for r in rows]
        summaries = [cfg.truncate_summary(r.get("summary")) for r in rows]
        name_width = max(cfg.name_column_min_width, max(len(n) for n in names))
        body = [f"{name.ljust(name_width)}{cfg.column_separator}{summary}" for name, summary in zip(names, summaries)]
        return cfg.line_separator.join([header, *body])


def _filter_phase_rows(rows: Sequence[Mapping[str, Any]], query: str | None) -> list[Mapping[str, Any]]:
    """Filter ``rows`` (already in a phase) by a free-text query.

    Args:
        rows: Command entries belonging to a single phase.
        query: Free-form term searched against ``name`` and ``summary``.
            ``None`` or empty returns ``rows`` unchanged.
    """
    if not query:
        return list(rows)
    needle = query.lower()
    return [row for row in rows if needle in row["name"].lower() or needle in (row.get("summary") or "").lower()]


def _enrich_detail_entry(entry: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    """Best-effort graph and telemetry enrichment for a single detail entry.

    Imports :mod:`cli.palette_graph` and :mod:`cli.palette_telemetry` lazily
    so the palette stays usable on hosts that have never run graphify or
    invoked any command yet — every missing artefact silently degrades to
    no enrichment without breaking the renderer contract.
    """
    if entry is None:
        return None
    enriched: Mapping[str, Any] = entry
    try:
        from cli.palette_graph import enrich_detail as graph_enrich
        from cli.palette_graph import safe_load_graph
    except Exception:
        graph_enrich = None  # type: ignore[assignment]
        safe_load_graph = None  # type: ignore[assignment]
    if graph_enrich is not None and safe_load_graph is not None:
        try:
            graph = safe_load_graph()
        except Exception:
            graph = None
        graph_result = graph_enrich(graph, enriched)
        if graph_result is not None:
            enriched = graph_result
    try:
        from cli.palette_telemetry import enrich_detail as telemetry_enrich
        from cli.palette_telemetry import safe_load_telemetry
    except Exception:
        return enriched
    try:
        telemetry = safe_load_telemetry()
    except Exception:
        telemetry = None
    telemetry_result = telemetry_enrich(telemetry, enriched)
    return telemetry_result if telemetry_result is not None else enriched


def render(
    index: Mapping[str, Any],
    line: str,
    *,
    config: PaletteRenderConfig | None = None,
) -> str:
    """Top-level entry point used by :class:`LazyOwnShell.do_palette`.

    Args:
        index: The parsed command-index document (already loaded).
        line: The raw text passed to ``do_palette``.
        config: Optional rendering configuration override. ``None`` uses the
            module default :class:`PaletteRenderConfig`.

    Returns:
        A ready-to-print multi-line string.
    """
    cfg = config or PaletteRenderConfig()
    query = PaletteIndexQuery(index)
    args = PaletteArgumentParser(cfg).parse(line, known_phases=query.phases)
    renderer = PaletteRenderer(cfg)
    if args.mode is PaletteMode.OVERVIEW:
        return renderer.render_overview(query.phase_counts)
    if args.mode is PaletteMode.PHASE:
        rows = _filter_phase_rows(query.in_phase(args.phase or ""), args.query)
        return renderer.render_phase(args.phase or "", rows)
    if args.mode is PaletteMode.SEARCH:
        rows = query.search(args.query or "", limit=cfg.search_default_limit)
        return renderer.render_search(args.query, rows)
    if args.mode is PaletteMode.DETAIL:
        entry = query.detail(args.target_name or "")
        return renderer.render_detail(_enrich_detail_entry(entry))
    if args.mode is PaletteMode.NEXT:
        next_phase = query.next_phase(args.phase, ordering=cfg.overview_phase_order)
        rows = query.in_phase(next_phase) if next_phase else []
        return renderer.render_next(next_phase, rows)
    return renderer.render_overview(query.phase_counts)


@dataclass(frozen=True)
class PaletteJsonResult:
    """Structured output of :class:`PaletteJsonRenderer` and :func:`render_json`.

    Consumers (the MCP tool, the C2 web client, automation scripts) read
    fields directly. The shape never includes raw helper text — only data —
    so each surface can localise or re-style without parsing strings.
    """

    mode: str
    phase: str | None = None
    query: str | None = None
    target: str | None = None
    results: tuple[Mapping[str, Any], ...] = field(default_factory=tuple)
    phase_counts: Mapping[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a plain ``dict`` suitable for ``json.dumps``."""
        return {
            "mode": self.mode,
            "phase": self.phase,
            "query": self.query,
            "target": self.target,
            "results": [dict(row) for row in self.results],
            "phase_counts": dict(self.phase_counts),
        }


class PaletteJsonRenderer:
    """Produce a :class:`PaletteJsonResult` from a parsed query.

    Mirrors :class:`PaletteRenderer` so adding a new ``PaletteMode`` requires
    one method here and one method on the text renderer; the dispatcher in
    :func:`render_json` does not have to change beyond a one-line entry.
    """

    def __init__(self, config: PaletteRenderConfig) -> None:
        self._config = config

    def render_overview(self, phase_counts: Mapping[str, int]) -> PaletteJsonResult:
        """Build a result document for overview mode."""
        return PaletteJsonResult(
            mode=PaletteMode.OVERVIEW.value,
            phase_counts=dict(phase_counts),
        )

    def render_phase(self, phase: str, query: str | None, rows: Sequence[Mapping[str, Any]]) -> PaletteJsonResult:
        """Build a result document for phase mode."""
        return PaletteJsonResult(
            mode=PaletteMode.PHASE.value,
            phase=phase,
            query=query,
            results=tuple(rows),
        )

    def render_search(self, query: str | None, rows: Sequence[Mapping[str, Any]]) -> PaletteJsonResult:
        """Build a result document for search mode."""
        return PaletteJsonResult(
            mode=PaletteMode.SEARCH.value,
            query=query,
            results=tuple(rows),
        )

    def render_detail(self, target: str | None, entry: Mapping[str, Any] | None) -> PaletteJsonResult:
        """Build a result document for detail mode."""
        return PaletteJsonResult(
            mode=PaletteMode.DETAIL.value,
            target=target,
            results=(entry,) if entry is not None else (),
        )

    def render_next(self, phase: str | None, rows: Sequence[Mapping[str, Any]]) -> PaletteJsonResult:
        """Build a result document for next-phase mode."""
        return PaletteJsonResult(
            mode=PaletteMode.NEXT.value,
            phase=phase,
            results=tuple(rows),
        )


def render_json(
    index: Mapping[str, Any],
    line: str,
    *,
    config: PaletteRenderConfig | None = None,
) -> dict[str, Any]:
    """Structured-data variant of :func:`render`.

    Args:
        index: The parsed command-index document.
        line: The raw text passed to the underlying surface.
        config: Optional configuration override.

    Returns:
        A serialisable ``dict`` matching :class:`PaletteJsonResult.to_dict`.
    """
    cfg = config or PaletteRenderConfig()
    query = PaletteIndexQuery(index)
    args = PaletteArgumentParser(cfg).parse(line, known_phases=query.phases)
    renderer = PaletteJsonRenderer(cfg)
    if args.mode is PaletteMode.OVERVIEW:
        return renderer.render_overview(query.phase_counts).to_dict()
    if args.mode is PaletteMode.PHASE:
        rows = _filter_phase_rows(query.in_phase(args.phase or ""), args.query)
        return renderer.render_phase(args.phase or "", args.query, rows).to_dict()
    if args.mode is PaletteMode.SEARCH:
        rows = query.search(args.query or "", limit=cfg.search_default_limit)
        return renderer.render_search(args.query, rows).to_dict()
    if args.mode is PaletteMode.DETAIL:
        entry = query.detail(args.target_name or "")
        return renderer.render_detail(args.target_name, _enrich_detail_entry(entry)).to_dict()
    if args.mode is PaletteMode.NEXT:
        next_phase = query.next_phase(args.phase, ordering=cfg.overview_phase_order)
        rows = query.in_phase(next_phase) if next_phase else []
        return renderer.render_next(next_phase, rows).to_dict()
    return renderer.render_overview(query.phase_counts).to_dict()


@dataclass(frozen=True)
class PaletteViewConfig:
    """Centralised constants for the C2 web view payload.

    Kept separate from :class:`PaletteRenderConfig` so a deployment may
    relabel the web UI without touching the CLI rendering strings.
    """

    page_title: str = "Command palette"
    page_subtitle: str = "Operator command catalogue"
    search_placeholder: str = "Search commands or summaries..."
    phase_filter_all_label: str = "All phases"
    empty_results_message: str = "No commands match the current filter."


def build_palette_view(
    index: Mapping[str, Any],
    *,
    config: PaletteRenderConfig | None = None,
    view_config: PaletteViewConfig | None = None,
) -> dict[str, Any]:
    """Assemble the template context consumed by the C2 ``/palette`` view.

    The shape is intentionally flat and JSON-serialisable so the template can
    embed the full payload as a ``<script type="application/json">`` block
    and the client-side JavaScript can filter without round-tripping.

    Args:
        index: The parsed command-index document.
        config: Optional rendering-config override (used to expose the flag
            strings the UI surfaces as filter chips).
        view_config: Optional view-config override.
    """
    cfg = config or PaletteRenderConfig()
    view = view_config or PaletteViewConfig()
    query = PaletteIndexQuery(index)
    commands = sorted(query.commands, key=lambda row: row["name"])
    enriched = _enrich_commands_for_view(commands)
    phase_counts = dict(query.phase_counts)
    phases = [
        {"id": phase, "label": phase, "count": phase_counts[phase]} for phase in _ordered_phase_ids(cfg, phase_counts)
    ]
    return {
        "page_title": view.page_title,
        "page_subtitle": view.page_subtitle,
        "search_placeholder": view.search_placeholder,
        "phase_filter_all_label": view.phase_filter_all_label,
        "empty_results_message": view.empty_results_message,
        "search_flag": cfg.search_flag,
        "info_flag": cfg.info_flag,
        "next_flag": cfg.next_flag,
        "phases": phases,
        "commands": enriched,
        "recents": _load_recent_commands(),
        "totals": {
            "commands": len(enriched),
            "phases": len(phases),
        },
    }


def _enrich_commands_for_view(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Best-effort graph and telemetry enrichment for a list of view rows.

    Behaves identically to :func:`_enrich_detail_entry` but in batch — and
    silently degrades to a copy of the input when graphify or telemetry data
    is absent so the C2 view never blocks on a missing artefact.
    """
    try:
        from cli.palette_graph import enrich_commands as graph_enrich_commands
        from cli.palette_graph import safe_load_graph
    except Exception:
        enriched: list[dict[str, Any]] = [dict(row) for row in rows]
    else:
        graph = safe_load_graph()
        enriched = graph_enrich_commands(graph, rows) if graph is not None else [dict(row) for row in rows]
    try:
        from cli.palette_telemetry import enrich_commands as telemetry_enrich_commands
        from cli.palette_telemetry import safe_load_telemetry
    except Exception:
        return enriched
    telemetry = safe_load_telemetry()
    return telemetry_enrich_commands(telemetry, enriched)


def _load_recent_commands() -> list[str]:
    """Return the most-recently invoked commands or an empty list on failure.

    Used by :func:`build_palette_view` to populate the Cmd+K overlay's
    "Recent" section without tying the function to the telemetry import.
    """
    try:
        from cli.palette_telemetry import recents, safe_load_telemetry
    except Exception:
        return []
    telemetry = safe_load_telemetry()
    if telemetry is None:
        return []
    return recents(telemetry)


def _ordered_phase_ids(config: PaletteRenderConfig, phase_counts: Mapping[str, int]) -> list[str]:
    """Return phase identifiers in display order honouring the config order."""
    present = set(phase_counts)
    ordered: list[str] = [p for p in config.overview_phase_order if p in present]
    ordered.extend(sorted(p for p in present if p not in config.overview_phase_order))
    return ordered


@dataclass(frozen=True)
class CompletionPosition:
    """Tokenisation snapshot produced by :class:`PaletteCompleter`."""

    index: int
    tokens: tuple[str, ...] = field(default_factory=tuple)


class PaletteCompleter:
    """Data-driven tab completion for ``palette``.

    Position rules:

    - First positional: phase identifiers and the verbs ``--search`` and
      ``--info``.
    - Second positional after a phase: command names belonging to that phase.
    - Second positional after ``--info``: every canonical command name.
    """

    def __init__(self, config: PaletteRenderConfig) -> None:
        self._config = config

    def complete(
        self,
        text: str,
        line: str,
        endidx: int,
        index: Mapping[str, Any],
    ) -> list[str]:
        """Return tab-completion candidates given the editor state."""
        cfg = self._config
        position = self._tokenise(line, endidx)
        query = PaletteIndexQuery(index)
        if position.index == 1:
            candidates = [*query.phases, cfg.search_flag, cfg.info_flag, cfg.next_flag]
            return self._filter_prefix(candidates, text)
        if position.index == 2 and position.tokens:
            head = position.tokens[0]
            if head == cfg.info_flag:
                names = [c["name"] for c in query.commands]
                return self._filter_prefix(sorted(names), text)
            if head == cfg.next_flag:
                return self._filter_prefix(query.phases, text)
            if head.lower() in {p.lower() for p in query.phases}:
                names = [c["name"] for c in query.in_phase(head)]
                return self._filter_prefix(sorted(names), text)
        return []

    def _tokenise(self, line: str, endidx: int) -> CompletionPosition:
        prefix = line[:endidx]
        try:
            tokens = tuple(shlex.split(prefix)) if prefix else tuple()
        except ValueError:
            tokens = tuple(prefix.split())
        index = len(tokens) - (0 if prefix.endswith(" ") else 1)
        if tokens and tokens[0] == "palette":
            tokens = tokens[1:]
            index = max(0, index - 1)
        return CompletionPosition(index=index + 1, tokens=tokens)

    @staticmethod
    def _filter_prefix(candidates: Iterable[str], text: str) -> list[str]:
        prefix = text or ""
        return sorted({c for c in candidates if c.startswith(prefix)})


__all__ = [
    "CompletionPosition",
    "PaletteArgs",
    "PaletteArgumentParser",
    "PaletteCompleter",
    "PaletteIndexQuery",
    "PaletteJsonRenderer",
    "PaletteJsonResult",
    "PaletteMode",
    "PaletteRenderConfig",
    "PaletteRenderer",
    "PaletteViewConfig",
    "build_palette_view",
    "render",
    "render_json",
]
