"""Authorization scope guard for offensive command execution.

A red-team framework that reads its target from ``payload.json`` has a sharp
edge: if the operator leaves ``rhost`` pointing at the wrong machine, every
offensive command fires at an unauthorized host. That is an engagement
incident, not a cosmetic bug. This module is the safety net.

The guard answers a single question before a command runs: *is the active
target inside the authorized engagement scope for this (potentially offensive)
command?* It is deliberately conservative and fail-open so it never breaks an
existing workflow:

* When the enforcement mode is ``off`` it is a no-op.
* When no scope is configured it allows everything (you cannot enforce a scope
  that was never defined), so operators who never touch the feature see no
  change at all.
* When the command is not classified as offensive (reporting, configuration,
  local helpers) it allows it.
* When the target is empty it allows it (nothing to check).

Only when an *offensive* command targets a host *outside* a *defined* scope does
the guard react, and even then ``warn`` mode merely annotates the decision
while ``enforce`` mode blocks pending operator confirmation.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py`` (Dependency Inversion);
      the shell depends on this module, never the reverse.
    - The offensive/benign classification is pure data
      (:data:`OFFENSIVE_CATEGORIES`) plus a pure function
      (:func:`build_offensive_commands`), so it is unit-testable without a live
      cmd2 shell. A drift test pins the category strings against
      ``utils.py``.
    - Scope matching understands CIDR networks, bare IPs and hostnames
      (including ``*.`` wildcards) via the standard library only.
    - Every decision is a value object (:class:`ScopeDecision`) carrying the
      reason, so the caller owns all rendering and prompting.
"""

from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Mapping, Sequence

OFFENSIVE_CATEGORIES: frozenset[str] = frozenset(
    {
        "01. Reconnaissance",
        "02. Scanning & Enumeration",
        "03. Exploitation",
        "04. Post-Exploitation",
        "05. Persistence",
        "06. Privilege Escalation",
        "07. Credential Access",
        "08. Lateral Movement",
        "09. Data Exfiltration",
        "15. Pwntomate Tools",
        "15. Adversary YAML.",
    }
)
"""Kill-chain categories whose commands generate traffic to or act upon the
target. Membership drives the scope guard. Local-only surfaces (Command &
Control infrastructure, Reporting, Miscellaneous) are intentionally excluded so
the guard never interferes with payload generation, report writing or
configuration."""


class ScopeMode(str, Enum):
    """Enforcement posture for the scope guard.

    Attributes:
        OFF: The guard is disabled and always allows.
        WARN: Out-of-scope offensive commands are allowed but annotated.
        ENFORCE: Out-of-scope offensive commands are blocked pending
            confirmation.
    """

    OFF = "off"
    WARN = "warn"
    ENFORCE = "enforce"

    @classmethod
    def from_value(cls, value: object) -> ScopeMode:
        """Coerce an arbitrary payload value into a :class:`ScopeMode`.

        Args:
            value: A :class:`ScopeMode`, a mode string, or anything else.

        Returns:
            The matching mode, defaulting to :attr:`WARN` for unknown input so
            a typo never silently disables the guard.
        """
        if isinstance(value, ScopeMode):
            return value
        text = str(value or "").strip().lower()
        for mode in cls:
            if mode.value == text:
                return mode
        return cls.WARN


@dataclass(frozen=True)
class ScopeDecision:
    """Outcome of a single scope evaluation.

    Attributes:
        allowed: Whether the command may proceed without confirmation.
        needs_confirmation: Whether the caller must obtain explicit operator
            confirmation before proceeding (only set in ``enforce`` mode).
        reason: Human-readable explanation, empty when the command is allowed
            for an uninteresting reason (mode off, no scope, benign command).
        target: The target the decision was made against.
        command: The command the decision was made against.
        mode: The enforcement mode in effect when the decision was made.
    """

    allowed: bool
    needs_confirmation: bool
    reason: str
    target: str
    command: str
    mode: ScopeMode


def build_offensive_commands(
    command_categories: Mapping[str, object],
) -> frozenset[str]:
    """Select the command names whose category is offensive.

    Args:
        command_categories: Mapping of command name to its cmd2 help category
            (or ``None`` for uncategorised commands).

    Returns:
        The frozenset of command names that belong to
        :data:`OFFENSIVE_CATEGORIES`.
    """
    return frozenset(name for name, category in command_categories.items() if category in OFFENSIVE_CATEGORIES)


