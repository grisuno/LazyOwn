"""Canonical non-actionable verb registry for post-command surfaces.

The inline hints, the unified tips engine, and the interactive chain
prompt each skip a near-identical list of verbs that produce no
engagement progress (help, history, navigation, and configuration
commands). This module is the single source of truth for that
vocabulary so the three surfaces can never drift apart again.

Each surface composes its own exported set from the shared base plus
its surface-specific extras, keeping backwards-compatible names:

- ``cli.reactive_hints.SKIP_COMMANDS`` = base + graph hints extras
- ``cli.tips_engine.SKIP_COMMANDS`` = base + tips extras
- ``cli.chain_mode.CHAIN_SKIP_VERBS`` = base + chain extras
"""

from __future__ import annotations

BASE_NOISE_VERBS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "set",
        "assign",
        "show",
        "palette",
        "palette_k",
        "browse",
        "timeline_browser",
        "form",
        "graph_overlay",
        "toast_clear",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
    }
)

HINTS_EXTRA_VERBS: frozenset[str] = frozenset(
    {
        "suggest_next",
        "graph_search",
        "neighbors",
        "god_nodes",
    }
)

TIPS_EXTRA_VERBS: frozenset[str] = frozenset(
    {
        "next",
        ".",
        ",",
        "sitrep",
        "ctx",
        "phase",
        "note",
        "l00t",
        "pivot",
        "tasks",
        "scans",
        "wizard",
        "chainmode",
    }
)

CHAIN_EXTRA_VERBS: frozenset[str] = TIPS_EXTRA_VERBS | frozenset(
    {
        "prev",
        "recommend_next",
        "suggest_next",
        "explore",
    }
)

__all__ = [
    "BASE_NOISE_VERBS",
    "CHAIN_EXTRA_VERBS",
    "HINTS_EXTRA_VERBS",
    "TIPS_EXTRA_VERBS",
]
