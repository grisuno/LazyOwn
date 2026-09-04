"""Contextual help system for the LazyOwn shell.

Extends the default ``cmd2`` help with phase, requirements, examples,
and alias information sourced from the command index and the shell state.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - All output through ``rich.console.Console``.
    - ``ContextualHelp`` receives its dependencies via constructor.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli.phase_labels import PHASE_LABELS

_console = Console(highlight=False, soft_wrap=True)

COMMAND_INDEX_PATH = Path("cli/command_index.json")

PHASE_TIPS: dict[str, tuple[str, ...]] = {
    "recon": (
        "Run 'ping' first to detect OS before scanning.",
        "Read sessions/scan_<rhost>.nmap before re-scanning.",
        "After nmap, run 'auto_populate' to fill payload context.",
    ),
    "enum": (
        "After enumeration, run 'facts_show' to review findings.",
        "Use 'recommend_next' for AI-ranked follow-ups.",
    ),
    "exploit": (
        "Search exploits first with 'ss <service> <version>'.",
        "Generate a payload with 'venom' or 'lazymsfvenom'.",
    ),
    "postexp": (
        "Run 'linpeas' (Linux) or 'winpeas' (Windows) for privesc paths.",
        "Capture credentials with 'creds' after access.",
    ),
    "cred": (
        "Capture creds with 'creds' to persist them.",
        "Use 'hash' to view captured hashes.",
    ),
    "lateral": (
        "Use 'evil' for WinRM or 'psexec' for SMB execution.",
        "Check 'creds' for captured credentials first.",
    ),
    "c2": (
        "Start C2 with 'lazyc2'.",
        "Use 'collab_join <handle>' for team collaboration.",
    ),
}


@dataclass(frozen=True)
class CommandInfo:
    """Enriched command information for contextual help."""

    name: str
    summary: str
    phase: str
    category: str | None
    source_file: str | None
    aliases: tuple[str, ...] = ()
    requires_rhost: bool = False
    requires_creds: bool = False
    requires_domain: bool = False
    examples: tuple[str, ...] = ()


@dataclass
class ContextualHelpConfig:
    """Centralised constants for contextual help."""

    index_path: Path = COMMAND_INDEX_PATH
    max_phase_commands: int = 15


def _load_command_index(path: Path | None = None) -> dict[str, Any]:
    """Load the command index JSON. Returns empty dict on failure."""
    p = path or COMMAND_INDEX_PATH
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def _build_command_lookup(index: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build a name -> info lookup from the command index."""
    lookup: dict[str, dict[str, Any]] = {}
    for cmd in index.get("commands", []):
        name = cmd.get("name", "")
        if name.startswith("do_"):
            lookup[name[3:]] = cmd
    return lookup


_CREDS_COMMANDS = frozenset(
    {
        "evil",
        "psexec",
        "secretsdump",
        "bloodhound",
        "cme",
        "enum4linux",
        "hashcat",
        "john",
        "hydra",
        "medusa",
        "spraykatz",
        "ssh_cmd",
        "wmiexec",
        "getnpusers",
        "kerberoasting",
    }
)

_RHOST_REQUIRED = frozenset(
    {
        "lazynmap",
        "batchnmap",
        "auto_populate",
        "facts_show",
        "gobuster",
        "ffuf",
        "nikto",
        "dirsearch",
        "nuclei",
        "nmap",
        "masscan",
        "enum4linux",
        "cme",
        "evil",
        "psexec",
        "ssh_cmd",
        "scp",
        "linpeas",
        "winpeas",
        "ss",
        "ww",
        "finalrecon",
        "sqlmap",
    }
)

_DOMAIN_REQUIRED = frozenset(
    {
        "bloodhound",
        "cme",
        "ldapdomaindump",
        "getnpusers",
        "nxcridbrute",
        "enum4linux",
    }
)


