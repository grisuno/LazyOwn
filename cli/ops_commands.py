"""Power-user operator commands: ctx, tgrep, phase, note, l00t, pivot, tasks, sitrep, scans.

All functions are pure (no side effects beyond filesystem reads/writes) and
have no imports from lazyown.py or lazyc2.py so they can be unit-tested in
isolation and reused from MCP tools.
"""

from __future__ import annotations

import csv
import datetime
import glob
import json
import os
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.text import Text

_console = Console(highlight=False, soft_wrap=True)

PHASES: tuple[str, ...] = ("recon", "scan", "enum", "exploit", "privesc", "lateral", "exfil", "report")

_PHASE_COLORS: dict[str, str] = {
    "recon": "cyan",
    "scan": "blue",
    "enum": "magenta",
    "exploit": "bold red",
    "privesc": "bold yellow",
    "lateral": "orange3",
    "exfil": "dark_orange",
    "report": "green",
}

_WORLD_MODEL = "sessions/world_model.json"
_SESSION_CSV = "sessions/LazyOwn_session_report.csv"
_TRANSCRIPT_JSONL = "sessions/_cli_transcript.jsonl"
_LOGS_DIR = "sessions/logs"
_CRED_GLOB = "sessions/credentials*.txt"
_HASH_GLOB = "sessions/hash*.txt"

_WORLD_MODEL_NAME = "world_model.json"
_SESSION_CSV_NAME = "LazyOwn_session_report.csv"
_OS_FILE_NAME = "os.json"
_PIVOT_FILE_NAME = "pivots.jsonl"

_LOOT_USER_MAX = 40
_LOOT_SECRET_MAX = 60

_CRED_REL_HARVESTED = "exposes_credential"
_CRED_REL_WORKED = "authenticates_to"
_CRED_REL_REJECTED = "rejected_by"
_CRED_REL_CANDIDATE = "may_authenticate_to"
_CRED_NODE_PREFIX = "cred:"
_HOST_NODE_PREFIX = "host:"
_CRED_NODE_HASH_LEN = 12

_HOST_STATE_RANK = {
    "unscanned": 0,
    "scanned": 1,
    "enumerated": 2,
    "exploited": 3,
    "owned": 4,
}

_PROGRESS_BAR_WIDTH = 10
_RECON_HOST_WEIGHT = 0.5
_RECON_OS_WEIGHT = 0.5
_ENUM_SERVICE_FLOOR = 0.25
_REPORT_GLOBS = ("report_*.md", "report_*.docx")


# ── ctx ─────────────────────────────────────────────────────────────────────


def print_ctx(payload: dict[str, Any], sessions_dir: str = "sessions") -> None:
    """Print a single-line operator context summary.

    Args:
        payload: Live params dict.
        sessions_dir: Path to sessions directory.
    """
    world = _read_json(_WORLD_MODEL)
    rhost = payload.get("rhost") or "—"
    lhost = payload.get("lhost") or "—"
    domain = payload.get("domain") or "—"
    os_id = str(payload.get("os_id", "?"))
    os_label = {"1": "Linux", "2": "Win"}.get(os_id, "?")
    phase = (world.get("phase") or world.get("current_phase") or "unknown").lower()
    phase_color = _PHASE_COLORS.get(phase, "white")
    creds = _count_glob(_CRED_GLOB)
    hashes = _count_glob(_HASH_GLOB)

    t = Text()
    t.append(" rhost ", style="bold white on dark_red")
    t.append(f" {rhost} ")
    t.append(" lhost ", style="bold white on dark_green")
    t.append(f" {lhost} ")
    t.append(" domain ", style="bold white on dark_blue")
    t.append(f" {domain} ")
    t.append(" phase ", style="bold white on grey23")
    t.append(f" {phase.upper()} ", style=f"bold {phase_color}")
    t.append(" os ", style="dim white")
    t.append(f" {os_label} ")
    if creds:
        t.append(" creds ", style="bold white on dark_green")
        t.append(f" {creds} ")
    if hashes:
        t.append(" hashes ", style="bold white on dark_red")
        t.append(f" {hashes} ")
    _console.print(t)


# ── tgrep ────────────────────────────────────────────────────────────────────


