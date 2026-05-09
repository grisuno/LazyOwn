"""Behavioural telemetry derived from ``sessions/LazyOwn_session_report.csv``.

The CLI logs every executed command to a CSV file. This module reads that
artefact once per process and exposes a tiny read-only API so the palette CLI,
the C2 web overlay and the MCP detail view can all attach the same "how often
did this run" / "what runs after it" / "what did I just use" hints to a
detail entry without duplicating parsing logic.

Design constraints driving the shape of this module:

- Single Responsibility — :class:`TelemetryIndex` only loads and caches; pure
  functions like :func:`command_stats`, :func:`runs_after` and
  :func:`recents` translate it into palette-friendly shapes.
- Open/Closed — every threshold, field name and limit lives on
  :class:`TelemetryConfig`; new aggregations mean adding a function, not
  editing existing call sites.
- Dependency Inversion — every public entry point accepts the parsed
  telemetry index, never reads it from disk on its own. Callers wire the
  loader through :func:`load_telemetry` so tests can inject fixtures.
- Sad path is a no-op. A missing or malformed CSV degrades to an empty
  index so the palette stays usable on hosts that have never run a command.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TELEMETRY_PATH = REPO_ROOT / "sessions" / "LazyOwn_session_report.csv"


class TelemetryIndexError(RuntimeError):
    """Raised when the telemetry CSV is malformed in a way callers must see."""


@dataclass(frozen=True)
class TelemetryConfig:
    """Centralised constants for behavioural telemetry parsing.

    Every literal that affects telemetry derivation lives here so behaviour
    is tunable without touching call sites. ``frozen=True`` prevents
    accidental mutation by per-surface consumers.
    """

    do_command_prefix: str = "do_"
    csv_command_field: str = "command"
    csv_start_field: str = "start"
    cooccurrence_window: int = 3
    cooccurrence_min_count: int = 2
    cooccurrence_limit: int = 6
    recents_limit: int = 8
    excluded_commands: frozenset[str] = frozenset({"", "default", "exit", "EOF"})


@dataclass(frozen=True)
class CommandStat:
    """Aggregated invocation data for a single ``do_*`` command.

    Attributes:
        name: Canonical ``do_<verb>`` form so the value plugs straight into
            the command-index key space.
        runs: Total number of invocations seen in the CSV.
        last_seen: ISO timestamp of the most recent invocation, or the
            empty string when the CSV row carried no timestamp.
    """

    name: str
    runs: int
    last_seen: str


@dataclass(frozen=True)
class TelemetryIndex:
    """Read-only view derived from the session CSV.

    Attributes:
        stats_by_command: ``{do_<verb>: CommandStat}`` for every command
            seen in the CSV.
        recent_order: ``do_<verb>`` names in most-recent-first order, with
            duplicates collapsed. Truncated to
            :attr:`TelemetryConfig.recents_limit`.
        cooccurrence: ``{do_<verb>: ((do_<other>, count), ...)}`` listing
            commands that ran shortly after ``do_<verb>`` within the
            configured window, sorted by descending frequency.
    """

    stats_by_command: Mapping[str, CommandStat] = field(default_factory=dict)
    recent_order: tuple[str, ...] = field(default_factory=tuple)
    cooccurrence: Mapping[str, tuple[tuple[str, int], ...]] = field(default_factory=dict)


def _normalise_command(value: str | None, *, prefix: str) -> str:
    """Return the canonical ``do_<verb>`` form for a CSV ``command`` field."""
    if not isinstance(value, str):
        return ""
    raw = value.strip()
    if not raw:
        return ""
    return raw if raw.startswith(prefix) else f"{prefix}{raw}"


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Return the parsed rows of ``path``.

    A missing file returns an empty list so the loader stays best-effort.
    Rows lacking the ``command`` column are dropped silently.
    """
    if not path.exists():
        return []
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            reader = csv.DictReader(fh)
            return [dict(row) for row in reader if isinstance(row, dict)]
    except (OSError, csv.Error) as exc:
        raise TelemetryIndexError(f"Cannot read telemetry from {path}: {exc}") from exc


def _build_index(rows: Iterable[Mapping[str, str]], *, config: TelemetryConfig) -> TelemetryIndex:
    """Translate a list of CSV rows into :class:`TelemetryIndex`.

    The aggregation walks the rows once collecting:

    - per-command counters and last-seen timestamps,
    - the ordered list of invocations for recency and co-occurrence.

    Co-occurrence pairs ``A -> B`` are emitted whenever ``B`` appears within
    :attr:`TelemetryConfig.cooccurrence_window` rows after ``A``; pairs that
    do not reach :attr:`TelemetryConfig.cooccurrence_min_count` are dropped.
    """
    stats_runs: dict[str, int] = defaultdict(int)
    stats_last_seen: dict[str, str] = {}
    sequence: list[str] = []
    for row in rows:
        name = _normalise_command(row.get(config.csv_command_field), prefix=config.do_command_prefix)
        if not name or name in config.excluded_commands or name == config.do_command_prefix:
            continue
        if name[len(config.do_command_prefix) :] in config.excluded_commands:
            continue
        stats_runs[name] += 1
        timestamp = row.get(config.csv_start_field) or ""
        if isinstance(timestamp, str) and timestamp:
            stats_last_seen[name] = timestamp
        sequence.append(name)
    pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for idx, source in enumerate(sequence):
        upper = min(len(sequence), idx + 1 + config.cooccurrence_window)
        for follower in sequence[idx + 1 : upper]:
            if follower == source:
                continue
            pair_counts[(source, follower)] += 1
    cooccurrence: dict[str, tuple[tuple[str, int], ...]] = {}
    grouped: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for (source, follower), count in pair_counts.items():
        if count < config.cooccurrence_min_count:
            continue
        grouped[source].append((follower, count))
    for source, pairs in grouped.items():
        pairs.sort(key=lambda row: (-row[1], row[0]))
        cooccurrence[source] = tuple(pairs[: config.cooccurrence_limit])
    recent: list[str] = []
    seen: set[str] = set()
    for name in reversed(sequence):
        if name in seen:
            continue
        seen.add(name)
        recent.append(name)
        if len(recent) >= config.recents_limit:
            break
    stats_by_command = {
        name: CommandStat(name=name, runs=stats_runs[name], last_seen=stats_last_seen.get(name, ""))
        for name in stats_runs
    }
    return TelemetryIndex(
        stats_by_command=stats_by_command,
        recent_order=tuple(recent),
        cooccurrence=cooccurrence,
    )


