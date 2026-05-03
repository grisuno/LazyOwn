#!/usr/bin/env python3
"""
LazyOwn Context Compaction Pipeline — 5-layer graduated compression (Claude Code style)

Layers:
  1. Budget reduction   — hard cap on individual tool output size
  2. Snip              — trim older history entries
  3. Microcompact      — remove redundant/boilerplate sections
  4. Context collapse  — read-time projection (structural summary)
  5. Auto-compact      — template-based session summary (last resort)
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ── Budget caps per tool category ────────────────────────────────────────────

_TOOL_BUDGET: dict[str, int] = {
    # High-cardinality outputs get smaller budgets
    "lazyown_session_sitrep":  6_000,
    "lazyown_campaign_sitrep": 5_000,
    "lazyown_heartbeat_status": 3_000,
    "lazyown_run_command":     8_000,
    "lazyown_run_api":         4_000,
    "lazyown_read_session_file": 6_000,
    "lazyown_list_sessions":   3_000,
    "lazyown_list_modules":    2_000,
    "lazyown_get_config":      2_000,
    "lazyown_automap_query":   5_000,
    "lazyown_pdb_query":       5_000,
    "lazyown_hive_recall":     4_000,
    "lazyown_policy_state":    3_000,
    "lazyown_facts_get":       4_000,
    "_default":               10_000,
}

# Patterns that add bulk but little signal → stripped in microcompact
_BOILERPLATE_PATTERNS = [
    re.compile(r"\[LazyOwn\]\s*[^\n]*\n", re.MULTILINE),   # banners
    re.compile(r"={40,}\n"),                                  # separator lines
    re.compile(r"─{20,}\n"),
    re.compile(r"\[DEBUG\][^\n]*\n", re.MULTILINE),
    re.compile(r"Press ENTER[^\n]*\n", re.MULTILINE),
    re.compile(r"Use Ctrl\+C[^\n]*\n", re.MULTILINE),
]

@dataclass
class CompactionResult:
    content: str
    original_len: int
    final_len: int
    layers_applied: list[str]
    truncated: bool = False

    def summary(self) -> str:
        pct = 100 * (1 - self.final_len / max(self.original_len, 1))
        return (f"[compacted {pct:.0f}% via {'+'.join(self.layers_applied)}]"
                if self.layers_applied else "")


class ContextCompactor:
    """
    Apply layered compaction to tool output strings.

    Usage:
        compactor = ContextCompactor()
        result = compactor.compact(content, tool_name="lazyown_run_command")
        return result.content
    """

    def __init__(
        self,
        budget_override: Optional[dict[str, int]] = None,
        snip_threshold: int = 6_000,
        collapse_threshold: int = 9_000,
    ):
        self.budget = {**_TOOL_BUDGET, **(budget_override or {})}
        self.snip_threshold = snip_threshold
        self.collapse_threshold = collapse_threshold

    # ── Layer 1: Budget reduction ─────────────────────────────────────────────

    def apply_budget(self, content: str, tool_name: str) -> tuple[str, bool]:
        """Hard-cap output. Keeps head + tail for readability."""
        cap = self.budget.get(tool_name, self.budget["_default"])
        if len(content) <= cap:
            return content, False
        head = cap * 6 // 10
        tail = cap * 2 // 10
        trimmed = (
            content[:head]
            + f"\n\n... [{len(content) - head - tail:,} chars truncated"
            f" — use lazyown_read_session_file for full output] ...\n\n"
            + content[-tail:]
        )
        return trimmed, True

    # ── Layer 2: Snip (remove repeated/old content blocks) ───────────────────

    def snip(self, content: str) -> tuple[str, bool]:
        """Remove duplicate consecutive lines (log noise)."""
        if len(content) <= self.snip_threshold:
            return content, False
        lines = content.splitlines(keepends=True)
        seen: set[str] = set()
        result: list[str] = []
        dups = 0
        for line in lines:
            stripped = line.strip()
            if stripped and stripped in seen and len(stripped) > 20:
                dups += 1
                continue
            seen.add(stripped)
            result.append(line)
        if dups == 0:
            return content, False
        return "".join(result) + f"\n[snip: {dups} duplicate lines removed]\n", True

    # ── Layer 3: Microcompact (strip boilerplate) ─────────────────────────────

    def microcompact(self, content: str) -> tuple[str, bool]:
        """Strip known low-signal patterns. Cheap, always run on >500 chars."""
        if len(content) <= 500:
            return content, False
        result = content
        removed = 0
        for pat in _BOILERPLATE_PATTERNS:
            new = pat.sub("", result)
            removed += len(result) - len(new)
            result = new
        if removed == 0:
            return content, False
        return result, True

    # ── Layer 4: Context collapse (structural summary) ────────────────────────

    def collapse(self, content: str, tool_name: str) -> tuple[str, bool]:
        """Replace repetitive sections with a structural summary."""
        if len(content) <= self.collapse_threshold:
            return content, False
        lines = content.splitlines()
        total = len(lines)
        # Keep first 40 + last 20 lines, summarize the middle
        if total <= 80:
            return content, False
        head_lines = lines[:40]
        tail_lines = lines[-20:]
        middle_count = total - 60
        collapsed = (
            "\n".join(head_lines)
            + f"\n\n[context-collapse: {middle_count} lines summarized]\n"
            + f"[Original length: {len(content):,} chars, tool: {tool_name}]\n\n"
            + "\n".join(tail_lines)
        )
        return collapsed, True

    # ── Layer 5: Auto-compact (session summary) ───────────────────────────────

    @staticmethod
    def auto_compact_session(entries: list[dict]) -> str:
        """
        Template-based session summary when full pipeline is insufficient.
        entries: list of {"type": str, "data": dict} from SessionTranscript.
        """
        commands: list[str] = []
        findings: list[str] = []
        errors: list[str] = []

        for e in entries:
            t = e.get("type", "")
            d = e.get("data", {})
            if t == "tool_use":
                cmd = d.get("arguments", {}).get("command", "")
                if cmd:
                    commands.append(f"{d.get('tool_name', '?')}: {cmd[:60]}")
            elif t == "tool_result":
                result = d.get("content", "")
                if any(kw in result.lower() for kw in ("found", "success", "open", "vuln", "cred")):
                    findings.append(result[:120])
                if any(kw in result.lower() for kw in ("error", "failed", "denied", "timeout")):
                    errors.append(result[:80])

        lines = [
            "## Auto-compact Session Summary",
            f"Total events: {len(entries)}",
            f"Commands run: {len(commands)}",
            f"Findings: {len(findings)}",
            f"Errors: {len(errors)}",
            "",
        ]
        if commands:
            lines.append("### Recent Commands (last 5)")
            lines.extend(f"  {c}" for c in commands[-5:])
        if findings:
            lines.append("### Key Findings (last 3)")
            lines.extend(f"  {f}" for f in findings[-3:])
        if errors:
            lines.append("### Errors (last 3)")
            lines.extend(f"  {e}" for e in errors[-3:])
        return "\n".join(lines)

    # ── Full pipeline ─────────────────────────────────────────────────────────

    def compact(self, content: str, tool_name: str = "_default") -> CompactionResult:
        """Apply all applicable layers in order."""
        original = len(content)
        applied: list[str] = []

        content, did_micro = self.microcompact(content)
        if did_micro:
            applied.append("micro")

        content, did_snip = self.snip(content)
        if did_snip:
            applied.append("snip")

        content, did_collapse = self.collapse(content, tool_name)
        if did_collapse:
            applied.append("collapse")

        content, truncated = self.apply_budget(content, tool_name)
        if truncated:
            applied.append("budget")

        return CompactionResult(
            content=content,
            original_len=original,
            final_len=len(content),
            layers_applied=applied,
            truncated=truncated,
        )


# Module-level singleton — import and use directly
_compactor = ContextCompactor()


def compact_output(content: str, tool_name: str = "_default") -> str:
    """Convenience wrapper: compact and return string."""
    return _compactor.compact(content, tool_name).content