def tgrep(
    pattern: str,
    *,
    sessions_dir: str = "sessions",
    limit: int = 40,
    case_insensitive: bool = True,
) -> None:
    """Search past command outputs and session logs for ``pattern``.

    Searches in order:
      1. ``sessions/_cli_transcript.jsonl`` (in-memory transcript with full output)
      2. ``sessions/LazyOwn_session_report.csv`` (command column)
      3. ``sessions/logs/`` text files

    Args:
        pattern: Regular expression or plain string to search for.
        sessions_dir: Base sessions directory.
        limit: Maximum total hits to display.
        case_insensitive: Case-insensitive matching when True.
    """
    if not pattern:
        _console.print("[bold red]  tgrep: pattern required[/]")
        return

    flags = re.IGNORECASE if case_insensitive else 0
    try:
        rx = re.compile(pattern, flags)
    except re.error as exc:
        _console.print(f"[bold red]  tgrep: invalid pattern — {exc}[/]")
        return

    hits: list[dict[str, str]] = []

    _search_transcript_jsonl(rx, hits, limit)
    if len(hits) < limit:
        _search_csv(rx, hits, limit)
    if len(hits) < limit:
        _search_logs(rx, hits, limit, sessions_dir)

    if not hits:
        _console.print(f"[dim]  tgrep: no matches for [bold]{pattern}[/][/]")
        return

    table = Table(
        title=f"tgrep: {pattern!r} — {len(hits)} hit(s)",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("Source", style="dim cyan", no_wrap=True, max_width=18)
    table.add_column("Context", style="dim white", no_wrap=True, max_width=20)
    table.add_column("Match", no_wrap=False)

    for hit in hits[:limit]:
        src = hit.get("source", "")
        ctx = hit.get("context", "")
        line = _highlight_match(hit.get("line", ""), rx)
        table.add_row(src, ctx[:20], line)

    _console.print(table)


def _search_transcript_jsonl(
    rx: re.Pattern,
    hits: list[dict[str, str]],
    limit: int,
) -> None:
    path = Path(_TRANSCRIPT_JSONL)
    if not path.exists():
        return
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return
    for raw in reversed(lines):
        if len(hits) >= limit:
            break
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            continue
        cmd = entry.get("command", "")
        output = entry.get("output", "")
        for text_line in (output or "").splitlines():
            if len(hits) >= limit:
                break
            if rx.search(text_line):
                hits.append(
                    {
                        "source": "transcript",
                        "context": cmd[:20],
                        "line": text_line.strip()[:120],
                    }
                )


def _search_csv(rx: re.Pattern, hits: list[dict[str, str]], limit: int) -> None:
    path = Path(_SESSION_CSV)
    if not path.exists():
        return
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
    except (OSError, csv.Error):
        return
    for row in reversed(rows):
        if len(hits) >= limit:
            break
        for col, val in row.items():
            if val and rx.search(val):
                hits.append(
                    {
                        "source": "session.csv",
                        "context": col,
                        "line": str(val).strip()[:120],
                    }
                )
                break


def _search_logs(
    rx: re.Pattern,
    hits: list[dict[str, str]],
    limit: int,
    sessions_dir: str,
) -> None:
    logs_dir = Path(sessions_dir) / "logs"
    if not logs_dir.is_dir():
        return
    for fpath in sorted(logs_dir.rglob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True):
        if len(hits) >= limit:
            break
        try:
            content = fpath.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in content.splitlines():
            if len(hits) >= limit:
                break
            if rx.search(line):
                hits.append(
                    {
                        "source": fpath.name[:18],
                        "context": "",
                        "line": line.strip()[:120],
                    }
                )


def _highlight_match(line: str, rx: re.Pattern) -> Text:
    t = Text()
    last = 0
    for m in rx.finditer(line):
        t.append(line[last : m.start()])
        t.append(line[m.start() : m.end()], style="bold yellow on dark_goldenrod")
        last = m.end()
    t.append(line[last:])
    return t


# ── phase ────────────────────────────────────────────────────────────────────


def read_phase() -> str:
    """Return the current kill-chain phase from world_model.json."""
    world = _read_json(_WORLD_MODEL)
    return (world.get("phase") or world.get("current_phase") or "unknown").lower()


def write_phase(phase: str) -> bool:
    """Set the current kill-chain phase in world_model.json.

    Args:
        phase: One of the PHASES values.

    Returns:
        True on success, False if the phase name is invalid.
    """
    if phase not in PHASES:
        return False
    world = _read_json(_WORLD_MODEL)
    old_phase = (world.get("phase") or world.get("current_phase") or "").lower()
    world["phase"] = phase
    world["current_phase"] = phase

    completed: list[str] = world.get("completed_phases") or []
    if old_phase and old_phase in PHASES and old_phase not in completed:
        old_idx = PHASES.index(old_phase)
        new_idx = PHASES.index(phase)
        if new_idx > old_idx:
            for p in PHASES[old_idx:new_idx]:
                if p not in completed:
                    completed.append(p)
    world["completed_phases"] = completed

    _write_json_atomic(_WORLD_MODEL, world)
    return True


def print_phase() -> None:
    """Print the current phase and the full kill-chain progress bar."""
    current = read_phase()
    world = _read_json(_WORLD_MODEL)
    completed: list[str] = world.get("completed_phases") or []

    t = Text()
    t.append("  Kill chain: ", style="dim white")
    for i, phase in enumerate(PHASES):
        if phase in completed:
            style = "bold green"
            icon = "✔"
        elif phase == current:
            style = f"bold {_PHASE_COLORS.get(phase, 'white')}"
            icon = "▶"
        else:
            style = "dim white"
            icon = "○"
        t.append(f"{icon}{phase}", style=style)
        if i < len(PHASES) - 1:
            t.append("  ", style="dim")
    _console.print(t)
    _console.print(
        f"  Current phase: [bold {_PHASE_COLORS.get(current, 'white')}]{current.upper()}[/]"
        f"  — dashboard refreshes in up to {5}s"
    )

    progress = phase_progress(world)
    for phase in PHASES:
        ratio = progress.get(phase, 0.0)
        color = _PHASE_COLORS.get(phase, "white")
        bar = _render_progress_bar(ratio)
        _console.print(f"  [bold {color}]{phase:<8}[/] [{color}]{bar}[/] [dim]{int(round(ratio * 100)):3d}%[/]")


def _render_progress_bar(ratio: float) -> str:
    """Return a fixed-width filled/empty block bar for ``ratio`` in [0, 1]."""
    clamped = max(0.0, min(1.0, ratio))
    filled = int(round(clamped * _PROGRESS_BAR_WIDTH))
    return "█" * filled + "░" * (_PROGRESS_BAR_WIDTH - filled)


def _os_identified(sessions_dir: str) -> bool:
    """Return True when sessions/os.json records an active OS fingerprint."""
    data = _read_json(str(Path(sessions_dir) / _OS_FILE_NAME))
    if isinstance(data, list):
        return bool(data) and data[0].get("state") == "active"
    return False


def _glob_count(sessions_dir: str, pattern: str) -> int:
    """Return the number of files under ``sessions_dir`` matching ``pattern``."""
    return len(glob.glob(str(Path(sessions_dir) / pattern)))


def _report_artifact_exists(sessions_dir: str) -> bool:
    """Return True when a generated report (report_*.md/.docx) is present."""
    return any(_glob_count(sessions_dir, pattern) for pattern in _REPORT_GLOBS)


def _count_pivots(sessions_dir: str) -> int:
    """Return the number of recorded pivot entries."""
    path = Path(sessions_dir) / _PIVOT_FILE_NAME
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())


