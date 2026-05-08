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
    detail_value_unset: str = "(none)"
    name_column_min_width: int = 4
    summary_max_chars: int = 88
    summary_truncation_marker: str = "..."
    search_default_limit: int = 50
    search_minimum_limit: int = 1
    search_flag: str = "--search"
    info_flag: str = "--info"
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
        """Format the detail view for a single command entry."""
        cfg = self._config
        if entry is None:
            return cfg.detail_missing_message
        labels = (
            (cfg.detail_label_name, entry.get("name", cfg.detail_value_unset)),
            (cfg.detail_label_phase, entry.get("phase", cfg.detail_value_unset)),
            (cfg.detail_label_category, entry.get("category") or cfg.detail_value_unset),
            (
                cfg.detail_label_source,
                f"{entry.get('source_file', cfg.detail_value_unset)}:{entry.get('line', cfg.detail_value_unset)}",
            ),
            (cfg.detail_label_summary, entry.get("summary") or cfg.detail_value_unset),
        )
        width = max(cfg.name_column_min_width, max(len(label) for label, _ in labels))
        lines = [f"{label.ljust(width)}{cfg.column_separator}{value}" for label, value in labels]
        return cfg.line_separator.join(lines)

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
        rows = query.in_phase(args.phase or "")
        if args.query:
            needle = args.query.lower()
            rows = [r for r in rows if needle in r["name"].lower() or needle in (r.get("summary") or "").lower()]
        return renderer.render_phase(args.phase or "", rows)
    if args.mode is PaletteMode.SEARCH:
        rows = query.search(args.query or "", limit=cfg.search_default_limit)
        return renderer.render_search(args.query, rows)
    if args.mode is PaletteMode.DETAIL:
        return renderer.render_detail(query.detail(args.target_name or ""))
    return renderer.render_overview(query.phase_counts)


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
            candidates = [*query.phases, cfg.search_flag, cfg.info_flag]
            return self._filter_prefix(candidates, text)
        if position.index == 2 and position.tokens:
            head = position.tokens[0]
            if head == cfg.info_flag:
                names = [c["name"] for c in query.commands]
                return self._filter_prefix(sorted(names), text)
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
    "PaletteMode",
    "PaletteRenderConfig",
    "PaletteRenderer",
    "render",
]