@lru_cache(maxsize=4)
def load_telemetry(path: str | None = None) -> TelemetryIndex:
    """Return the parsed telemetry index, cached per resolved path.

    Args:
        path: Override the default CSV location. ``None`` uses
            :data:`DEFAULT_TELEMETRY_PATH`.

    Returns:
        A :class:`TelemetryIndex`. When the file is missing the function
        returns an empty index; callers that want to surface parse errors
        should catch :class:`TelemetryIndexError`.
    """
    target = Path(path) if path is not None else DEFAULT_TELEMETRY_PATH
    config = TelemetryConfig()
    rows = _read_csv_rows(target)
    return _build_index(rows, config=config)


def safe_load_telemetry(path: str | None = None) -> TelemetryIndex | None:
    """Best-effort variant of :func:`load_telemetry`.

    Returns ``None`` instead of raising so the palette stays usable on hosts
    where the CSV is malformed.
    """
    try:
        return load_telemetry(path)
    except TelemetryIndexError:
        return None


def command_stats(
    telemetry: TelemetryIndex | None,
    command_name: str,
    *,
    config: TelemetryConfig | None = None,
) -> CommandStat | None:
    """Return aggregated stats for ``command_name`` or ``None`` when unseen.

    Args:
        telemetry: The loaded telemetry index, or ``None`` for a no-op.
        command_name: A ``do_*`` command name with or without the ``do_``
            prefix.
        config: Optional override for the lookup config.
    """
    cfg = config or TelemetryConfig()
    if telemetry is None:
        return None
    name = _normalise_command(command_name, prefix=cfg.do_command_prefix)
    if not name:
        return None
    return telemetry.stats_by_command.get(name)


def runs_after(
    telemetry: TelemetryIndex | None,
    command_name: str,
    *,
    config: TelemetryConfig | None = None,
) -> list[str]:
    """Return commands that frequently run after ``command_name``.

    Sorted by descending frequency; ties broken alphabetically. The list is
    truncated to :attr:`TelemetryConfig.cooccurrence_limit` entries.
    """
    cfg = config or TelemetryConfig()
    if telemetry is None:
        return []
    name = _normalise_command(command_name, prefix=cfg.do_command_prefix)
    if not name:
        return []
    return [other for other, _count in telemetry.cooccurrence.get(name, ())]


def recents(
    telemetry: TelemetryIndex | None,
    *,
    config: TelemetryConfig | None = None,
) -> list[str]:
    """Return the most-recently invoked unique ``do_*`` commands.

    Order is most-recent-first; truncated to
    :attr:`TelemetryConfig.recents_limit` entries.
    """
    cfg = config or TelemetryConfig()
    if telemetry is None:
        return []
    return list(telemetry.recent_order[: cfg.recents_limit])


def enrich_detail(
    telemetry: TelemetryIndex | None,
    entry: Mapping[str, object] | None,
    *,
    config: TelemetryConfig | None = None,
) -> dict[str, object] | None:
    """Attach ``runs``, ``last_seen`` and ``runs_after`` to a detail entry.

    The returned dict is a shallow copy so the underlying command index is
    never mutated. ``None`` input passes through unchanged so callers can
    delegate the missing-target sad path to the renderer.
    """
    if entry is None:
        return None
    cfg = config or TelemetryConfig()
    name = str(entry.get("name", ""))
    enriched = dict(entry)
    stat = command_stats(telemetry, name, config=cfg)
    if stat is not None:
        enriched["runs"] = stat.runs
        enriched["last_seen"] = stat.last_seen
    enriched["runs_after"] = runs_after(telemetry, name, config=cfg)
    return enriched


def enrich_commands(
    telemetry: TelemetryIndex | None,
    rows: Iterable[Mapping[str, object]],
    *,
    config: TelemetryConfig | None = None,
) -> list[dict[str, object]]:
    """Enrich every entry of ``rows`` with telemetry data.

    Used by the C2 view and the Cmd+K overlay so the client-side renderer
    can show ``runs`` badges per row without round-tripping.
    """
    cfg = config or TelemetryConfig()
    out: list[dict[str, object]] = []
    for row in rows:
        enriched = enrich_detail(telemetry, row, config=cfg)
        out.append(enriched or {})
    return out


__all__ = [
    "CommandStat",
    "DEFAULT_TELEMETRY_PATH",
    "TelemetryConfig",
    "TelemetryIndex",
    "TelemetryIndexError",
    "command_stats",
    "enrich_commands",
    "enrich_detail",
    "load_telemetry",
    "recents",
    "runs_after",
    "safe_load_telemetry",
]