def phase_progress(world: dict[str, Any], sessions_dir: str = "sessions") -> dict[str, float]:
    """Estimate per-phase completion in [0, 1] from world-model state.

    Signals are data-driven: host state ranks, nmap scan files, discovered
    services, captured loot, recorded pivots, and report artefacts. Any phase
    listed in ``completed_phases`` is forced to 1.0.

    Args:
        world: Parsed world_model.json document.
        sessions_dir: Base sessions directory for filesystem signals.

    Returns:
        A mapping of each :data:`PHASES` value to a completion ratio.
    """
    hosts = world.get("hosts", {}) or {}
    ranks = [_HOST_STATE_RANK.get((h.get("state") or "unscanned"), 0) for h in hosts.values()]
    n_hosts = len(ranks)
    n_services = sum(len(h.get("services", {}) or {}) for h in hosts.values())
    n_loot = _glob_count(sessions_dir, "credentials*.txt") + _glob_count(sessions_dir, "hash*.txt")
    n_owned = sum(1 for r in ranks if r >= _HOST_STATE_RANK["owned"])
    n_pivots = _count_pivots(sessions_dir)
    has_scan_files = _glob_count(sessions_dir, "scan_*.nmap") > 0

    def frac_at_least(min_rank: int) -> float:
        if n_hosts == 0:
            return 0.0
        return sum(1 for r in ranks if r >= min_rank) / n_hosts

    recon = (_RECON_HOST_WEIGHT if n_hosts else 0.0) + (_RECON_OS_WEIGHT if _os_identified(sessions_dir) else 0.0)
    scan = frac_at_least(_HOST_STATE_RANK["scanned"]) if n_hosts else (0.5 if has_scan_files else 0.0)
    enum = max(frac_at_least(_HOST_STATE_RANK["enumerated"]), _ENUM_SERVICE_FLOOR if n_services else 0.0)
    exploit = frac_at_least(_HOST_STATE_RANK["exploited"])
    privesc = frac_at_least(_HOST_STATE_RANK["owned"])
    lateral = (
        0.0 if n_owned == 0 else min(1.0, n_pivots / max(n_hosts - 1, 1)) if n_hosts > 1 else (1.0 if n_pivots else 0.0)
    )
    exfil = 1.0 if n_loot else 0.0
    report = 1.0 if _report_artifact_exists(sessions_dir) else 0.0

    progress = {
        "recon": recon,
        "scan": scan,
        "enum": enum,
        "exploit": exploit,
        "privesc": privesc,
        "lateral": lateral,
        "exfil": exfil,
        "report": report,
    }

    for phase in world.get("completed_phases") or []:
        if phase in progress:
            progress[phase] = 1.0

    return {phase: round(progress.get(phase, 0.0), 4) for phase in PHASES}


# ── shared helpers ────────────────────────────────────────────────────────────


