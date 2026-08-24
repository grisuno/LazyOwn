"""Interactive post-install tutorial for the LazyOwn framework.

Guides a new operator through the golden path:
    ping -> lazynmap -> auto_populate -> facts_show -> recommend_next

Each step explains what happens, shows the output, and suggests the next
action.  Persists completion in ``sessions/tutorial_done`` so it does not
repeat on subsequent launches.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - All output through ``rich.console.Console``.
    - ``run`` receives a ``params`` dict and a ``command_runner`` callable
      so tests can stub execution without touching the shell.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console(highlight=False, soft_wrap=True)

DONE_MARKER = Path("sessions/tutorial_done")

PHASES: tuple[tuple[str, str, str], ...] = (
    (
        "ping",
        "ICMP TTL probe to detect the target OS",
        "TTL ~64 = Linux, ~128 = Windows. Sets os_id automatically.",
    ),
    (
        "lazynmap",
        "Full TCP port scan",
        "Writes to sessions/scan_<rhost>.nmap. Never re-run if the file exists.",
    ),
    (
        "auto_populate",
        "Parse nmap XML into payload context",
        "Fills domain, os_id, services and first creds into payload.json.",
    ),
    (
        "facts_show",
        "Display discovered facts",
        "Quick read of what the scan found: ports, services, versions.",
    ),
    (
        "recommend_next",
        "AI-ranked next steps",
        "Local engine fuses policy + recon plan + knowledge graph into the 3-5 best commands.",
    ),
)

FINISHED_TEXT = """\
The golden path is complete.  You now know the five core commands
that drive every engagement.

Next steps:
  [bold cyan]engage[/]          - Run the whole kill chain automatically
  [bold cyan]orchestrate[/]     - Hand a free-text goal to the AI backends
  [bold cyan]dashboard[/]       - Full-screen TUI with target, phase, hints
  [bold cyan]help[/]            - Browse all 727+ commands
  [bold cyan]wizard[/]          - Re-run the guided setup wizard

Type [bold green]?[/] at any time for the full command list.
"""


@dataclass(frozen=True)
class TutorialConfig:
    """Centralised constants for the tutorial."""

    done_marker: Path = DONE_MARKER
    sessions_dir: str = "sessions"


def is_done(config: TutorialConfig | None = None) -> bool:
    """Return True if the tutorial has already been completed."""
    cfg = config or TutorialConfig()
    return cfg.done_marker.exists()


def mark_done(config: TutorialConfig | None = None) -> None:
    """Persist the tutorial completion marker."""
    cfg = config or TutorialConfig()
    cfg.done_marker.parent.mkdir(parents=True, exist_ok=True)
    cfg.done_marker.write_text("done")


def render_header() -> None:
    """Print the tutorial welcome banner."""
    _console.print()
    _console.print(
        Panel(
            "[bold yellow]LazyOwn Interactive Tutorial[/]\n\n"
            "This guided walkthrough teaches the [bold]golden path[/] -- "
            "the five commands that drive every engagement.\n\n"
            "Press [bold cyan]Enter[/] after each step to continue, "
            "or type [bold cyan]skip[/] to jump to the end.",
            title="[bold]Tutorial[/]",
            border_style="yellow",
        )
    )
    _console.print()


def render_phase_table() -> None:
    """Print the full phase overview before starting."""
    table = Table(title="The Golden Path", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Command", style="green")
    table.add_column("What it does")
    table.add_column("Why it matters", style="dim")

    for idx, (cmd, desc, why) in enumerate(PHASES, 1):
        table.add_row(str(idx), cmd, desc, why)

    _console.print(table)
    _console.print()


def run_step(
    index: int,
    command: str,
    description: str,
    why: str,
    params: dict[str, Any],
    command_runner: Callable[[str], str],
) -> bool:
    """Execute one tutorial step and return True if the user wants to continue.

    Args:
        index: 1-based step number.
        command: The command verb to execute.
        description: One-line explanation of the command.
        why: Why this step matters.
        params: Live payload params dict.
        command_runner: Callable that executes a LazyOwn shell command and
            returns its output string.

    Returns:
        True if the user pressed Enter to continue, False if they typed skip.
    """
    rhost = params.get("rhost", "")
    _console.print()
    _console.print(
        f"[bold yellow]Step {index}/5[/] -- [bold green]{command}[/]"
    )
    _console.print(f"  {description}")
    _console.print(f"  [dim]{why}[/]")
    _console.print()

    if command in ("ping", "lazynmap", "auto_populate") and not rhost:
        _console.print(
            "  [bold red]rhost is not set.[/] Run [bold cyan]assign rhost <IP>[/] "
            "before continuing the tutorial."
        )
        _console.print()
        return True

    _console.print(f"  [dim]$ {command}[/]")
    try:
        output = command_runner(command)
        if output:
            lines = output.strip().splitlines()
            for line in lines[:20]:
                _console.print(f"  {line}")
            if len(lines) > 20:
                _console.print(f"  [dim]... ({len(lines) - 20} more lines)[/]")
    except Exception as exc:
        _console.print(f"  [bold red]Command failed:[/] {exc}")

    _console.print()
    try:
        user_input = input("  Press Enter to continue, or type 'skip': ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        user_input = "skip"

    return user_input != "skip"


def run(
    params: dict[str, Any],
    command_runner: Callable[[str], str],
    *,
    force: bool = False,
    config: TutorialConfig | None = None,
) -> bool:
    """Run the interactive tutorial.

    Args:
        params: Live params dict (in-memory mirror of payload.json).
        command_runner: Callable that executes a LazyOwn shell command string.
        force: When True, re-run even if already completed.
        config: Optional config override.

    Returns:
        True if the tutorial completed, False if skipped or already done.
    """
    cfg = config or TutorialConfig()

    if not force and is_done(cfg):
        _console.print("[dim]Tutorial already completed. Use 'tutorial --force' to replay.[/]")
        return True

    render_header()
    render_phase_table()

    for idx, (cmd, desc, why) in enumerate(PHASES, 1):
        cont = run_step(idx, cmd, desc, why, params, command_runner)
        if not cont:
            _console.print("[yellow]Tutorial skipped.[/]")
            return False

    _console.print()
    _console.print(Panel(FINISHED_TEXT, title="[bold green]Tutorial Complete[/]", border_style="green"))
    mark_done(cfg)
    return True
