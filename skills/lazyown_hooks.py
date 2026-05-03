#!/usr/bin/env python3
"""
LazyOwn Hook Pipeline (Claude Code style)

8 lifecycle events with chainable handlers.
Hooks can block execution (return "deny" context) or enrich results.

Events:
  pre_tool_use       → can deny/modify before dispatch
  post_tool_use      → can enrich/log after success
  post_tool_failure  → runs after exception
  permission_denied  → runs when permission gate blocks a tool
  session_start      → runs once on MCP init
  pre_compact        → runs before context compaction
  post_compact       → runs after compaction
  audit              → runs on every tool call (logging only)
"""

import json
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Optional


class HookEvent(Enum):
    PRE_TOOL_USE      = "pre_tool_use"
    POST_TOOL_USE     = "post_tool_use"
    POST_TOOL_FAILURE = "post_tool_failure"
    PERMISSION_DENIED = "permission_denied"
    SESSION_START     = "session_start"
    PRE_COMPACT       = "pre_compact"
    POST_COMPACT      = "post_compact"
    AUDIT             = "audit"


class HookRegistry:
    """
    Chainable hook system.

    Each handler receives a context dict and returns an (optionally modified)
    context dict. Returning None leaves the context unchanged.
    Setting context["_block"] = True in a pre_tool_use hook denies execution.
    """

    def __init__(self):
        self._hooks: dict[str, list[Callable]] = {}
        self._counts: dict[str, int] = {
            "runs": 0, "blocks": 0, "errors": 0,
        }
        self._per_event: dict[str, dict[str, int]] = {}

    def register(self, event: HookEvent, handler: Callable) -> None:
        self._hooks.setdefault(event.value, []).append(handler)

    def run(self, event: HookEvent, context: dict) -> dict:
        """Run all handlers for event, chaining modified contexts."""
        ev_name = event.value
        self._counts["runs"] += 1
        ev_stats = self._per_event.setdefault(ev_name, {"runs": 0, "blocks": 0, "errors": 0})
        ev_stats["runs"] += 1
        for handler in self._hooks.get(ev_name, []):
            try:
                result = handler(context)
                if isinstance(result, dict):
                    context = result
            except Exception as exc:
                self._counts["errors"] += 1
                ev_stats["errors"] += 1
                context.setdefault("_hook_errors", []).append(
                    f"{handler.__name__}: {exc}"
                )
        if context.get("_block"):
            self._counts["blocks"] += 1
            ev_stats["blocks"] += 1
        return context

    def metrics(self) -> dict:
        """Return aggregate hook execution counts."""
        return {
            "events_registered": list(self._hooks.keys()),
            "handler_counts": {ev: len(hs) for ev, hs in self._hooks.items()},
            "totals": dict(self._counts),
            "per_event": {k: dict(v) for k, v in self._per_event.items()},
        }


# ── Built-in hooks ────────────────────────────────────────────────────────────

# Patterns that trigger automatic denial regardless of permission rules
_DESTRUCTIVE_RE = re.compile(
    r"rm\s+-rf\s+/|mkfs\.|dd\s+if=/dev/zero|fork\s+bomb|:\(\).*:\|:&",
    re.IGNORECASE,
)

# Rate-limiting state (simple in-memory counter)
_rate: dict[str, list[float]] = {}


def sandbox_hook(context: dict) -> dict:
    """
    PRE_TOOL_USE: block catastrophic shell commands before permission evaluation.
    Acts as a last-resort safety net independent of the permission system.
    """
    import time
    tool = context.get("tool_name", "")
    args = context.get("arguments", {})
    cmd  = args.get("command", "") + args.get("script", "")

    if cmd and _DESTRUCTIVE_RE.search(cmd):
        context["_block"] = True
        context["_block_reason"] = f"Sandbox: destructive pattern in command"
    return context


def rate_limit_hook(context: dict, window: float = 2.0, limit: int = 5) -> dict:
    """
    PRE_TOOL_USE: prevent rapid-fire C2 commands (>5 per 2s).
    Protects against runaway agent loops.
    """
    import time
    tool = context.get("tool_name", "")
    if not tool.startswith("lazyown_c2_"):
        return context

    now = time.monotonic()
    bucket = _rate.setdefault(tool, [])
    # evict old entries
    _rate[tool] = [t for t in bucket if now - t < window]
    if len(_rate[tool]) >= limit:
        context["_block"] = True
        context["_block_reason"] = f"Rate limit: {tool} exceeded {limit} calls/{window}s"
        return context
    _rate[tool].append(now)
    return context


def audit_hook(context: dict, audit_path: Optional[Path] = None) -> dict:
    """
    AUDIT: append a one-line JSON record of every tool call to the audit log.
    Non-blocking — errors are silently swallowed.
    """
    if audit_path is None:
        return context
    try:
        entry = {
            "ts":      datetime.now().isoformat(),
            "tool":    context.get("tool_name", "?"),
            "event":   context.get("_event", "audit"),
            "blocked": context.get("_block", False),
            "args":    str(context.get("arguments", {}))[:200],
        }
        with open(audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass
    return context


def timing_hook(context: dict) -> dict:
    """
    POST_TOOL_USE: annotate result with wall-clock execution time.
    Reads _start_time set by pre_tool_use in the same call.
    """
    import time
    start = context.get("_start_time")
    if start is not None:
        elapsed = time.monotonic() - start
        content = context.get("result_content", "")
        context["result_content"] = content + f"\n[elapsed: {elapsed:.2f}s]"
    return context


def start_timer_hook(context: dict) -> dict:
    """PRE_TOOL_USE: record start time for timing_hook."""
    import time
    context["_start_time"] = time.monotonic()
    return context


# ── Registry factory ──────────────────────────────────────────────────────────

def build_default_registry(sessions_dir: Optional[Path] = None) -> HookRegistry:
    """
    Create a HookRegistry with the built-in safety hooks wired up.
    Call this once and keep the singleton.
    """
    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
    registry = HookRegistry()

    # Safety hooks run first
    registry.register(HookEvent.PRE_TOOL_USE, sandbox_hook)
    registry.register(HookEvent.PRE_TOOL_USE, rate_limit_hook)
    registry.register(HookEvent.PRE_TOOL_USE, start_timer_hook)

    # Post hooks
    registry.register(HookEvent.POST_TOOL_USE, timing_hook)

    # Audit hook (with path bound if sessions_dir given)
    if sessions_dir:
        audit_path = sessions_dir / "tool_audit.jsonl"
        def _audit(ctx):
            return audit_hook(ctx, audit_path)
        _audit.__name__ = "audit_hook"
        registry.register(HookEvent.AUDIT, _audit)
        registry.register(HookEvent.POST_TOOL_USE, _audit)
        registry.register(HookEvent.PERMISSION_DENIED, _audit)
        registry.register(HookEvent.POST_TOOL_FAILURE, _audit)

    return registry


# Module-level singleton (initialized by MCP on startup)
_registry: Optional[HookRegistry] = None


def get_registry(sessions_dir: Optional[Path] = None) -> HookRegistry:
    global _registry
    if _registry is None:
        _registry = build_default_registry(sessions_dir)
    return _registry
