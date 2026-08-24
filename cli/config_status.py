"""Simplified configuration status display for the LazyOwn shell.

Groups payload.json fields by category, shows which are set, which need
attention, and which are optional -- replacing the raw JSON dump with a
human-friendly overview.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py``.
    - All output through ``rich.console.Console``.
    - ``ConfigStatus`` receives a params dict; never reads payload.json directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console(highlight=False, soft_wrap=True)

FIELD_GROUPS: dict[str, dict[str, tuple[str, str, str]]] = {
    "Target": {
        "rhost": ("Target IP or hostname", "required", "assign rhost <IP>"),
        "domain": ("Target domain (e.g. target.htb)", "recommended", "assign domain <domain>"),
        "scope": ("Authorization scope (CIDR/hostname)", "optional", "scope add <CIDR>"),
        "os_id": ("Target OS (1=Linux, 2=Windows)", "auto", "detected by ping"),
    },
    "Attacker": {
        "lhost": ("Your VPN/tun0 IP", "required", "assign lhost <IP>"),
        "lport": ("Your listen port", "required", "assign lport <port>"),
        "device": ("Network interface", "optional", "assign device eth0"),
    },
    "Credentials": {
        "start_user": ("Initial username for brute-force", "recommended", "assign start_user <user>"),
        "start_pass": ("Initial password for brute-force", "recommended", "assign start_pass <pass>"),
        "api_key": ("LLM API key (Groq/OpenAI)", "optional", "assign api_key <key>"),
    },
    "Wordlists": {
        "dirwordlist": ("Directory brute-force wordlist", "auto", "auto-detected from SecLists"),
        "usrwordlist": ("Username brute-force wordlist", "auto", "auto-detected from SecLists"),
        "dnswordlist": ("DNS subdomain wordlist", "auto", "auto-detected from SecLists"),
    },
    "C2": {
        "c2_port": ("C2 server port", "required", "assign c2_port <port>"),
        "c2_user": ("C2 login username", "required", "assign c2_user <user>"),
        "c2_pass": ("C2 login password", "required", "assign c2_pass <pass>"),
    },
}


@dataclass(frozen=True)
class ConfigStatusConfig:
    """Centralised constants for config status display."""

    default_marker = "CHANGE_ME"
    null_markers = frozenset({"null", "None", "none", ""})


class ConfigStatus:
    """Display grouped configuration status.

    Args:
        params: Live params dict from the shell.
        config: Optional config override.
    """

    def __init__(
        self,
        params: dict[str, Any],
        config: ConfigStatusConfig | None = None,
    ) -> None:
        self._params = params
        self._config = config or ConfigStatusConfig()

    def _field_status(self, key: str, value: Any) -> tuple[str, str]:
        """Return (status_label, color) for a field value."""
        if value is None:
            return ("NOT SET", "red")
        str_val = str(value).strip()
        if str_val in self._config.null_markers:
            return ("NOT SET", "red")
        if str_val == self._config.default_marker:
            return ("CHANGE ME", "yellow")
        return ("OK", "green")

    def render_status(self) -> None:
        """Render the grouped configuration status table."""
        total_ok = 0
        total_warn = 0
        total_unset = 0

        for group_name, fields in FIELD_GROUPS.items():
            table = Table(title=group_name, show_header=True, header_style="bold")
            table.add_column("Field", style="bold", min_width=16)
            table.add_column("Value")
            table.add_column("Status", justify="center")
            table.add_column("How to set", style="dim")

            for key, (_description, importance, hint) in fields.items():
                value = self._params.get(key)
                status, color = self._field_status(key, value)

                display_val = str(value) if value is not None else "-"
                if len(display_val) > 40:
                    display_val = display_val[:37] + "..."

                status_text = f"[{color}]{status}[/]"
                if importance == "required" and status != "OK":
                    status_text = f"[bold red]{status}[/]"
                    total_unset += 1
                elif importance == "recommended" and status != "OK":
                    total_warn += 1
                elif status == "OK":
                    total_ok += 1
                else:
                    total_unset += 1

                table.add_row(key, display_val, status_text, hint)

            _console.print(table)
            _console.print()

        summary = (
            f"[green]{total_ok} set[/] | "
            f"[yellow]{total_warn} recommended[/] | "
            f"[red]{total_unset} unset[/]"
        )
        _console.print(Panel(summary, title="[bold]Configuration summary[/]", border_style="cyan"))

    def render_quick_check(self) -> None:
        """Quick check: show only required fields that are not set."""
        missing: list[str] = []
        for _group_name, fields in FIELD_GROUPS.items():
            for key, (_description, importance, hint) in fields.items():
                if importance == "required":
                    value = self._params.get(key)
                    status, _ = self._field_status(key, value)
                    if status != "OK":
                        missing.append(f"  [red]{key}[/] -- {hint}")

        if missing:
            _console.print(Panel(
                "\n".join(missing),
                title="[bold red]Required fields not set[/]",
                border_style="red",
            ))
        else:
            _console.print("[green]All required fields are configured.[/]")
