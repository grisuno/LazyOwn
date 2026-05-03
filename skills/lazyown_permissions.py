#!/usr/bin/env python3
"""
LazyOwn Permission System — Deny-First Rule Evaluation (Claude Code style)

Deny rules ALWAYS win over allow rules.
Modes: plan | default | accept_edits | auto | dont_ask | bypass_permissions
"""

import fnmatch
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class PermissionMode(Enum):
    PLAN        = "plan"               # model creates plan, user approves all
    DEFAULT     = "default"            # standard interactive use
    ACCEPT_EDITS = "accept_edits"      # file edits auto-approved
    AUTO        = "auto"               # ML classifier evaluates
    DONT_ASK    = "dont_ask"           # no prompts; deny rules apply
    BYPASS      = "bypass_permissions" # skip most checks (test/debug only)
    BUBBLE      = "bubble"             # escalate to parent terminal (internal)


@dataclass
class PermissionRule:
    tool_pattern: str          # glob: "lazyown_c2_command", "lazyown_run_*"
    action: str                # "allow" | "deny" | "ask"
    condition: Optional[str] = None  # "contains:rm -rf", "target:10.10.11.*"
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "tool_pattern": self.tool_pattern,
            "action": self.action,
            "condition": self.condition,
            "description": self.description,
            "created_at": self.created_at,
        }


# Tools that are always safe to allow regardless of mode
_READ_ONLY_TOOLS = frozenset({
    "lazyown_get_config",
    "lazyown_list_modules",
    "lazyown_get_beacons",
    "lazyown_c2_status",
    "lazyown_session_sitrep",
    "lazyown_list_sessions",
    "lazyown_read_session_file",
    "lazyown_agent_status",
    "lazyown_agent_result",
    "lazyown_list_agents",
    "lazyown_hive_status",
    "lazyown_hive_recall",
    "lazyown_hive_result",
    "lazyown_campaign_sitrep",
    "lazyown_heartbeat_status",
    "lazyown_search_tools",
    "lazyown_manage_permissions",
    "lazyown_get_objectives",
    "lazyown_get_soul",
    "lazyown_policy_state",
    "lazyown_recommend",
    "lazyown_facts_get",
    "lazyown_automap_query",
    "lazyown_swan_status",
})

# Command patterns that are always denied regardless of rules
_ALWAYS_DENY_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"mkfs\.",
    r"dd\s+if=/dev/zero\s+of=/dev/[sh]d",
    r":(){ :|:& };:",       # fork bomb
    r"chmod\s+-R\s+777\s+/",
    r">\s*/etc/passwd",
    r"wget.*\|\s*bash",
    r"curl.*\|\s*bash",
    r"curl.*\|\s*sh",
]
_ALWAYS_DENY_RE = re.compile("|".join(_ALWAYS_DENY_PATTERNS), re.IGNORECASE)


