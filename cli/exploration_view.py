"""Rich-based renderers for the exploration engine.

Keeps the rendering logic out of :mod:`cli.exploration` so the engine
stays pure (no console / no terminal dependency) and trivially unit-
testable. Every renderer here accepts plain dataclasses from the engine
and writes to a :class:`rich.console.Console` instance supplied by the
caller, so the shell, the dashboard TUI and the tests can all share the
same output without coupling.
"""

from __future__ import annotations

from typing import Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from cli.exploration import (
    AddonEntry,
    CoverageReport,
    DiscoveredService,
    ExplorationEngine,
    ToolEntry,
)

TREE_GUIDE_STYLE: str = "dim cyan"
HEADER_STYLE: str = "bold cyan"
SERVICE_STYLE: str = "bold yellow"
ADDON_STYLE: str = "green"
TOOL_STYLE: str = "magenta"
RUN_GLYPH: str = "[done]"
PENDING_GLYPH: str = "[ ]"
MAX_NAME_WIDTH: int = 32


def render_exploration(
    console: Console,
    engine: ExplorationEngine,
    target: str | None,
    history: set[str],
) -> None:
    """Render the full ``explore`` view to ``console``.

    Args:
        console: Rich console used for output.
        engine: Pre-configured exploration engine to query.
        target: Optional rhost filter for the nmap scan lookup.
        history: Set of already executed command/tool/addon names.
    """

    services = engine.services(target)
    grouped = engine.suggestions_for_target(target)
    coverage = engine.coverage(target)

    _render_header(console, target, coverage)
    if not services:
        console.print("[yellow]No nmap XML found in sessions/. Run 'lazynmap' first to populate exploration data.[/]")
    else:
        _render_service_tree(console, services, grouped, history)
    _render_unexplored(
        console,
        engine.unexplored_addons(target),
        engine.unexplored_tools(target),
    )
    _render_coverage_table(console, coverage)


def _render_header(
    console: Console,
    target: str | None,
    coverage: CoverageReport,
) -> None:
    """Render the heading panel summarising scope and coverage."""

    scope_label = target or "(all targets)"
    text = Text()
    text.append("Target: ", style=HEADER_STYLE)
    text.append(scope_label + "\n")
    text.append("Discovered services: ", style=HEADER_STYLE)
    text.append(f"{coverage.services_total}\n")
    text.append("Addons enabled: ", style=HEADER_STYLE)
    text.append(f"{coverage.addons_enabled}/{coverage.addons_total}\n")
    text.append("Tools active: ", style=HEADER_STYLE)
    text.append(f"{coverage.tools_total}\n")
    text.append("Commands in history: ", style=HEADER_STYLE)
    text.append(f"{coverage.history_commands}")
    console.print(Panel(text, title="Exploration scope", border_style="cyan"))


def _render_service_tree(
    console: Console,
    services: Sequence[DiscoveredService],
    grouped: dict[str, dict[str, list]],
    history: set[str],
) -> None:
    """Render the host -> service -> addons/tools tree."""

    root = Tree("[bold]Discovered surface[/bold]", guide_style=TREE_GUIDE_STYLE)
    by_host: dict[str, list[DiscoveredService]] = {}
    for service in services:
        by_host.setdefault(service.host, []).append(service)

    for host, host_services in sorted(by_host.items()):
        host_branch = root.add(f"[bold]{host}[/bold]  ({len(host_services)} ports)")
        for service in host_services:
            service_label = Text()
            service_label.append(service.label, style=SERVICE_STYLE)
            extras: list[str] = []
            if service.product:
                extras.append(service.product)
            if service.version:
                extras.append(service.version)
            if extras:
                service_label.append("  ")
                service_label.append(" ".join(extras), style="dim")
            service_branch = host_branch.add(service_label)
            groups = grouped.get(service.label, {"addons": [], "tools": []})
            _render_entries(
                service_branch,
                groups["addons"],
                history,
                style=ADDON_STYLE,
                kind="addon",
            )
            _render_entries(
                service_branch,
                groups["tools"],
                history,
                style=TOOL_STYLE,
                kind="tool",
            )
            if not groups["addons"] and not groups["tools"]:
                service_branch.add(Text("(no triggered items)", style="dim"))
    console.print(root)


def _render_entries(
    parent: Tree,
    entries: Sequence[AddonEntry | ToolEntry],
    history: set[str],
    style: str,
    kind: str,
) -> None:
    """Render a row per addon or tool under a service branch."""

    for entry in entries:
        glyph = RUN_GLYPH if entry.name in history else PENDING_GLYPH
        name_field = entry.name[:MAX_NAME_WIDTH].ljust(MAX_NAME_WIDTH)
        os_field = entry.addon_os if isinstance(entry, AddonEntry) else entry.tool_os
        label = Text()
        label.append(f"{glyph} ", style="dim")
        label.append(f"{kind:<5} ", style="dim")
        label.append(name_field, style=style)
        label.append(f"  os={os_field}", style="dim")
        parent.add(label)


def _render_unexplored(
    console: Console,
    unexplored_addons: Sequence[AddonEntry],
    unexplored_tools: Sequence[ToolEntry],
) -> None:
    """Render the 'try these next' section for the active scan."""

    if not unexplored_addons and not unexplored_tools:
        return
    table = Table(
        title="Triggered but never run",
        title_style=HEADER_STYLE,
        show_lines=False,
    )
    table.add_column("Kind")
    table.add_column("Name")
    table.add_column("OS")
    table.add_column("Trigger")
    for addon in unexplored_addons:
        table.add_row(
            "addon",
            Text(addon.name, style=ADDON_STYLE),
            addon.addon_os,
            ", ".join(addon.trigger) or "(any)",
        )
    for tool in unexplored_tools:
        table.add_row(
            "tool",
            Text(tool.name, style=TOOL_STYLE),
            tool.tool_os,
            ", ".join(tool.trigger) or "(any)",
        )
    console.print(table)


def _render_coverage_table(console: Console, coverage: CoverageReport) -> None:
    """Render a coverage percentage summary table."""

    table = Table(
        title="Exploration coverage",
        title_style=HEADER_STYLE,
        show_lines=False,
    )
    table.add_column("Dimension")
    table.add_column("Done")
    table.add_column("Total")
    table.add_column("Percent")
    table.add_row(
        "Services with a run command",
        str(coverage.services_with_run_command),
        str(coverage.services_total),
        f"{coverage.service_coverage * 100:.1f}%",
    )
    table.add_row(
        "Enabled addons executed",
        str(coverage.addons_executed),
        str(coverage.addons_enabled),
        f"{coverage.addon_coverage * 100:.1f}%",
    )
    table.add_row(
        "Active tools executed",
        str(coverage.tools_executed),
        str(coverage.tools_total),
        f"{coverage.tool_coverage * 100:.1f}%",
    )
    console.print(table)


__all__ = ["render_exploration"]
