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


def loot_show(sessions_dir: str = "sessions") -> None:
    """Print a unified table of all captured credentials and hashes.

    Reads every credentials*.txt and hash*.txt under sessions_dir. Each file
    is expected to have one ``user:secret`` entry per line.
    """
    import glob as _glob

    rows: list[dict[str, str]] = []

    for pattern, kind in (
        (f"{sessions_dir}/credentials*.txt", "cleartext"),
        (f"{sessions_dir}/hash*.txt", "hash"),
    ):
        for fpath in sorted(_glob.glob(pattern)):
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
                rows.append(
                    {
                        "source": fname,
                        "kind": kind,
                        "user": user.strip()[:40],
                        "secret": secret.strip()[:60],
                    }
                )

    if not rows:
        _console.print("  [dim]No l00t yet.  Credentials land in sessions/credentials*.txt[/]")
        return

    table = Table(
        title=f"Loot — {len(rows)} credential(s)",
        border_style="dim",
        show_lines=False,
        expand=True,
    )
    table.add_column("Source", style="dim cyan", no_wrap=True, max_width=24)
    table.add_column("Type", style="dim", width=10)
    table.add_column("User", style="bold white", no_wrap=True, max_width=30)
    table.add_column("Secret / Hash", no_wrap=False)

    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (row["user"], row["secret"])
        dup_style = "dim" if key in seen else ""
        seen.add(key)
        secret_cell = Text(row["secret"])
        if row["kind"] == "cleartext":
            secret_cell.stylize("bold green")
        else:
            secret_cell.stylize("bold red")
        if dup_style:
            secret_cell.stylize("dim")
        table.add_row(
            Text(row["source"], style=f"dim cyan {dup_style}"),
            Text(row["kind"], style=f"dim {dup_style}"),
            Text(row["user"], style=f"bold white {dup_style}"),
            secret_cell,
        )

    _console.print(table)


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
    "loot_show",
    "note_add",
    "note_list",
    "pivot_add",
    "pivot_list",
    "print_ctx",
    "print_phase",
    "read_phase",
    "scans_list",
    "sitrep",
    "tasks_add",
    "tasks_done",
    "tasks_list",
    "tasks_start",
    "tgrep",
    "write_phase",
]
