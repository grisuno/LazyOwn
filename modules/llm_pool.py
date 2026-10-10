"""Ordered LLM failover pool with health-aware skipping.

Ports the LAZY llmpool contract. Members form a priority chain with
the active profile heading. Failover happens only before the first
token. Mid-stream failures surface unchanged for harness resume.
"""

from __future__ import annotations

import itertools
import threading
import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True, slots=True)
class PoolConfig:
    """Centralized constants for pool behavior (LAZY llmpool parity)."""

    unhealthy_cooldown_sec: float = 300.0
    max_failures: int = 3
    backoff_sec: tuple = (60.0, 300.0, 1800.0)
    max_output_chars: int = 30000
    overflow_dirname: str = "cmd-output"


CONFIG = PoolConfig()


class PoolExhausted(RuntimeError):
    """Raised when every pool member fails a request."""


_SHARED_HEALTH: HealthRegistry | None = None
_SHARED_LOCK = threading.Lock()


def shared_registry(config: PoolConfig = CONFIG) -> HealthRegistry:
    """Return the process-wide health registry (LAZY Registry parity).

    Breaker state survives pool rebuilds so repeated failures across
    suggestions trip the breaker instead of resetting each call.
    """
    global _SHARED_HEALTH
    with _SHARED_LOCK:
        if _SHARED_HEALTH is None:
            _SHARED_HEALTH = HealthRegistry(config)
        return _SHARED_HEALTH


@dataclass
class PoolMember:
    """Single provider in the failover chain."""

    member_id: str
    name: str
    model: str
    rank: int
    complete: Callable[[str], str] = field(repr=False, compare=False)
    window_tokens: int = 0


class HealthRegistry:
    """Failure counting registry with tiered backoff (LAZY parity).

    Soft trips after max_failures transient errors; auth errors
    (401/402/quota) trip immediately. Backoff tiers are 1m/5m/30m.
    """

    def __init__(self, config: PoolConfig = CONFIG) -> None:
        """Initialize empty health counters."""
        self._config = config
        self._lock = threading.Lock()
        self._failures: dict[str, int] = {}
        self._last_failure: dict[str, float] = {}
        self._hard_trip: dict[str, float] = {}

    def report_success(self, member_id: str) -> None:
        """Clear failure state for a member."""
        with self._lock:
            self._failures.pop(str(member_id), None)
            self._last_failure.pop(str(member_id), None)
            self._hard_trip.pop(str(member_id), None)

    def report_failure(self, member_id: str, error: str = "") -> None:
        """Record a failure; auth/quota errors trip immediately."""
        lowered = str(error or "").lower()
        immediate = any(k in lowered for k in ("401", "402", "unauthorized",
                                               "quota", "insufficient"))
        with self._lock:
            key = str(member_id)
            if immediate:
                self._hard_trip[key] = time.time()
            self._failures[key] = self._failures.get(key, 0) + 1
            self._last_failure[key] = time.time()

    def _backoff_for(self, failures: int) -> float:
        """Return the backoff tier for a failure count."""
        tiers = self._config.backoff_sec
        if failures <= 0:
            return 0.0
        idx = min(failures - self._config.max_failures, len(tiers) - 1)
        return float(tiers[max(0, idx)])

    def healthy(self, member_id: str) -> bool:
        """Return True when a member may serve traffic."""
        with self._lock:
            key = str(member_id)
            failures = self._failures.get(key, 0)
            if failures < self._config.max_failures and key not in self._hard_trip:
                return True
            last = self._last_failure.get(key, 0.0)
            if key in self._hard_trip:
                last = max(last, self._hard_trip.get(key, 0.0))
            return (time.time() - last) >= self._backoff_for(max(failures, self._config.max_failures))


class LLMPool:
    """Failover chain over ordered pool members with RR intra-rank."""

    def __init__(self, members: list[PoolMember],
                 health: HealthRegistry | None = None,
                 config: PoolConfig = CONFIG) -> None:
        """Order members by descending rank (RR within equal rank)."""
        if not members:
            raise ValueError("Pool requires at least one member.")
        self._members = sorted(list(members),
                               key=lambda m: m.rank, reverse=True)
        self._health = health or HealthRegistry(config)
        self._config = config
        self._cursor = itertools.count()
        self._lock = threading.Lock()

    @property
    def members(self) -> list[PoolMember]:
        """Return chain members in order."""
        return list(self._members)

    def session_key(self, conversation_id: str = "", role: str = "worker",
                    index: int = 0) -> str:
        """Build a sticky session header (LAZY session_header parity)."""
        conv = str(conversation_id or "default").strip() or "default"
        return f"conv-{conv}-{role}-{index}"

    def _ordered(self) -> list[PoolMember]:
        """Active-first, rank DESC, round-robin within equal rank."""
        with self._lock:
            tick = next(self._cursor)
        groups: dict[int, list[PoolMember]] = {}
        for member in self._members:
            groups.setdefault(member.rank, []).append(member)
        ordered: list[PoolMember] = []
        for rank in sorted(groups, reverse=True):
            group = groups[rank]
            if len(group) > 1:
                offset = tick % len(group)
                group = group[offset:] + group[:offset]
            ordered.extend(group)
        return ordered

    def _truncate(self, text: str, overflow_dir: str = "") -> str:
        """Cap output at max_output_chars, spilling to a file when set."""
        limit = self._config.max_output_chars
        if limit <= 0 or len(text) <= limit:
            return text
        if overflow_dir:
            try:
                from pathlib import Path as _Path
                import hashlib as _hashlib
                import time as _time
                target = _Path(str(overflow_dir)) / self._config.overflow_dirname
                target.mkdir(parents=True, exist_ok=True)
                name = f"llm-{int(_time.time())}-{_hashlib.sha256(text.encode()).hexdigest()[:8]}.txt"
                (target / name).write_text(text, encoding="utf-8")
                return text[:limit] + f"\n[... truncated, full output in {name}]"
            except Exception:
                pass
        return text[:limit] + "\n[... truncated]"

    def complete(self, prompt: str, max_tokens: int = 0,
                 session_key: str = "", overflow_dir: str = "") -> str:
        """Complete a prompt with pre-token failover across members."""
        errors: list[str] = []
        for member in self._ordered():
            if member.window_tokens and max_tokens and \
                    member.window_tokens < max_tokens:
                continue
            if not self._health.healthy(member.member_id):
                continue
            try:
                try:
                    result = member.complete(str(prompt), session_key=session_key)
                except TypeError:
                    result = member.complete(str(prompt))
                self._health.report_success(member.member_id)
                return self._truncate(str(result), overflow_dir)
            except Exception as exc:
                self._health.report_failure(member.member_id, str(exc))
                errors.append(f"{member.name}: {exc}")
        raise PoolExhausted(f"All providers failed: {'; '.join(errors)}")