class PermissionSystem:
    """
    Deny-first rule evaluator with persistent JSON rule store.

    Rule evaluation order:
      1. Hard-coded always-deny patterns (catastrophic commands)
      2. Read-only tool bypass (never blocked by mode)
      3. User deny rules (wins over allow)
      4. User allow rules
      5. Mode default (dont_ask → deny; others → ask)
    """

    def __init__(self, sessions_dir: Path):
        self.rules_file = sessions_dir / "permissions.json"
        self.audit_log  = sessions_dir / "permissions_audit.jsonl"
        self.mode       = PermissionMode.DEFAULT
        self.rules: list[PermissionRule] = []
        sessions_dir.mkdir(parents=True, exist_ok=True)
        self._load()

    # ── persistence ──────────────────────────────────────────────────────────

    def _load(self):
        if not self.rules_file.exists():
            self._save()
            return
        try:
            data = json.loads(self.rules_file.read_text())
            self.mode = PermissionMode(data.get("mode", "default"))
            self.rules = [PermissionRule(**r) for r in data.get("rules", [])]
        except Exception:
            pass

    def _save(self):
        data = {
            "mode": self.mode.value,
            "updated_at": datetime.now().isoformat(),
            "rules": [r.to_dict() for r in self.rules],
        }
        self.rules_file.write_text(json.dumps(data, indent=2))

    def _audit(self, tool: str, decision: str, reason: str, args: dict):
        entry = {
            "ts": datetime.now().isoformat(),
            "tool": tool,
            "decision": decision,
            "reason": reason,
            "args_preview": str(args)[:200],
        }
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    # ── rule management ───────────────────────────────────────────────────────

    def add_rule(self, tool_pattern: str, action: str,
                 condition: Optional[str] = None, description: str = "") -> str:
        rule = PermissionRule(tool_pattern, action, condition, description)
        self.rules.append(rule)
        self._save()
        return f"Rule added: {action} {tool_pattern}"

    def remove_rule(self, tool_pattern: str, action: str) -> str:
        before = len(self.rules)
        self.rules = [
            r for r in self.rules
            if not (r.tool_pattern == tool_pattern and r.action == action)
        ]
        self._save()
        return f"Removed {before - len(self.rules)} rule(s) for {tool_pattern}"

    def set_mode(self, mode: str) -> str:
        self.mode = PermissionMode(mode)
        self._save()
        return f"Permission mode set to: {self.mode.value}"

    def list_rules(self) -> list[dict]:
        return [r.to_dict() for r in self.rules]

    # ── evaluation ───────────────────────────────────────────────────────────

    def evaluate(self, tool_name: str, arguments: dict) -> tuple[str, str]:
        """
        Returns (decision, reason).
        decision: "allow" | "deny" | "ask"
        """
        # 0. Bypass mode skips everything
        if self.mode == PermissionMode.BYPASS:
            self._audit(tool_name, "allow", "bypass mode", arguments)
            return "allow", "bypass_permissions mode active"

        # 1. Hard always-deny patterns (catastrophic command check)
        cmd = arguments.get("command", "") or arguments.get("script", "")
        if cmd and _ALWAYS_DENY_RE.search(cmd):
            reason = "Catastrophic command pattern detected"
            self._audit(tool_name, "deny", reason, arguments)
            return "deny", reason

        # 2. Read-only tools are always allowed
        if tool_name in _READ_ONLY_TOOLS:
            self._audit(tool_name, "allow", "read-only tool", arguments)
            return "allow", "read-only tool (always permitted)"

        # 3. Deny rules take precedence
        for rule in self.rules:
            if rule.action == "deny" and self._matches(rule, tool_name, arguments):
                reason = f"Deny rule: {rule.tool_pattern}"
                if rule.description:
                    reason += f" — {rule.description}"
                self._audit(tool_name, "deny", reason, arguments)
                return "deny", reason

        # 4. Allow rules
        for rule in self.rules:
            if rule.action == "allow" and self._matches(rule, tool_name, arguments):
                reason = f"Allow rule: {rule.tool_pattern}"
                self._audit(tool_name, "allow", reason, arguments)
                return "allow", reason

        # 5. Mode defaults
        if self.mode == PermissionMode.DONT_ASK:
            reason = "dont_ask mode: deny-first (no matching allow rule)"
            self._audit(tool_name, "deny", reason, arguments)
            return "deny", reason

        if self.mode == PermissionMode.BYPASS:
            self._audit(tool_name, "allow", "bypass", arguments)
            return "allow", "bypass mode"

        reason = f"No explicit rule — interactive approval needed ({self.mode.value} mode)"
        self._audit(tool_name, "ask", reason, arguments)
        return "ask", reason

    def _matches(self, rule: PermissionRule, tool_name: str, args: dict) -> bool:
        if not fnmatch.fnmatch(tool_name, rule.tool_pattern):
            return False
        if not rule.condition:
            return True
        # condition format: "contains:<substring>" or "target:<pattern>"
        if rule.condition.startswith("contains:"):
            needle = rule.condition[len("contains:"):]
            haystack = args.get("command", "") + args.get("script", "")
            return needle in haystack
        if rule.condition.startswith("target:"):
            pattern = rule.condition[len("target:"):]
            target = args.get("target", "") or args.get("rhost", "")
            return fnmatch.fnmatch(target, pattern)
        return True

    # ── metrics (defense-in-depth dashboard) ──────────────────────────────────

    def metrics(self) -> dict:
        """Aggregate audit log into per-decision and per-tool counts."""
        counts: dict[str, int] = {"allow": 0, "deny": 0, "ask": 0}
        by_tool: dict[str, dict[str, int]] = {}
        recent_denials: list[dict] = []
        if self.audit_log.exists():
            try:
                with open(self.audit_log) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            e = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        decision = e.get("decision", "?")
                        tool = e.get("tool", "?")
                        counts[decision] = counts.get(decision, 0) + 1
                        by_tool.setdefault(tool, {"allow": 0, "deny": 0, "ask": 0})
                        by_tool[tool][decision] = by_tool[tool].get(decision, 0) + 1
                        if decision == "deny":
                            recent_denials.append({
                                "ts": e.get("ts", ""), "tool": tool,
                                "reason": e.get("reason", "")[:80],
                            })
            except OSError:
                pass
        return {
            "mode": self.mode.value,
            "rules_count": len(self.rules),
            "decisions": counts,
            "total_evaluations": sum(counts.values()),
            "by_tool": by_tool,
            "recent_denials": recent_denials[-5:],
        }

    # ── human-readable status ─────────────────────────────────────────────────

    def status_text(self) -> str:
        lines = [
            f"Permission mode: {self.mode.value}",
            f"Rules loaded:    {len(self.rules)}",
            "",
        ]
        if self.rules:
            lines.append("Rules (deny first):")
            deny_rules  = [r for r in self.rules if r.action == "deny"]
            allow_rules = [r for r in self.rules if r.action == "allow"]
            ask_rules   = [r for r in self.rules if r.action == "ask"]
            for r in deny_rules:
                lines.append(f"  ❌ DENY  {r.tool_pattern}"
                             + (f"  [{r.condition}]" if r.condition else "")
                             + (f"  # {r.description}" if r.description else ""))
            for r in allow_rules:
                lines.append(f"  ✅ ALLOW {r.tool_pattern}"
                             + (f"  [{r.condition}]" if r.condition else "")
                             + (f"  # {r.description}" if r.description else ""))
            for r in ask_rules:
                lines.append(f"  ❓ ASK   {r.tool_pattern}"
                             + (f"  [{r.condition}]" if r.condition else "")
                             + (f"  # {r.description}" if r.description else ""))
        else:
            lines.append("No rules configured — all non-read-only tools require approval in DEFAULT mode.")
        lines += [
            "",
            "Modes: plan | default | accept_edits | auto | dont_ask | bypass_permissions",
            "Use lazyown_manage_permissions to add rules or change mode.",
        ]
        return "\n".join(lines)