def _read_json(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def _write_json_atomic(path: str, data: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(dir=str(target.parent), suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, default=str)
        os.chmod(tmp_path, 0o600)
        os.rename(tmp_path, str(target))
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _count_glob(pattern: str) -> int:
    import glob as _glob

    total = 0
    for fpath in _glob.glob(pattern):
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                total += sum(1 for line in fh if line.strip())
        except OSError:
            pass
    return total


# ── note ─────────────────────────────────────────────────────────────────────

_NOTES_FILE = "sessions/notes.jsonl"


def note_add(text: str, rhost: str = "", phase: str = "") -> None:
    """Append a timestamped operator note to sessions/notes.jsonl.

    Args:
        text: Free-form note text.
        rhost: Current target IP (attached as context).
        phase: Current kill-chain phase (attached as context).
    """
    entry = {
        "ts": time.time(),
        "rhost": rhost or "",
        "phase": phase or read_phase(),
        "text": text.strip(),
    }
    path = Path(_NOTES_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    _console.print(
        f"  [bold green]note saved[/]  [{entry['phase'].upper()}] "
        f"[dim]{entry['rhost'] or 'no target'}[/]  {text.strip()[:80]}"
    )


def note_list(rhost: str = "", limit: int = 20) -> None:
    """Print recent operator notes, optionally filtered by rhost.

    Args:
        rhost: When non-empty, only show notes for this target.
        limit: Maximum number of notes to display.
    """
    path = Path(_NOTES_FILE)
    if not path.exists():
        _console.print("  [dim]No notes yet.  Use: note <text>[/]")
        return

    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    entries = []
    for raw in lines:
        try:
            entries.append(json.loads(raw))
        except json.JSONDecodeError:
            continue

    if rhost:
        entries = [e for e in entries if e.get("rhost") == rhost]

    if not entries:
        _console.print(f"  [dim]No notes{' for ' + rhost if rhost else ''}.[/]")
        return

    table = Table(
        title=f"Operator notes{' — ' + rhost if rhost else ''}",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Phase", style="bold yellow", width=10)
    table.add_column("Target", style="cyan", width=16)
    table.add_column("Note", no_wrap=False)

    for _i, entry in enumerate(entries[-limit:], 1):
        ts_str = datetime.datetime.fromtimestamp(entry.get("ts", 0)).strftime("%H:%M")
        phase = (entry.get("phase") or "?").upper()
        target = entry.get("rhost") or "—"
        text = entry.get("text") or ""
        table.add_row(f"{ts_str}", phase, target, text)

    _console.print(table)


# ── loot ──────────────────────────────────────────────────────────────────────


@dataclass
class LootEntry:
    """A single captured credential or hash parsed from a loot file.

    Attributes:
        source: Basename of the file the entry was read from.
        kind: ``cleartext`` for credentials*.txt, ``hash`` for hash*.txt.
        user: Username portion (text before the first colon), full length.
        secret: Password or hash portion (text after the first colon).
    """

    source: str
    kind: str
    user: str
    secret: str

    @property
    def value(self) -> str:
        """Return the canonical ``user:secret`` credential value.

        Returns:
            ``user:secret`` when a secret is present, otherwise just ``user``.
            Matches the value format stored by ``modules.world_model``.
        """
        return f"{self.user}:{self.secret}" if self.secret else self.user


def gather_loot(sessions_dir: str = "sessions") -> list[LootEntry]:
    """Parse every credentials*.txt and hash*.txt under ``sessions_dir``.

    Each file is expected to hold one ``user:secret`` entry per line; blank
    lines and ``#`` comments are skipped. This is the single source of truth
    for loot parsing reused by show / search / reuse / mark.

    Args:
        sessions_dir: Base sessions directory.

    Returns:
        A list of :class:`LootEntry` in file then line order.
    """
    entries: list[LootEntry] = []
    for pattern, kind in (
        (f"{sessions_dir}/credentials*.txt", "cleartext"),
        (f"{sessions_dir}/hash*.txt", "hash"),
    ):
        for fpath in sorted(glob.glob(pattern)):
            fname = Path(fpath).name
            try:
                content = Path(fpath).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for raw_line in content.splitlines():
                stripped = raw_line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if ":" in stripped:
                    user, _, secret = stripped.partition(":")
                else:
                    user, secret = stripped, ""
                entries.append(
                    LootEntry(
                        source=fname,
                        kind=kind,
                        user=user.strip(),
                        secret=secret.strip(),
                    )
                )
    return entries


def loot_show(sessions_dir: str = "sessions") -> None:
    """Print a unified table of all captured credentials and hashes.

    Args:
        sessions_dir: Base sessions directory.
    """
    entries = gather_loot(sessions_dir)
    if not entries:
        _console.print("  [dim]No l00t yet.  Credentials land in sessions/credentials*.txt[/]")
        return

    table = Table(
        title=f"Loot — {len(entries)} credential(s)",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("Source", style="dim cyan", no_wrap=True, max_width=24)
    table.add_column("Type", style="dim", width=10)
    table.add_column("User", style="bold white", no_wrap=True, max_width=30)
    table.add_column("Secret / Hash", no_wrap=False)

    seen: set[tuple[str, str]] = set()
    for entry in entries:
        user = entry.user[:_LOOT_USER_MAX]
        secret = entry.secret[:_LOOT_SECRET_MAX]
        key = (user, secret)
        dup_style = "dim" if key in seen else ""
        seen.add(key)
        secret_cell = Text(secret)
        secret_cell.stylize("bold green" if entry.kind == "cleartext" else "bold red")
        if dup_style:
            secret_cell.stylize("dim")
        table.add_row(
            Text(entry.source, style=f"dim cyan {dup_style}"),
            Text(entry.kind, style=f"dim {dup_style}"),
            Text(user, style=f"bold white {dup_style}"),
            secret_cell,
        )

    _console.print(table)


def _loot_provenance(query: str, sessions_dir: str) -> dict[str, str] | None:
    """Find the first session-log row that mentions ``query``.

    Args:
        query: Case-insensitive needle to search the command CSV for.
        sessions_dir: Base sessions directory.

    Returns:
        ``{"command": ..., "ts": ...}`` for the first matching row, or
        ``None`` when the CSV is absent or holds no match.
    """
    csv_path = Path(sessions_dir) / _SESSION_CSV_NAME
    if not csv_path.exists():
        return None
    needle = query.lower()
    try:
        with csv_path.open("r", encoding="utf-8", errors="ignore") as fh:
            for row in csv.DictReader(fh):
                blob = " ".join(str(v) for v in row.values() if v).lower()
                if needle in blob:
                    return {
                        "command": row.get("command") or row.get("cmd") or "",
                        "ts": row.get("timestamp") or row.get("ts") or "",
                    }
    except (OSError, csv.Error):
        return None
    return None


def loot_search(query: str, sessions_dir: str = "sessions") -> None:
    """Search captured loot for ``query`` across users and secrets.

    Args:
        query: Case-insensitive substring matched against user and secret.
        sessions_dir: Base sessions directory.
    """
    if not query.strip():
        _console.print("  [bold red]loot search: query required[/]  — l00t search <user|host|hash>")
        return

    needle = query.strip().lower()
    entries = gather_loot(sessions_dir)
    hits = [e for e in entries if needle in e.user.lower() or needle in e.secret.lower()]

    if not hits:
        _console.print(f"  [dim]loot search: no credentials match [bold]{query}[/][/]")
        return

    table = Table(
        title=f"Loot search: {query!r} — {len(hits)} hit(s)",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("Source", style="dim cyan", no_wrap=True, max_width=24)
    table.add_column("Type", style="dim", width=10)
    table.add_column("User", style="bold white", no_wrap=True, max_width=30)
    table.add_column("Secret / Hash", no_wrap=False)

    for entry in hits:
        secret_cell = Text(entry.secret[:_LOOT_SECRET_MAX])
        secret_cell.stylize("bold green" if entry.kind == "cleartext" else "bold red")
        table.add_row(entry.source, entry.kind, entry.user[:_LOOT_USER_MAX], secret_cell)

    _console.print(table)

    prov = _loot_provenance(query, sessions_dir)
    if prov and (prov["command"] or prov["ts"]):
        _console.print(
            f"  [dim]first seen in log:[/] [cyan]{prov['command'][:80]}[/]"
            + (f"  [dim]{prov['ts']}[/]" if prov["ts"] else "")
        )


def _cred_outcomes_for_host(world: dict[str, Any], host: str) -> tuple[set[str], set[str]]:
    """Return cred-node prefixes that worked / were rejected for ``host``.

    Args:
        world: Parsed world_model.json document.
        host: Target host IP.

    Returns:
        ``(worked, rejected)`` sets of ``cred:<hash>`` node identifiers that
        the network graph records as authenticating to / rejected by ``host``.
    """
    worked: set[str] = set()
    rejected: set[str] = set()
    host_node = f"{_HOST_NODE_PREFIX}{host}"
    for rel in world.get("network_graph", {}).get("relations", []):
        if rel.get("target") != host_node:
            continue
        src = rel.get("source", "")
        if not src.startswith(_CRED_NODE_PREFIX):
            continue
        if rel.get("relation") == _CRED_REL_WORKED:
            worked.add(src)
        elif rel.get("relation") == _CRED_REL_REJECTED:
            rejected.add(src)
    return worked, rejected


def _cred_node(value: str) -> str:
    """Return the network-graph node id for a credential value."""
    return f"{_CRED_NODE_PREFIX}{value[:_CRED_NODE_HASH_LEN]}"


def loot_reuse(rhost: str, sessions_dir: str = "sessions") -> None:
    """Suggest captured credentials worth trying against ``rhost``.

    Ranks credentials that have not yet been rejected by the target, favouring
    cleartext over hashes and credentials already confirmed elsewhere, and
    prints ready-to-run authentication hints.

    Args:
        rhost: Current target IP (from payload ``rhost``).
        sessions_dir: Base sessions directory.
    """
    if not rhost.strip():
        _console.print("  [bold red]loot reuse: no target[/]  — set one with [bold]assign rhost <ip>[/]")
        return

    entries = gather_loot(sessions_dir)
    if not entries:
        _console.print("  [dim]No l00t to reuse.  Credentials land in sessions/credentials*.txt[/]")
        return

    world = _read_json(str(Path(sessions_dir) / _WORLD_MODEL_NAME))
    worked_here, rejected_here = _cred_outcomes_for_host(world, rhost)

    worked_anywhere: set[str] = set()
    for rel in world.get("network_graph", {}).get("relations", []):
        if rel.get("relation") == _CRED_REL_WORKED and rel.get("source", "").startswith(_CRED_NODE_PREFIX):
            worked_anywhere.add(rel["source"])

    ranked: list[tuple[float, LootEntry, str]] = []
    seen_values: set[str] = set()
    for entry in entries:
        if entry.value in seen_values:
            continue
        seen_values.add(entry.value)
        node = _cred_node(entry.value)
        if node in rejected_here:
            continue
        status = ""
        score = 1.0 if entry.kind == "cleartext" else 0.5
        if node in worked_here:
            status = "already works here"
            score += 2.0
        elif node in worked_anywhere:
            status = "confirmed elsewhere"
            score += 1.0
        ranked.append((score, entry, status))

    if not ranked:
        _console.print(f"  [dim]No untried credentials left for {rhost} (all rejected).[/]")
        return

    ranked.sort(key=lambda t: -t[0])

    table = Table(
        title=f"Reuse candidates for {rhost} — {len(ranked)}",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("User", style="bold white", no_wrap=True, max_width=30)
    table.add_column("Secret / Hash", no_wrap=False)
    table.add_column("Type", style="dim", width=10)
    table.add_column("Status", style="dim", width=20)
    table.add_column("Try", no_wrap=False)

    for _score, entry, status in ranked:
        if entry.kind == "cleartext":
            secret_style = "bold green"
            hint = f"nxc smb {rhost} -u '{entry.user}' -p '{entry.secret}'"
        else:
            secret_style = "bold red"
            hint = f"nxc smb {rhost} -u '{entry.user}' -H '{entry.secret}'"
        table.add_row(
            entry.user[:_LOOT_USER_MAX],
            Text(entry.secret[:_LOOT_SECRET_MAX], style=secret_style),
            entry.kind,
            status,
            Text(hint, style="dim cyan"),
        )

    _console.print(table)
    _console.print("  [dim]Record an outcome with [bold]l00t mark <user> worked|rejected[/][/]")


def loot_graph(sessions_dir: str = "sessions") -> None:
    """Render the credential-centric view of the network graph.

    Shows, per captured credential, the hosts it was harvested from, the hosts
    it authenticated to, the hosts that rejected it, and candidate hosts.

    Args:
        sessions_dir: Base sessions directory.
    """
    world = _read_json(str(Path(sessions_dir) / _WORLD_MODEL_NAME))
    relations = world.get("network_graph", {}).get("relations", [])

    creds: dict[str, dict[str, list[str]]] = {}

    def _bucket(node: str) -> dict[str, list[str]]:
        return creds.setdefault(node, {"harvested": [], "worked": [], "rejected": [], "candidate": []})

    def _host_label(node: str) -> str:
        return node[len(_HOST_NODE_PREFIX) :] if node.startswith(_HOST_NODE_PREFIX) else node

    for rel in relations:
        relation = rel.get("relation", "")
        source = rel.get("source", "")
        target = rel.get("target", "")
        if relation == _CRED_REL_HARVESTED and target.startswith(_CRED_NODE_PREFIX):
            _bucket(target)["harvested"].append(_host_label(source))
        elif source.startswith(_CRED_NODE_PREFIX):
            bucket = _bucket(source)
            if relation == _CRED_REL_WORKED:
                bucket["worked"].append(_host_label(target))
            elif relation == _CRED_REL_REJECTED:
                bucket["rejected"].append(_host_label(target))
            elif relation == _CRED_REL_CANDIDATE:
                bucket["candidate"].append(_host_label(target))

    if not creds:
        _console.print(
            "  [dim]No credential graph yet.  Creds appear here once found during "
            "recon/enum; mark outcomes with [bold]l00t mark[/].[/]"
        )
        return

    table = Table(
        title=f"Credential graph — {len(creds)} credential(s)",
        border_style="dim",
        show_lines=True,
        expand=True,
    )
    table.add_column("Credential", style="bold white", no_wrap=True, max_width=20)
    table.add_column("Harvested from", style="dim cyan", no_wrap=False)
    table.add_column("Worked on", style="bold green", no_wrap=False)
    table.add_column("Rejected on", style="bold red", no_wrap=False)
    table.add_column("Candidate", style="dim yellow", no_wrap=False)

    def _join(items: list[str]) -> str:
        return ", ".join(sorted(set(items))) if items else "—"

    for node, bucket in creds.items():
        cred_label = node[len(_CRED_NODE_PREFIX) :]
        table.add_row(
            cred_label,
            _join(bucket["harvested"]),
            _join(bucket["worked"]),
            _join(bucket["rejected"]),
            _join(bucket["candidate"]),
        )

    _console.print(table)


def resolve_cred_value(selector: str, entries: list[LootEntry]) -> str | None:
    """Resolve a user/secret ``selector`` to a canonical credential value.

    Args:
        selector: Username, secret, or full ``user:secret`` string.
        entries: Loot entries to resolve against (from :func:`gather_loot`).

    Returns:
        The matching ``user:secret`` value, preferring an exact username match,
        then an exact value match, then the first substring match. ``None`` when
        nothing matches.
    """
    sel = selector.strip()
    if not sel:
        return None
    lowered = sel.lower()
    for entry in entries:
        if entry.user == sel:
            return entry.value
    for entry in entries:
        if entry.value == sel:
            return entry.value
    for entry in entries:
        if lowered in entry.user.lower() or lowered in entry.secret.lower():
            return entry.value
    return None


def loot_mark(selector: str, outcome: str, host: str, sessions_dir: str = "sessions") -> bool:
    """Record that a credential worked or was rejected against ``host``.

    Args:
        selector: Username/secret/value identifying the credential.
        outcome: ``worked`` or ``rejected``.
        host: Host the credential was tried against.
        sessions_dir: Base sessions directory.

    Returns:
        True when an outcome edge was written, False on a usage/resolution error.
    """
    outcome = outcome.strip().lower()
    if outcome not in ("worked", "rejected"):
        _console.print("  [bold red]loot mark: outcome must be 'worked' or 'rejected'[/]")
        return False
    if not host.strip():
        _console.print("  [bold red]loot mark: no host[/]  — set [bold]assign rhost <ip>[/] or pass a host")
        return False

    value = resolve_cred_value(selector, gather_loot(sessions_dir))
    if value is None:
        _console.print(f"  [bold red]loot mark: no captured credential matches [bold]{selector}[/][/]")
        return False

    from modules.world_model import get_world_model

    wm = get_world_model(str(Path(sessions_dir) / _WORLD_MODEL_NAME))
    if outcome == "worked":
        wm.link_credential_to_success(value, host.strip())
        _console.print(f"  [bold green]marked[/] {value[:_LOOT_SECRET_MAX]} → worked on [cyan]{host.strip()}[/]")
    else:
        wm.link_credential_to_failure(value, host.strip())
        _console.print(f"  [bold red]marked[/] {value[:_LOOT_SECRET_MAX]} → rejected on [cyan]{host.strip()}[/]")
    return True


# ── pivot ─────────────────────────────────────────────────────────────────────

_PIVOT_FILE = "sessions/pivots.jsonl"


def pivot_add(new_ip: str, via_ip: str = "", note: str = "") -> None:
    """Record a newly discovered pivot target.

    Args:
        new_ip: IP of the newly reachable host.
        via_ip: IP of the compromised host that gave access (current rhost).
        note: Optional context (service, port, method).
    """
    entry = {
        "ts": time.time(),
        "ip": new_ip.strip(),
        "via": via_ip.strip(),
        "note": note.strip(),
        "phase": read_phase(),
    }
    path = Path(_PIVOT_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    _console.print(
        f"  [bold green]pivot recorded[/]  "
        f"[cyan]{new_ip}[/] via [dim]{via_ip or 'direct'}[/]" + (f"  ({note})" if note else "")
    )


def pivot_list() -> None:
    """Print the pivot chain discovered so far."""
    path = Path(_PIVOT_FILE)
    if not path.exists():
        _console.print("  [dim]No pivots recorded.  Use: pivot <new-ip> [via-ip] [note][/]")
        return

    entries = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            entries.append(json.loads(raw))
        except json.JSONDecodeError:
            continue

    if not entries:
        _console.print("  [dim]No pivots recorded.[/]")
        return

    table = Table(
        title=f"Pivot chain — {len(entries)} hop(s)",
        border_style="dim",
        show_lines=False,
    )
    table.add_column("New target", style="bold cyan", no_wrap=True)
    table.add_column("Via (compromised)", style="dim yellow", no_wrap=True)
    table.add_column("Phase", style="dim", width=10)
    table.add_column("Note", style="dim white")

    for entry in entries:
        ts = datetime.datetime.fromtimestamp(entry.get("ts", 0)).strftime("%H:%M")
        table.add_row(
            entry.get("ip", "?"),
            entry.get("via", "—") + f"  [{ts}]",
            (entry.get("phase") or "?").upper(),
            entry.get("note") or "",
        )

    _console.print(table)
    _console.print("  [dim]To make a pivot target active: [bold]assign rhost <ip>[/][/]")


# ── tasks ─────────────────────────────────────────────────────────────────────

_TASKS_FILE = "sessions/tasks.json"


def _load_tasks() -> list[dict[str, Any]]:
    data = _read_json(_TASKS_FILE)
    if isinstance(data, list):
        return data
    return data.get("tasks", data.get("items", []))


def _save_tasks(tasks: list[dict[str, Any]]) -> None:
    _write_json_atomic(_TASKS_FILE, tasks)


def tasks_list(status_filter: str = "active", limit: int = 30) -> None:
    """Print tasks from sessions/tasks.json.

    Args:
        status_filter: 'active' (New+Started), 'all', or a specific status.
        limit: Maximum rows to display.
    """
    tasks = _load_tasks()
    if not tasks:
        _console.print("  [dim]No tasks yet.  Use: tasks add <description>[/]")
        return

    if status_filter == "active":
        shown = [t for t in tasks if t.get("status", "New") in ("New", "Started")]
    elif status_filter == "all":
        shown = tasks
    else:
        shown = [t for t in tasks if t.get("status", "") == status_filter]

    from collections import Counter

    counts = Counter(t.get("status", "?") for t in tasks)
    summary = "  ".join(f"[bold]{v}[/] {k}" for k, v in sorted(counts.items()))

    table = Table(
        title=f"Tasks ({status_filter})  —  {summary}",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("ID", style="dim", width=5)
    table.add_column("Status", width=10)
    table.add_column("Title", no_wrap=False)
    table.add_column("Operator", style="dim cyan", width=18)

    _STATUS_STYLE = {
        "Done": "bold green",
        "Started": "bold yellow",
        "New": "dim white",
        "Blocked": "bold red",
    }
    for t in shown[-limit:]:
        tid = str(t.get("id", "?"))
        status = t.get("status", "New")
        style = _STATUS_STYLE.get(status, "dim white")
        table.add_row(
            tid,
            Text(status, style=style),
            t.get("title") or t.get("description") or "—",
            (t.get("operator") or "cli")[:18],
        )

    _console.print(table)


def tasks_add(title: str, operator: str = "cli") -> None:
    """Append a new task to sessions/tasks.json.

    Args:
        title: Task description.
        operator: Who created it (default 'cli').
    """
    tasks = _load_tasks()
    new_id = max((t.get("id", 0) for t in tasks), default=-1) + 1
    task = {
        "id": new_id,
        "title": title.strip(),
        "description": f"Added by operator | ts={int(time.time())}",
        "operator": operator,
        "status": "New",
    }
    tasks.append(task)
    _save_tasks(tasks)
    _console.print(f"  [bold green]task #{new_id} added[/]  {title.strip()[:80]}")


def tasks_done(task_id: int) -> bool:
    """Mark a task as Done.

    Args:
        task_id: The integer id of the task.

    Returns:
        True if found and updated, False otherwise.
    """
    tasks = _load_tasks()
    for t in tasks:
        if t.get("id") == task_id:
            t["status"] = "Done"
            _save_tasks(tasks)
            _console.print(f"  [bold green]task #{task_id} marked Done[/]  {t.get('title', '')[:60]}")
            return True
    _console.print(f"  [bold red]task #{task_id} not found[/]")
    return False


def tasks_start(task_id: int) -> bool:
    """Mark a task as Started.

    Args:
        task_id: The integer id of the task.

    Returns:
        True if found and updated, False otherwise.
    """
    tasks = _load_tasks()
    for t in tasks:
        if t.get("id") == task_id:
            t["status"] = "Started"
            _save_tasks(tasks)
            _console.print(f"  [bold yellow]task #{task_id} started[/]  {t.get('title', '')[:60]}")
            return True
    _console.print(f"  [bold red]task #{task_id} not found[/]")
    return False


# ── scans ─────────────────────────────────────────────────────────────────────


def scans_list(rhost: str = "", sessions_dir: str = "sessions") -> None:
    """List nmap scan files in sessions/, optionally filtered by rhost.

    Reads the first lines of each .nmap file to extract open ports.

    Args:
        rhost: When non-empty, only show scans for this target IP.
        sessions_dir: Path to sessions directory.
    """
    pattern = f"{sessions_dir}/scan_*.nmap"
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

    if rhost:
        files = [f for f in files if rhost in os.path.basename(f)]

    if not files:
        _console.print(f"  [dim]No scan files found{' for ' + rhost if rhost else ''}.  Run: lazynmap[/]")
        return

    table = Table(
        title=f"Nmap scans{' — ' + rhost if rhost else ''}",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("File", style="dim cyan", no_wrap=True, max_width=36)
    table.add_column("Age", style="dim", width=10)
    table.add_column("Size", style="dim", width=8)
    table.add_column("Open ports (from file)", no_wrap=False)

    _PORT_RE = re.compile(r"(\d{1,5}/\w+\s+open\s+\S+)")
    now = time.time()

    for fpath in files[:20]:
        fname = os.path.basename(fpath)
        age_s = now - os.path.getmtime(fpath)
        age_str = _human_age(age_s)
        size_str = _human_size(os.path.getsize(fpath))
        ports: list[str] = []
        try:
            content = Path(fpath).read_text(encoding="utf-8", errors="ignore")
            ports = [m.group(1) for m in _PORT_RE.finditer(content)][:6]
        except OSError:
            pass
        ports_str = "  ".join(ports) if ports else "[dim](no open ports)[/]"
        table.add_row(fname, age_str, size_str, ports_str)

    _console.print(table)


# ── sitrep ────────────────────────────────────────────────────────────────────


def sitrep(payload: dict[str, Any], sessions_dir: str = "sessions") -> None:
    """Print a unified operational situation report.

    Aggregates: target info, phase/OS, scans found, loot captured, tasks
    backlog, operator notes, pivot chain, world model hosts/vulns, and
    the last lines of sessions/plan.txt when present.

    Args:
        payload: Live params dict (from payload.json).
        sessions_dir: Path to the sessions directory.
    """
    rhost = payload.get("rhost") or "—"
    lhost = payload.get("lhost") or "—"
    domain = payload.get("domain") or "—"
    os_id = str(payload.get("os_id", "?"))
    os_label = {"1": "Linux", "2": "Windows"}.get(os_id, "?")

    world = _read_json(_WORLD_MODEL)
    phase = (world.get("phase") or world.get("current_phase") or "unknown").upper()
    phase_color = _PHASE_COLORS.get(phase.lower(), "white")
    n_hosts = len(world.get("hosts", {}))
    n_vulns = len(world.get("vulnerabilities", []))
    n_world_creds = len(world.get("credentials", []))

    tasks = _load_tasks()
    n_new = sum(1 for t in tasks if t.get("status") == "New")
    n_started = sum(1 for t in tasks if t.get("status") == "Started")
    n_done = sum(1 for t in tasks if t.get("status") == "Done")

    cred_count = _count_glob(f"{sessions_dir}/credentials*.txt")
    hash_count = _count_glob(f"{sessions_dir}/hash*.txt")

    notes_path = Path(_NOTES_FILE)
    n_notes = 0
    if notes_path.exists():
        for raw in notes_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                e = json.loads(raw)
                if rhost == "—" or e.get("rhost") == rhost:
                    n_notes += 1
            except json.JSONDecodeError:
                pass

    pivots_path = Path(_PIVOT_FILE)
    n_pivots = 0
    if pivots_path.exists():
        n_pivots = sum(
            1 for line in pivots_path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()
        )

    scan_pattern = f"{sessions_dir}/scan_*.nmap"
    scan_files = glob.glob(scan_pattern)
    rhost_scans = [f for f in scan_files if rhost in os.path.basename(f)] if rhost != "—" else []
    latest_scan = ""
    if rhost_scans:
        newest = max(rhost_scans, key=os.path.getmtime)
        age_s = time.time() - os.path.getmtime(newest)
        latest_scan = f"{os.path.basename(newest)} ({_human_age(age_s)} ago)"

    plan_snippet = _read_plan()

    _console.print()
    _console.rule(f"[bold]SITREP[/]  [cyan]{rhost}[/]  [bold {phase_color}]{phase}[/]  [dim]{os_label}[/]")

    # Target row
    t = Text()
    t.append("  TARGET  ", style="bold white on dark_red")
    t.append(f" {rhost}  lhost={lhost}  domain={domain}  os={os_label}\n")
    _console.print(t)

    # World model row
    wm_style = "bold green" if n_hosts else "dim"
    _console.print(
        f"  [bold]World model[/]   "
        f"[{wm_style}]{n_hosts} host(s)[/]  "
        f"{'[bold red]' if n_vulns else '[dim]'}{n_vulns} vuln(s)[/]  "
        f"{'[bold green]' if n_world_creds else '[dim]'}{n_world_creds} cred(s) tracked[/]"
    )

    # Scans row
    scan_info = latest_scan if latest_scan else f"{len(scan_files)} scan file(s) (not for {rhost})"
    scan_style = "bold cyan" if rhost_scans else "dim"
    _console.print(f"  [bold]Scans[/]         [{scan_style}]{scan_info}[/]  — run [bold]scans[/] for full list")

    # Loot row
    loot_style = "bold green" if cred_count else "dim"
    hash_style = "bold red" if hash_count else "dim"
    _console.print(
        f"  [bold]Loot[/]          "
        f"[{loot_style}]{cred_count} credential(s)[/]  "
        f"[{hash_style}]{hash_count} hash(es)[/]  — run [bold]l00t[/] to view"
    )

    # Tasks row
    task_new_style = "bold yellow" if n_new else "dim"
    _console.print(
        f"  [bold]Tasks[/]         "
        f"[{task_new_style}]{n_new} New[/]  "
        f"{'[bold cyan]' if n_started else '[dim]'}{n_started} Started[/]  "
        f"[dim]{n_done} Done[/]  — run [bold]tasks[/] to view"
    )

    # Notes row
    note_style = "bold magenta" if n_notes else "dim"
    _console.print(
        f"  [bold]Notes[/]         [{note_style}]{n_notes} note(s)[/] for this target  — run [bold]note[/] to view"
    )

    # Pivots row
    pivot_style = "bold orange3" if n_pivots else "dim"
    _console.print(
        f"  [bold]Pivots[/]        [{pivot_style}]{n_pivots} hop(s) recorded[/]  — run [bold]pivot[/] to view"
    )

    # Plan row
    if plan_snippet:
        _console.print(f"  [bold]Plan[/]          [dim]{plan_snippet}[/]")

    # What's next
    _console.print()
    _console.rule("[bold]What to do next[/]")
    _print_next_steps(
        rhost=rhost,
        phase=phase.lower(),
        has_scan=bool(rhost_scans),
        cred_count=cred_count,
        n_tasks_new=n_new,
        n_hosts=n_hosts,
    )
    _console.rule()
    _console.print()


def _print_next_steps(
    rhost: str,
    phase: str,
    has_scan: bool,
    cred_count: int,
    n_tasks_new: int,
    n_hosts: int,
) -> None:
    """Print 2-4 contextual next-step suggestions based on engagement state.

    Args:
        rhost: Active target IP (or "—" if unset).
        phase: Current phase string (lowercase).
        has_scan: True when a nmap scan file exists for rhost.
        cred_count: Number of credential lines captured.
        n_tasks_new: Number of tasks in New status.
        n_hosts: Number of hosts in world model.
    """
    steps: list[tuple[str, str]] = []

    if rhost == "—":
        steps.append(("wizard", "configure rhost, lhost, domain and wordlists"))
        steps.append(("assign rhost <IP>", "set target IP directly"))
        _render_steps(steps)
        return

    if not has_scan:
        steps.append(("lazynmap", "full port scan — no scan found for this target yet"))
        steps.append(("ping", "quick host reachability check before scanning"))
    else:
        if phase in ("recon", "scan", "enum", "unknown"):
            steps.append(("recommend_next", "AI-powered next command suggestion"))
            steps.append(("palette enum", "browse enumeration commands for this phase"))
            if not cred_count:
                steps.append(("suggest_next", "graph-based command recommendation"))
        elif phase == "exploit":
            steps.append(("recommend_next", "AI next-step from current scan results"))
            steps.append(("palette exploit", "browse exploitation commands"))
        elif phase == "privesc":
            steps.append(("linpeas", "Linux privilege escalation scan (os_id=1)"))
            steps.append(("winpeas", "Windows privilege escalation scan (os_id=2)"))
            steps.append(("recommend_next", "AI recommendation based on current state"))
        elif phase in ("lateral", "cred"):
            steps.append(("recommend_next", "AI lateral movement or cred-access suggestion"))
            if cred_count:
                steps.append(("l00t", f"review {cred_count} captured credential(s)"))
        elif phase == "report":
            steps.append(("vulns", "review discovered vulnerabilities"))
            steps.append(("eyewitness", "screenshot web services for the report"))
        else:
            steps.append(("recommend_next", "AI-powered next command suggestion"))
            steps.append(("palette recon", "browse recon commands"))

    if n_tasks_new:
        steps.append(("tasks", f"review {n_tasks_new} open task(s) in the backlog"))

    if not steps:
        steps.append(("sitrep", "re-run to refresh state after next command"))

    _render_steps(steps)


def _render_steps(steps: list[tuple[str, str]]) -> None:
    for cmd, reason in steps:
        _console.print(f"  [bold cyan]{cmd:<25}[/] [dim]{reason}[/]")


def _read_plan() -> str:
    path = Path("sessions/plan.txt")
    if not path.exists():
        return ""
    try:
        lines = [
            line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()
        ]
        if not lines:
            return ""
        first = lines[0]
        if "Error" in first or "API" in first:
            return ""
        return first[:100]
    except OSError:
        return ""


# ── shared small helpers ───────────────────────────────────────────────────────


def _human_age(seconds: float) -> str:
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{int(seconds / 60)}m"
    if seconds < 86400:
        return f"{int(seconds / 3600)}h"
    return f"{int(seconds / 86400)}d"


def _human_size(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n // 1024}K"
    return f"{n // (1024 * 1024)}M"


__all__ = [
    "PHASES",
    "LootEntry",
    "gather_loot",
    "loot_graph",
    "loot_mark",
    "loot_reuse",
    "loot_search",
    "loot_show",
    "note_add",
    "note_list",
    "phase_progress",
    "pivot_add",
    "pivot_list",
    "print_ctx",
    "print_phase",
    "read_phase",
    "resolve_cred_value",
    "scans_list",
    "sitrep",
    "tasks_add",
    "tasks_done",
    "tasks_list",
    "tasks_start",
    "tgrep",
    "write_phase",
]
