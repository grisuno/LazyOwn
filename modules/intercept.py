"""User-configurable tool-call interception layer with human-in-loop approvals.

Ports the LAZY ``guard`` + ``intercept`` contracts to LazyOwn idioms:
every autonomous tool call passes through :meth:`Interceptor.evaluate`
before execution. Three actions are supported: allow, deny, ask.
Ask creates a pending record that an operator approves or denies,
optionally with a timeout that resolves to a safe default.
"""

from __future__ import annotations

import re
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class InterceptAction(str, Enum):
    """Possible outcomes of rule evaluation."""

    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


ALLOWED_ACTIONS = frozenset({a.value for a in InterceptAction})


@dataclass(frozen=True, slots=True)
class InterceptConfig:
    """Centralized constants for interception behavior."""

    ask_timeout_sec: float = 300.0
    deny_message: str = "Blocked by intercept rule."
    ask_message: str = "Waiting for operator approval."
    audit_limit: int = 200


CONFIG = InterceptConfig()

DEFAULT_ASK_TIMEOUT_SEC = CONFIG.ask_timeout_sec
DEFAULT_DENY_MESSAGE = CONFIG.deny_message
DEFAULT_ASK_MESSAGE = CONFIG.ask_message


@dataclass
class InterceptRule:
    """Single user-configurable interception rule."""

    pattern: str
    action: str
    priority: int = 0
    message: str = ""
    is_regex: bool = False
    builtin: bool = False
    _compiled: Any = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        """Validate action and pre-compile regex patterns."""
        if self.action not in ALLOWED_ACTIONS:
            raise ValueError(f"Invalid action: {self.action}")
        if self.is_regex:
            self._compiled = re.compile(self.pattern)

    def matches(self, tool: str, command: str) -> bool:
        """Return True when this rule matches the tool call surface."""
        haystack = f"{tool} {command or ''}"
        if self.is_regex and self._compiled is not None:
            return bool(self._compiled.search(haystack))
        return self.pattern.lower() in haystack.lower()


@dataclass
class PendingApproval:
    """Pending human-in-loop approval request."""

    approval_id: str
    tool: str
    command: str
    rule_pattern: str
    created_at: float
    timeout_sec: float
    status: str = "pending"
    decision: str = ""
    decided_at: float | None = None


@dataclass
class InterceptVerdict:
    """Result of evaluating a tool call."""

    action: str
    message: str = ""
    approval_id: str = ""
    rule_pattern: str = ""


def builtin_rules() -> list[InterceptRule]:
    """Return the default destructive and exfiltration guard rules."""
    return [
        InterceptRule(pattern=r"rm\s+-rf\s+/", action="ask", priority=100,
                      message="Destructive filesystem wipe requires approval.",
                      is_regex=True, builtin=True),
        InterceptRule(pattern=r"mkfs|dd\s+if=.*of=/dev/", action="ask", priority=100,
                      message="Disk destructive operation requires approval.",
                      is_regex=True, builtin=True),
        InterceptRule(pattern=r"shutdown|reboot|halt|poweroff|fork.{0,8}bomb|: ?\(\ ?\) ?\{",
                      action="ask", priority=100,
                      message="Host-destructive operation requires approval.",
                      is_regex=True, builtin=True),
        InterceptRule(pattern=r">\s*/dev/sd[a-z]|>\s*/dev/nvme|of=/dev/",
                      action="ask", priority=100,
                      message="Raw-disk write requires approval.",
                      is_regex=True, builtin=True),
        InterceptRule(pattern=r"curl|wget.*\|.*sh|bash\s+-c.*curl", action="ask",
                      priority=90, message="Remote pipe-to-shell requires approval.",
                      is_regex=True, builtin=True),
        InterceptRule(pattern="mimikatz", action="ask", priority=80,
                      message="Credential dumping requires approval."),
        InterceptRule(pattern="secretsdump", action="ask", priority=80,
                      message="Credential dumping requires approval."),
    ]


GLOBAL_SCOPE_DENY = (".gov", ".gov.cn", ".edu", ".edu.cn", ".mil")


def scope_blocked(target: str) -> str:
    """Return the matching global scope suffix or empty (LAZY parity)."""
    low = str(target or "").strip().lower()
    for suffix in GLOBAL_SCOPE_DENY:
        if low == suffix.lstrip(".") or low.endswith(suffix):
            return suffix
    return ""


_BLOCKED_RE = re.compile(r"403|forbidden|waf|blocked|denied|captcha|429", re.IGNORECASE)
_ERROR_RE = re.compile(r"error|failed|traceback|refused|timeout|no such", re.IGNORECASE)


def observe_post_tool(output: str) -> str:
    """Classify post-execution output (LAZY Guard.postToolUse parity)."""
    text = str(output or "")
    if _BLOCKED_RE.search(text):
        return "blocked"
    if _ERROR_RE.search(text):
        return "error"
    return "ok"


