"""Non-blocking inline hint renderer for the LazyOwn cmd2 shell.

After each command executes, a single dim line is printed with the top-N
graph-based next-step suggestions derived from the graphify knowledge graph.
The GraphLoader caches by (path, mtime) so rendering is sub-millisecond after
the first graph load; subsequent calls return from memory.

Design notes:
- Zero coupling to cmd2, lazyown.py or Flask — this module is a pure renderer.
- The caller decides whether hints are enabled (reads payload.json flag).
- Output goes to stdout via rich so ANSI is handled correctly on all terminals.
- Commands on SKIP_COMMANDS never produce hints (noise-free UX).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.text import Text

if TYPE_CHECKING:
    from cli.graph_advisor import GraphAdvisor

SKIP_COMMANDS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "suggest_next",
        "graph_search",
        "neighbors",
        "god_nodes",
        "set",
        "show",
        "palette",
        "assign",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
    }
)

_MAX_LABEL_LEN: int = 24
_HINT_CONSOLE: Console = Console(stderr=False, highlight=False, soft_wrap=True)


def render_inline_hints(
    advisor: GraphAdvisor,
    last_command: str,
    limit: int = 3,
    enabled: bool = True,
) -> None:
    """Print a single dim hint line below the command output and return immediately.

    The line format is:
        ↳ label_a · label_b · label_c

    This renders between the command output and the next cmd2 prompt so it
    never blocks the operator from typing the next command.

    Args:
        advisor: GraphAdvisor instance (reuses its internal mtime-keyed cache).
        last_command: Raw command string that just executed (first token used).
        limit: Maximum number of suggestions to display.
        enabled: When False the function is a no-op. Controlled by the
            ``enable_inline_hints`` key in payload.json.

    Returns:
        None — side effect is at most one line written to stdout.
    """
    if not enabled:
        return
    cmd = _first_token(last_command)
    if not cmd or cmd in SKIP_COMMANDS:
        return
    try:
        suggestions = advisor.suggest_next(recent_commands=[cmd], limit=limit)
    except Exception:
        return
    if not suggestions:
        return
    labels = _extract_labels(suggestions, limit)
    if not labels:
        return
    _render(labels)


def _first_token(raw: str) -> str:
    parts = (raw or "").split()
    return parts[0] if parts else ""


def _extract_labels(suggestions: list[dict], limit: int) -> list[str]:
    out: list[str] = []
    for s in suggestions:
        label = s.get("label") or s.get("id") or ""
        if label:
            out.append(_truncate(label, _MAX_LABEL_LEN))
        if len(out) >= limit:
            break
    return out


def _truncate(value: str, max_len: int) -> str:
    return value if len(value) <= max_len else value[: max_len - 1] + "…"


def _render(labels: list[str]) -> None:
    hint = Text()
    hint.append("  ↳ ", style="bold dim cyan")
    hint.append(" · ".join(labels), style="dim white italic")
    _HINT_CONSOLE.print(hint)


__all__ = ["SKIP_COMMANDS", "render_inline_hints"]