def normalize_scope(entries: object) -> tuple[str, ...]:
    """Coerce a scope specification into a tuple of entry strings.

    Accepts the canonical list form stored in ``payload.json`` as well as the
    string forms an operator might produce via ``assign`` (a JSON array, or a
    comma/space separated list), so the guard is robust to either source.

    Args:
        entries: A list/tuple/set of entries, a string, or ``None``.

    Returns:
        A tuple of non-empty, stripped entry strings.
    """
    if entries is None:
        return ()
    if isinstance(entries, str):
        text = entries.strip()
        if not text:
            return ()
        try:
            parsed = json.loads(text)
        except (ValueError, TypeError):
            parsed = None
        if isinstance(parsed, list):
            return tuple(str(item).strip() for item in parsed if str(item).strip())
        parts = [part.strip() for part in text.replace(",", " ").split()]
        return tuple(part for part in parts if part)
    if isinstance(entries, (list, tuple, set)):
        return tuple(str(item).strip() for item in entries if str(item).strip())
    return ()


def _parse_ip(value: str) -> ipaddress._BaseAddress | None:
    try:
        return ipaddress.ip_address(value)
    except ValueError:
        return None


def _parse_network(value: str) -> ipaddress._BaseNetwork | None:
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError:
        return None


def _hostname_match(target: str, entry: str) -> bool:
    normalized_target = target.lower().rstrip(".")
    normalized_entry = entry.lower().rstrip(".")
    if normalized_entry.startswith("*."):
        bare = normalized_entry[2:]
        return normalized_target == bare or normalized_target.endswith("." + bare)
    return normalized_target == normalized_entry or normalized_target.endswith("." + normalized_entry)


def target_in_scope(target: str, entries: Sequence[str]) -> bool:
    """Return whether *target* falls within any of the scope *entries*.

    IP targets are matched against CIDR networks and bare IP entries; hostname
    targets are matched against hostname entries (supporting a leading ``*.``
    wildcard for subdomains). Cross-kind comparisons (IP target vs hostname
    entry, or vice versa) never match because resolving them would require DNS,
    which the guard deliberately avoids.

    Args:
        target: The active target (IP address or hostname).
        entries: Authorized scope entries.

    Returns:
        ``True`` when the target is authorized by at least one entry.
    """
    target = (target or "").strip()
    if not target:
        return False
    parsed_target = _parse_ip(target)
    for raw in entries:
        entry = raw.strip()
        if not entry:
            continue
        if entry == target:
            return True
        network = _parse_network(entry)
        if network is not None:
            if parsed_target is not None and parsed_target in network:
                return True
            continue
        if parsed_target is None and _hostname_match(target, entry):
            return True
    return False


class ScopeGuard:
    """Decides whether an offensive command may run against the active target.

    The guard is cheap to construct and holds no mutable state, so the shell
    can build a fresh instance per command with the current payload values;
    this guarantees mid-session changes to the scope or the enforcement mode
    take effect immediately.
    """

    def __init__(
        self,
        scope_entries: object,
        mode: object,
        is_offensive: Callable[[str], bool],
    ) -> None:
        """Initialise the guard.

        Args:
            scope_entries: The authorized scope, in any form accepted by
                :func:`normalize_scope`.
            mode: The enforcement mode, in any form accepted by
                :meth:`ScopeMode.from_value`.
            is_offensive: Predicate returning ``True`` when a command name is
                offensive. Injected so the guard never imports the shell.
        """
        self.entries = normalize_scope(scope_entries)
        self.mode = ScopeMode.from_value(mode)
        self._is_offensive = is_offensive

    def evaluate(self, command: str, target: str) -> ScopeDecision:
        """Evaluate a single command against the active target.

        Args:
            command: The command name about to run.
            target: The active target (``rhost``).

        Returns:
            A :class:`ScopeDecision`. The guard fails open: any classification
            error is treated as benign so a bug here never blocks the operator.
        """
        command = (command or "").strip()
        target = (target or "").strip()
        allow = ScopeDecision(True, False, "", target, command, self.mode)
        if self.mode is ScopeMode.OFF:
            return allow
        if not self.entries:
            return allow
        try:
            offensive = bool(self._is_offensive(command))
        except Exception:
            offensive = False
        if not offensive:
            return allow
        if not target:
            return allow
        if target_in_scope(target, self.entries):
            return allow
        reason = (
            f"Target {target!r} is OUTSIDE the authorized scope for offensive "
            f"command {command!r}. Authorized scope: {', '.join(self.entries)}."
        )
        if self.mode is ScopeMode.WARN:
            return ScopeDecision(True, False, reason, target, command, self.mode)
        return ScopeDecision(False, True, reason, target, command, self.mode)


__all__ = [
    "OFFENSIVE_CATEGORIES",
    "ScopeMode",
    "ScopeDecision",
    "ScopeGuard",
    "build_offensive_commands",
    "normalize_scope",
    "target_in_scope",
]
