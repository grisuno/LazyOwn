"""Reconnaissance plan generator built on top of :mod:`cli.exploration`.

After ``do_lazynmap`` finishes scanning a target the operator is left with
a raw XML in ``sessions/`` and no immediate guidance about which addon,
``.tool`` or CLI verb to invoke next. This module bridges that gap by
composing the trigger-matched outputs already produced by
:class:`cli.exploration.ExplorationEngine` (addons + tools) with the
phase-aware ``cli/command_index.json`` into a single, persisted plan.

The module is pure: it does no shell I/O, holds no global state and
never imports ``cmd2``, ``rich`` or ``lazyown.py``. The CLI integration
lives in ``do_lazynmap`` / ``do_recommend_next`` which call
:func:`build_recon_plan`, then optionally pipe the result through
:func:`render_markdown` (operator + LLM consumption) or
:func:`render_rich` (terminal preview).

Design constraints honoured:

* Single Responsibility: every helper does exactly one thing.
* Open / Closed: new item kinds extend :class:`ReconPlanItem` without
  touching the renderer.
* Liskov / Interface Segregation: the engine collaborator only needs to
  satisfy the ``unexplored_addons`` / ``unexplored_tools`` / ``services``
  / ``history`` contract already provided by
  :class:`cli.exploration.ExplorationEngine`.
* Dependency Inversion: file I/O, command-index loading and time are all
  injected so the suite never touches the real ``sessions/`` tree.
* No magic numbers / hardcoded paths: every default lives in
  :class:`ReconPlanConfig`.
* Sessions ``write_plan`` is atomic (``*.tmp`` then ``os.replace``) with
  ``0o600`` permissions, matching the pattern used by
  :class:`skills.unified_orchestrator.EventBus`.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from cli.exploration import (
    AddonEntry,
    DiscoveredService,
    ExplorationEngine,
    ToolEntry,
)

_KIND_ADDON = "addon"
_KIND_TOOL = "tool"
_KIND_COMMAND = "command"
_KIND_NOTE = "note"
_PLAN_FILE_PREFIX = "recon_plan_"
_PLAN_FILE_SUFFIX = ".md"


@dataclass(frozen=True)
class ReconPlanConfig:
    """Immutable defaults for plan generation, rendering and persistence."""

    sessions_dir: str = "sessions"
    command_index_path: str = "cli/command_index.json"
    plan_file_prefix: str = _PLAN_FILE_PREFIX
    plan_file_suffix: str = _PLAN_FILE_SUFFIX
    max_addons: int = 5
    max_tools: int = 5
    max_commands: int = 5
    file_mode: int = 0o600
    encoding: str = "utf-8"
    default_phase: str = "enum"
    phase_aliases: Mapping[str, str] = field(
        default_factory=lambda: {
            "recon": "recon",
            "scan": "recon",
            "enum": "enum",
            "exploit": "exploit",
            "privesc": "privesc",
            "lateral": "lateral",
            "cred": "cred",
            "persist": "persist",
            "exfil": "exfil",
            "report": "report",
            "c2": "c2",
        }
    )
    fallback_target: str = "unknown-target"


@dataclass(frozen=True)
class ReconPlanItem:
    """One actionable suggestion in a :class:`ReconPlan`.

    Attributes:
        kind: One of ``addon``, ``tool``, ``command``, ``note``.
        name: Identifier of the addon, tool or CLI verb.
        service: ``service:port/proto`` label that triggered the item, or
            an empty string for phase-priority command suggestions.
        trigger_match: Comma-separated trigger keywords that matched.
        command_preview: Best-effort copy-paste command shown to the
            operator. Empty when the item is a CLI verb the operator
            invokes directly.
        reason: One-line justification (English, no emoji) explaining
            why the item is in the plan.
    """

    kind: str
    name: str
    service: str
    trigger_match: str
    command_preview: str
    reason: str


@dataclass(frozen=True)
class ReconPlan:
    """Snapshot of a target's next-step plan.

    Attributes:
        target: Host or hostname the plan was built for.
        platform: Resolved victim OS used to filter items.
        phase: Kill-chain phase the command suggestions came from.
        services: Discovered services that fed the trigger matching.
        items: Ordered actionable suggestions.
        generated_at: Epoch seconds when the plan was assembled.
    """

    target: str
    platform: str
    phase: str
    services: tuple[DiscoveredService, ...]
    items: tuple[ReconPlanItem, ...]
    generated_at: float

    @property
    def is_empty(self) -> bool:
        """Return ``True`` when the plan carries no actionable items."""
        return not self.items


def build_recon_plan(
    target: str | None,
    engine: ExplorationEngine,
    payload: Mapping[str, Any] | None = None,
    config: ReconPlanConfig | None = None,
    command_index_loader: Callable[[Path], Mapping[str, Any] | None] | None = None,
    clock: Callable[[], float] | None = None,
) -> ReconPlan:
    """Assemble a :class:`ReconPlan` for ``target`` using ``engine``.

    Args:
        target: Host the plan is for. ``None`` lets the engine fall back
            to the most recent scan in ``sessions/``.
        engine: An :class:`ExplorationEngine` already configured with the
            current victim OS.
        payload: Optional ``payload.json`` mapping. Used to resolve the
            active phase and substitute ``{ip}`` / ``{domain}`` /
            ``{username}`` / ``{password}`` placeholders in the
            previewed commands.
        config: Optional :class:`ReconPlanConfig` override.
        command_index_loader: Injected loader for ``cli/command_index.json``.
            Defaults to a stdlib-only reader. Returning ``None`` skips
            the command-suggestions layer cleanly.
        clock: Zero-arg callable returning the current epoch seconds.
            Defaults to :func:`time.time`.

    Returns:
        A populated :class:`ReconPlan`. The result is empty (``is_empty``
        true) when no nmap scan has been performed yet.
    """
    cfg = config or ReconPlanConfig()
    payload = payload or {}
    clock = clock or time.time
    command_index_loader = command_index_loader or _default_command_index_loader

    resolved_target = (target or "").strip() or _payload_target(payload, cfg)
    services = tuple(engine.services(resolved_target if resolved_target else None))
    unexplored_addons = engine.unexplored_addons(resolved_target if resolved_target else None)
    unexplored_tools = engine.unexplored_tools(resolved_target if resolved_target else None)
    history = engine.history()

    items: list[ReconPlanItem] = []
    items.extend(_addon_items(unexplored_addons[: cfg.max_addons], services, payload))
    items.extend(_tool_items(unexplored_tools[: cfg.max_tools], services, payload))
    phase = _resolve_phase(payload, cfg)
    command_items = _command_items(
        command_index_loader(Path(cfg.command_index_path)),
        phase=phase,
        history=history,
        limit=cfg.max_commands,
    )
    items.extend(command_items)

    return ReconPlan(
        target=resolved_target or cfg.fallback_target,
        platform=engine.current_os,
        phase=phase,
        services=services,
        items=tuple(items),
        generated_at=float(clock()),
    )


def render_markdown(plan: ReconPlan) -> str:
    """Render ``plan`` as a Markdown document suitable for sessions/.

    The output is intentionally small (no embedded HTML, no nested
    formatting) so both the operator and downstream LLM agents can parse
    it deterministically.
    """
    lines: list[str] = []
    lines.append(f"# Recon plan — {plan.target}")
    lines.append("")
    lines.append(f"_generated_at_: `{int(plan.generated_at)}`  _platform_: `{plan.platform}`  _phase_: `{plan.phase}`")
    lines.append("")
    if plan.services:
        lines.append("## Discovered services")
        lines.append("")
        lines.append("| service | port | product | version |")
        lines.append("|---|---|---|---|")
        for svc in plan.services:
            lines.append(
                f"| {svc.service or '?'} | {svc.port}/{svc.proto} | {svc.product or '-'} | {svc.version or '-'} |"
            )
        lines.append("")
    if plan.is_empty:
        lines.append("_No actionable items: no triggers matched or every match has been run._")
        lines.append("")
        return "\n".join(lines)
    lines.append("## Suggested next steps")
    lines.append("")
    lines.append("| # | kind | name | service | trigger | reason |")
    lines.append("|---|---|---|---|---|---|")
    for index, item in enumerate(plan.items, 1):
        lines.append(
            f"| {index} | {item.kind} | `{item.name}` | "
            f"{item.service or '-'} | {item.trigger_match or '-'} | {item.reason} |"
        )
    lines.append("")
    preview_items = [item for item in plan.items if item.command_preview]
    if preview_items:
        lines.append("## Command previews")
        lines.append("")
        for item in preview_items:
            lines.append(f"### {item.kind}: {item.name}")
            lines.append("")
            lines.append("```sh")
            lines.append(item.command_preview)
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


def write_plan(
    plan: ReconPlan,
    sessions_dir: str | os.PathLike[str] | None = None,
    config: ReconPlanConfig | None = None,
) -> Path:
    """Persist ``plan`` to ``sessions/recon_plan_<target>.md`` atomically.

    Args:
        plan: Plan to persist.
        sessions_dir: Override for the sessions directory. Defaults to
            ``config.sessions_dir`` resolved against the current working
            directory.
        config: Optional :class:`ReconPlanConfig` override.

    Returns:
        The absolute :class:`Path` of the written plan file.
    """
    cfg = config or ReconPlanConfig()
    sessions = Path(sessions_dir) if sessions_dir is not None else Path(cfg.sessions_dir)
    sessions.mkdir(parents=True, exist_ok=True)
    filename = f"{cfg.plan_file_prefix}{_safe_filename_component(plan.target)}{cfg.plan_file_suffix}"
    final_path = (sessions / filename).resolve()
    body = render_markdown(plan)
    fd, tmp_path = tempfile.mkstemp(
        prefix=f".{filename}.",
        suffix=".tmp",
        dir=str(sessions),
    )
    try:
        with os.fdopen(fd, "w", encoding=cfg.encoding) as handle:
            handle.write(body)
        os.chmod(tmp_path, cfg.file_mode)
        os.replace(tmp_path, final_path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
    return final_path


def render_rich(plan: ReconPlan, console: Any) -> None:
    """Render ``plan`` to the supplied Rich console.

    The console is duck-typed; only ``print`` is required so callers can
    inject any object implementing the same interface in tests.
    """
    if plan.is_empty:
        console.print(f"[dim]Recon plan empty for {plan.target} (no addons/tools/commands matched).[/]")
        return
    console.print(
        f"[bold]Recon plan[/] for [cyan]{plan.target}[/] "
        f"([dim]platform={plan.platform} phase={plan.phase} "
        f"services={len(plan.services)}[/])"
    )
    for index, item in enumerate(plan.items, 1):
        style = _RICH_KIND_STYLE.get(item.kind, "white")
        service_part = f"[dim]{item.service}[/] " if item.service else ""
        console.print(
            f"  [bold cyan]{index}.[/] [{style}]{item.kind:<7}[/] "
            f"[bold]{item.name:<24}[/] {service_part}[dim]{item.reason}[/]"
        )


_RICH_KIND_STYLE: Mapping[str, str] = {
    _KIND_ADDON: "green",
    _KIND_TOOL: "magenta",
    _KIND_COMMAND: "yellow",
    _KIND_NOTE: "dim",
}


def _addon_items(
    addons: Sequence[AddonEntry],
    services: Sequence[DiscoveredService],
    payload: Mapping[str, Any],
) -> Iterable[ReconPlanItem]:
    for addon in addons:
        matched_service, trigger_match = _service_for_trigger(addon.trigger, services)
        yield ReconPlanItem(
            kind=_KIND_ADDON,
            name=addon.name,
            service=matched_service,
            trigger_match=trigger_match,
            command_preview="",
            reason=(f"addon triggers on [{', '.join(addon.trigger) or 'any'}] and has not been run for this target"),
        )


def _tool_items(
    tools: Sequence[ToolEntry],
    services: Sequence[DiscoveredService],
    payload: Mapping[str, Any],
) -> Iterable[ReconPlanItem]:
    for tool in tools:
        matched_service, trigger_match = _service_for_trigger(tool.trigger, services)
        preview = _tool_command_preview(tool, payload)
        yield ReconPlanItem(
            kind=_KIND_TOOL,
            name=tool.name,
            service=matched_service,
            trigger_match=trigger_match,
            command_preview=preview,
            reason=(
                f"pwntomate tool triggers on [{', '.join(tool.trigger) or 'any'}] and has not been run for this target"
            ),
        )


def _command_items(
    index: Mapping[str, Any] | None,
    phase: str,
    history: set[str],
    limit: int,
) -> Iterable[ReconPlanItem]:
    if not isinstance(index, Mapping):
        return []
    phase_to_commands = index.get("phase_to_commands")
    if not isinstance(phase_to_commands, Mapping):
        return []
    candidates = phase_to_commands.get(phase, [])
    if not isinstance(candidates, Sequence):
        return []
    commands_list = index.get("commands", [])
    summaries: dict[str, str] = {}
    if isinstance(commands_list, Sequence):
        for entry in commands_list:
            if isinstance(entry, Mapping):
                name = entry.get("name")
                if isinstance(name, str):
                    summaries[name] = str(entry.get("summary") or "").strip()
    out: list[ReconPlanItem] = []
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        if candidate in history:
            continue
        verb = candidate[3:] if candidate.startswith("do_") else candidate
        if verb in history:
            continue
        summary = summaries.get(candidate, "")
        out.append(
            ReconPlanItem(
                kind=_KIND_COMMAND,
                name=verb,
                service="",
                trigger_match=phase,
                command_preview=verb,
                reason=summary or f"unrun {phase} verb from the command index",
            )
        )
        if len(out) >= limit:
            break
    return out


def _service_for_trigger(
    trigger: Sequence[str],
    services: Sequence[DiscoveredService],
) -> tuple[str, str]:
    if not trigger:
        return ("", "")
    trigger_set = {t.lower() for t in trigger if isinstance(t, str)}
    for svc in services:
        if (svc.service or "").lower() in trigger_set:
            matches = ", ".join(sorted(trigger_set & {(svc.service or "").lower()}))
            return (svc.label, matches)
    return ("", ", ".join(trigger))


def _tool_command_preview(tool: ToolEntry, payload: Mapping[str, Any]) -> str:
    raw = _read_tool_command(tool.source_path)
    if not raw:
        return ""
    substitutions = {
        "ip": str(payload.get("rhost") or ""),
        "rhost": str(payload.get("rhost") or ""),
        "lhost": str(payload.get("lhost") or ""),
        "lport": str(payload.get("lport") or ""),
        "domain": str(payload.get("domain") or ""),
        "username": str(payload.get("start_user") or ""),
        "password": str(payload.get("start_pass") or ""),
        "toolname": tool.name,
        "outputdir": "sessions",
    }
    preview = raw
    for key, value in substitutions.items():
        preview = preview.replace("{" + key + "}", value)
    return preview.strip()


def _read_tool_command(source_path: str) -> str:
    if not source_path:
        return ""
    try:
        text = Path(source_path).read_text(encoding="utf-8")
    except OSError:
        return ""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return ""
    if not isinstance(data, Mapping):
        return ""
    command = data.get("command")
    return command if isinstance(command, str) else ""


def _payload_target(payload: Mapping[str, Any], config: ReconPlanConfig) -> str:
    for key in ("active_target", "rhost", "domain"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _resolve_phase(payload: Mapping[str, Any], config: ReconPlanConfig) -> str:
    raw = payload.get("phase") or payload.get("current_phase") or ""
    if not isinstance(raw, str):
        return config.default_phase
    return config.phase_aliases.get(raw.strip().lower(), config.default_phase)


def _safe_filename_component(value: str) -> str:
    if not value:
        return "unknown"
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    cleaned = "".join(c if c in allowed else "_" for c in value.strip())
    return cleaned or "unknown"


def _default_command_index_loader(path: Path) -> Mapping[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        return None
    return loaded if isinstance(loaded, Mapping) else None


__all__ = [
    "ReconPlan",
    "ReconPlanConfig",
    "ReconPlanItem",
    "build_recon_plan",
    "render_markdown",
    "render_rich",
    "write_plan",
]