class ContextualHelp:
    """Enriched help provider for LazyOwn commands.

    Args:
        aliases: Live aliases dict from the shell.
        params: Live params dict from the shell.
        config: Optional config override.
    """

    def __init__(
        self,
        aliases: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        config: ContextualHelpConfig | None = None,
    ) -> None:
        self._aliases = aliases or {}
        self._params = params or {}
        self._config = config or ContextualHelpConfig()
        self._index = _load_command_index(self._config.index_path)
        self._lookup = _build_command_lookup(self._index)

    def get_command_info(self, name: str) -> CommandInfo | None:
        """Return enriched info for a command, or None if not found."""
        info = self._lookup.get(name)
        if info is None:
            return None

        aliases = tuple(a for a, target in self._aliases.items() if target == name)

        return CommandInfo(
            name=name,
            summary=info.get("summary", "No description available."),
            phase=info.get("phase", "uncategorized"),
            category=info.get("category"),
            source_file=info.get("source_file"),
            aliases=aliases,
            requires_rhost=name in _RHOST_REQUIRED,
            requires_creds=name in _CREDS_COMMANDS,
            requires_domain=name in _DOMAIN_REQUIRED,
        )

    def render_command_help(self, name: str) -> bool:
        """Render contextual help for a single command. Returns True if rendered."""
        info = self.get_command_info(name)
        if info is None:
            return False

        rhost = self._params.get("rhost", "")
        start_user = self._params.get("start_user", "")
        start_pass = self._params.get("start_pass", "")
        domain = self._params.get("domain", "")
        os_id = str(self._params.get("os_id", ""))

        parts: list[str] = []
        parts.append(f"[bold]{info.summary}[/]")

        phase_label = PHASE_LABELS.get(info.phase, info.phase.title())
        parts.append(f"[dim]Phase:[/] {phase_label}")
        if info.source_file:
            parts.append(f"[dim]Source:[/] {info.source_file}")

        reqs: list[str] = []
        if info.requires_rhost:
            status = "green" if rhost else "red"
            reqs.append(f"[{status}]rhost ({rhost or 'NOT SET'})[/]")
        if info.requires_creds:
            has_creds = start_user != "CHANGE_ME" and start_pass != "CHANGE_ME"
            status = "green" if has_creds else "yellow"
            reqs.append(f"[{status}]credentials ({start_user if has_creds else 'NOT SET'})[/]")
        if info.requires_domain:
            status = "green" if domain else "yellow"
            reqs.append(f"[{status}]domain ({domain or 'NOT SET'})[/]")

        if reqs:
            parts.append(f"[dim]Requires:[/] {' | '.join(reqs)}")

        if info.aliases:
            parts.append(f"[dim]Aliases:[/] {', '.join(info.aliases)}")

        tips = PHASE_TIPS.get(info.phase, ())
        if tips:
            parts.append(f"\n[dim]Tips for {phase_label}:[/]")
            for tip in tips:
                parts.append(f"  [dim]-[/] {tip}")

        _console.print(
            Panel(
                "\n".join(parts),
                title=f"[bold cyan]{name}[/]",
                border_style="cyan",
            )
        )
        return True

    def render_phase_commands(self, phase: str) -> None:
        """Render all commands for a given phase."""
        label = PHASE_LABELS.get(phase, phase.title())
        cmds = self._index.get("phase_to_commands", {}).get(phase, [])

        if not cmds:
            _console.print(f"[dim]No commands found for phase '{label}'.[/]")
            return

        table = Table(title=f"{label} commands", show_header=True, header_style="bold cyan")
        table.add_column("Command", style="green", min_width=20)
        table.add_column("Description")

        for cmd_name in cmds:
            info = self._lookup.get(cmd_name, {})
            summary = info.get("summary", "")
            table.add_row(cmd_name, summary[:80])

        _console.print(table)

    def render_requirements_status(self) -> None:
        """Show which requirements are met for the current session."""
        rhost = self._params.get("rhost", "")
        lhost = self._params.get("lhost", "")
        start_user = self._params.get("start_user", "")
        start_pass = self._params.get("start_pass", "")
        domain = self._params.get("domain", "")
        os_id = str(self._params.get("os_id", ""))

        table = Table(title="Session requirements", show_header=True, header_style="bold")
        table.add_column("Requirement", style="bold")
        table.add_column("Value")
        table.add_column("Status")

        items = [
            ("rhost", rhost, bool(rhost) and rhost != "127.0.0.1"),
            ("lhost", lhost, bool(lhost)),
            ("os_id", os_id, os_id in ("1", "2")),
            ("domain", domain, bool(domain)),
            ("credentials", f"{start_user}", start_user != "CHANGE_ME" and start_pass != "CHANGE_ME"),
        ]

        for label, value, met in items:
            status = "[green]SET[/]" if met else "[red]NOT SET[/]"
            table.add_row(label, value or "-", status)

        _console.print(table)