class Interceptor:
    """Evaluate tool calls against prioritized user rules."""

    def __init__(self, rules: list[InterceptRule] | None = None,
                 ask_timeout_sec: float = DEFAULT_ASK_TIMEOUT_SEC,
                 timeout_action: str = "deny") -> None:
        """Initialize with rules sorted by descending priority."""
        if str(timeout_action or "").lower() not in ("deny", "allow"):
            raise ValueError("timeout_action must be deny or allow.")
        self._lock = threading.Lock()
        self._rules: list[InterceptRule] = sorted(
            list(rules) if rules else builtin_rules(),
            key=lambda r: r.priority, reverse=True)
        self._pending: dict[str, PendingApproval] = {}
        self._ask_timeout_sec = float(ask_timeout_sec)
        self._timeout_action = str(timeout_action).lower()

    @property
    def rules(self) -> list[InterceptRule]:
        """Return a copy of the active rule list."""
        with self._lock:
            return list(self._rules)

    def add_rule(self, rule: InterceptRule) -> None:
        """Add a rule and keep priority ordering."""
        with self._lock:
            self._rules.append(rule)
            self._rules.sort(key=lambda r: r.priority, reverse=True)

    def remove_rule(self, pattern: str) -> bool:
        """Remove the first rule matching pattern text."""
        with self._lock:
            for rule in self._rules:
                if rule.pattern == pattern:
                    self._rules.remove(rule)
                    return True
        return False

    def evaluate(self, tool: str, command: str = "") -> InterceptVerdict:
        """Evaluate a tool call and return the verdict."""
        safe_tool = str(tool or "")
        safe_command = str(command or "")
        with self._lock:
            for rule in self._rules:
                if rule.matches(safe_tool, safe_command):
                    if rule.action == InterceptAction.ALLOW.value:
                        return InterceptVerdict(action="allow", rule_pattern=rule.pattern)
                    if rule.action == InterceptAction.DENY.value:
                        return InterceptVerdict(
                            action="deny",
                            message=rule.message or DEFAULT_DENY_MESSAGE,
                            rule_pattern=rule.pattern)
                    approval = PendingApproval(
                        approval_id=uuid.uuid4().hex[:12],
                        tool=safe_tool, command=safe_command,
                        rule_pattern=rule.pattern,
                        created_at=time.time(),
                        timeout_sec=self._ask_timeout_sec)
                    self._pending[approval.approval_id] = approval
                    return InterceptVerdict(
                        action="ask",
                        message=rule.message or DEFAULT_ASK_MESSAGE,
                        approval_id=approval.approval_id,
                        rule_pattern=rule.pattern)
            return InterceptVerdict(action="allow")

    def decide(self, approval_id: str, decision: str) -> bool:
        """Resolve a pending approval with approve or deny."""
        normalized = str(decision or "").lower()
        if normalized not in ("approve", "deny"):
            raise ValueError("Decision must be approve or deny.")
        with self._lock:
            pending = self._pending.get(str(approval_id))
            if pending is None or pending.status != "pending":
                return False
            pending.status = "decided"
            pending.decision = normalized
            pending.decided_at = time.time()
            return True

    def pending_approvals(self) -> list[PendingApproval]:
        """List unresolved approvals, expiring timed-out ones per policy."""
        now = time.time()
        with self._lock:
            result = []
            for pending in self._pending.values():
                if pending.status == "pending":
                    if now - pending.created_at > pending.timeout_sec:
                        pending.status = "expired"
                        pending.decision = self._timeout_action
                        pending.decided_at = now
                    else:
                        result.append(pending)
            return list(result)

    def approval_status(self, approval_id: str) -> PendingApproval | None:
        """Fetch a single approval record by id."""
        with self._lock:
            return self._pending.get(str(approval_id))


class Guard:
    """Audit every gated tool call and attribute failures."""

    def __init__(self, interceptor: Interceptor | None = None) -> None:
        """Initialize audit log with an optional interceptor."""
        self._lock = threading.Lock()
        self._interceptor = interceptor or Interceptor()
        self._audit: list[dict[str, Any]] = []
        self._attribution: dict[str, int] = {}

    @property
    def interceptor(self) -> Interceptor:
        """Expose the underlying interceptor."""
        return self._interceptor

    def check(self, tool: str, command: str = "") -> InterceptVerdict:
        """Audit the call then evaluate intercept rules (trace id kept)."""
        verdict = self._interceptor.evaluate(tool, command)
        entry = {"ts": time.time(), "tool": str(tool),
                 "command": str(command or "")[:2000],
                 "action": verdict.action, "rule": verdict.rule_pattern,
                 "trace_id": verdict.approval_id or uuid.uuid4().hex[:12]}
        with self._lock:
            self._audit.append(entry)
            self._audit = self._audit[-2000:]
        return verdict

    def observe(self, output: str, source: str = "") -> str:
        """Classify output and attribute blocked/error counters."""
        outcome = observe_post_tool(output)
        with self._lock:
            if outcome in ("blocked", "error"):
                key = str(source or outcome)
                self._attribution[key] = self._attribution.get(key, 0) + 1
        return outcome

    def record_failure(self, source: str) -> None:
        """Attribute a post-execution failure to a source."""
        with self._lock:
            self._attribution[str(source)] = self._attribution.get(str(source), 0) + 1

    def audit_log(self, limit: int = 200) -> list[dict[str, Any]]:
        """Return the most recent audit entries."""
        with self._lock:
            return list(self._audit[-max(1, int(limit)):])

    def attribution(self) -> dict[str, int]:
        """Return failure attribution counters."""
        with self._lock:
            return dict(self._attribution)
