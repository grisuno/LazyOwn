"""Adaptive guardrails for the autonomous loop.

Four independent primitives, one contract each:

- :class:`RepeatDetector`: sliding window over the last executed
  commands; ``stuck`` flips when the window fills with identical
  commands, which is the operator-visible signal that the planner is
  going in circles.
- :class:`EdrPacer`: observes per-command duration and output
  anomalies (high latency, connection resets, timeouts) and estimates
  a defense-telemetry level. At higher levels the loop inserts random
  inter-step sleeps and downgrades noisy verbs to quieter variants
  instead of burning bandwidth and blue-team attention.
- :class:`TargetLimiter`: semaphore that caps how many distinct
  targets the loop attacks simultaneously; per-thread re-entrant so a
  worker touching one target across many steps never self-deadlocks.
- :class:`FactVectorStore`: stdlib TF-IDF vector memory. Facts
  (command plus output digests) are embedded on write and retrieved by
  cosine similarity so the LLM context carries only the facts relevant
  to the current query instead of the whole transcript.

All four are persistence-friendly, exception-tolerant and safe to call
from worker threads.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import tempfile
import threading
import time
from collections import deque
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_REPEAT_WINDOW = 5
DEFAULT_TARGET_LIMIT = 3
DEFAULT_MAX_TARGETS = 16
DEFAULT_MAX_FACTS = 500
DEFAULT_SEARCH_RESULTS = 5

_EDR_DURATION_THRESHOLD_SEC = 30.0
_EDR_RESET_PATTERNS = ("connection reset", "reset by peer", "host seems down", "timed out")
_EDR_HIGH_SIGNAL_SCORE = 2.0
_EDR_SIGNAL_WEIGHT = 2.0
_EDR_DECAY = 0.5
_PAUSE_RANGES = {1: (2.0, 5.0), 2: (5.0, 15.0)}
_PAUSE_MAX_DELAY_SEC = 300.0
_SLEEPER_WINDOW_RE = re.compile(r"^(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})$")

_FALLBACK_PACING_LOCAL: dict[str, Any] = {
    "enabled": True,
    "jitter_pct_min": 0.0,
    "jitter_pct_max": 0.0,
    "edr_pause_ranges": _PAUSE_RANGES,
    "max_delay_sec": _PAUSE_MAX_DELAY_SEC,
    "sleeper_windows": (),
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOPWORDS = frozenset(
    {
        "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "is",
        "was", "at", "by", "from", "as", "it", "be", "this", "that", "are", "not",
    }
)

_QUIET_RULES: tuple[tuple[re.Pattern, str, int], ...] = (
    (re.compile(r"nmap\s+-sS\b"), "nmap -sT -T2", 1),
    (re.compile(r"nmap\s+-sV\b"), "nmap -sV --version-light -T2", 1),
    (re.compile(r"nmap\s+-A\b"), "nmap -sV -T2", 2),
    (re.compile(r"nmap\s+-T[45]\b"), "nmap -T2", 1),
    (re.compile(r"(?<![\w-])nikto\b"), "nikto -Tuning 123", 2),
)


@dataclass
class Fact:
    """One stored fact with its sparse TF-IDF vector."""

    text: str
    meta: dict = field(default_factory=dict)
    ts: float = 0.0
    tokens: dict[str, float] = field(default_factory=dict)


class RepeatDetector:
    """Sliding-window detector for identical, alternating and cyclic repeats.

    Three stuck-loop shapes are recognised:

    - AAAA: every command in the window is identical.
    - ABABAB: the window alternates between exactly two commands with at
      least two repetitions each, the oscillation the legacy loop vetoed.
    - ABCDEF twice: the newest ``2p`` entries are two identical rounds of
      a cycle of ``p >=`` :data:`_CYCLE_MIN_PERIOD` distinct commands — the
      shape a full recon family produces round after round, where no pair
      ever alternates and no window is all-identical.

    Args:
        window: How many recent commands a single stuck shape may span.
            The internal ring holds twice that so a cycle of up to
            ``window`` commands can be caught over two full rounds.
    """

    _OSCILLATION_MIN = 6
    _CYCLE_MIN_PERIOD = 3

    def __init__(self, window: int = DEFAULT_REPEAT_WINDOW) -> None:
        self._window = max(2, int(window))
        ring = max(self._window * 2, self._window)
        self._recent: deque[str] = deque(maxlen=ring)
        self._oscillation_a = ""
        self._oscillation_b = ""
        self._cycle: tuple[str, ...] = ()

    def record(self, command: str) -> bool:
        """Add one executed command; returns True when the window fills.

        Args:
            command: Exact command line as executed.

        Returns:
            True when a stuck-loop shape fills the window.
        """
        text = (command or "").strip()
        if not text:
            return False
        self._recent.append(text)
        self._update_oscillation()
        self._cycle = self._periodic_cycle(list(self._recent))
        return self.stuck

    def _update_oscillation(self) -> None:
        """Refresh the detected alternating pair, if any."""
        entries = list(self._recent)
        if (
            len(entries) < self._OSCILLATION_MIN
            or len(set(entries)) != 2
            or not self._strict_alternating(entries)
        ):
            self._oscillation_a = ""
            self._oscillation_b = ""
            return
        self._oscillation_a, self._oscillation_b = entries[0], entries[1]

    @staticmethod
    def _strict_alternating(entries: list[str]) -> bool:
        """Return True when consecutive entries always differ."""
        return all(entries[i] != entries[i + 1] for i in range(len(entries) - 1))

    @staticmethod
    def _periodic_cycle(entries: list[str]) -> tuple[str, ...]:
        """Return the repeating command block over two identical rounds.

        Args:
            entries: Recent commands, oldest first.

        Returns:
            The repeating cycle block (length >= ``_CYCLE_MIN_PERIOD``,
            at least three distinct commands) or an empty tuple when the
            newest records are not two identical rounds of one cycle.
        """
        for period in range(len(entries) // 2, RepeatDetector._CYCLE_MIN_PERIOD - 1, -1):
            recent = entries[-period * 2 :]
            first, second = recent[:period], recent[period:]
            if len(set(second)) < RepeatDetector._CYCLE_MIN_PERIOD:
                continue
            if first == second:
                return tuple(second)
        return ()

    @property
    def stuck(self) -> bool:
        """True when the loop is visibly not progressing.

        One of: an all-identical window (AAAA), a two-command
        oscillation (ABABAB), or two identical rounds of a cycle of at
        least three distinct commands (ABCDEF twice).
        """
        entries = list(self._recent)
        if len(entries) < 2:
            return False
        if self._periodic_cycle(entries):
            return True
        if len(entries) >= self._OSCILLATION_MIN and self._alternating():
            return True
        if all(entry == entries[0] for entry in entries):
            return len(entries) >= self._window
        return False

    def describe(self) -> str:
        """Human sentence of the stuck shape for activity lines."""
        entries = list(self._recent)
        if self._cycle:
            block = " -> ".join(command[:60] for command in self._cycle)
            return f"a cycle of {len(self._cycle)} commands x2: {block}"
        if self._alternating():
            return f"alternating between {self._oscillation_a[:60]!r} and {self._oscillation_b[:60]!r}"
        if entries and all(entry == entries[0] for entry in entries):
            return f"the same command {entries[0][:100]!r}"
        if entries[0:]:
            return f"{entries[0][:100]!r}"
        return "repeating steps"

    def _alternating(self) -> bool:
        """True when the window holds an exact two-command oscillation."""
        return (
            self._oscillation_a != ""
            and self._oscillation_b != ""
            and self._oscillation_a != self._oscillation_b
        )

    def oscillation_pair(self) -> tuple[str, str]:
        """Return the detected alternating pair, ('', '') when none."""
        return self._oscillation_a, self._oscillation_b

    def cycle(self) -> tuple[str, ...]:
        """Return the detected repeating block, empty when none."""
        return self._cycle

    def last_commands(self) -> list[str]:
        """Snapshot of the recent command window (oldest first)."""
        return list(self._recent)

    def reset(self) -> None:
        """Clear the window (operator intervention acknowledged)."""
        self._recent.clear()
        self._oscillation_a = ""
        self._oscillation_b = ""
        self._cycle = ()


class EdrPacer:
    """Defense-aware pacing driven by observed execution anomalies.

    The pacer never blocks by itself: it only recommends. ``observe``
    feeds one executed command with its wall-clock duration and output;
    the internal score decays over time so a single anomaly does not
    permanently slow the loop.

    Delays are fully configurable through the orchestrator ``pacing``
    block (see ``orchestrator_config.pacing``): per-level quiet ranges,
    a jitter percentage applied to every drawn delay and ``HH:MM-HH:MM``
    sleeper windows during which the recommended delay extends to the
    window end (clamped to ``max_delay_sec`` so callers re-check the
    window instead of oversleeping a cancellation).
    """

    def __init__(
        self,
        duration_threshold: float = _EDR_DURATION_THRESHOLD_SEC,
        *,
        pause_ranges: dict[int, tuple[float, float]] | None = None,
        jitter_pct: tuple[float, float] = (0.0, 0.0),
        max_delay_sec: float = _PAUSE_MAX_DELAY_SEC,
        sleeper_windows: tuple[str, ...] | list[str] = (),
        clock: Callable[[], float] | None = None,
        rng: Callable[[float, float], float] | None = None,
    ) -> None:
        """Configure the pacer.

        Args:
            duration_threshold: Seconds after which a step counts as slow.
            pause_ranges: Per-level ``(low, high)`` quiet ranges; None
                keeps the built-in table. An empty mapping disables
                level-based pauses entirely.
            jitter_pct: ``(min, max)`` percentage applied to every drawn
                pause, e.g. ``(-30, 60)`` shrinks or stretches the delay.
            max_delay_sec: Upper clamp for any recommended delay.
            sleeper_windows: ``HH:MM-HH:MM`` quiet windows (local time).
            clock: Injectable wall clock (epoch seconds) for tests.
            rng: Injectable ``uniform(low, high)`` sampler for tests.
        """
        self._threshold = max(1.0, float(duration_threshold))
        raw_ranges = dict(pause_ranges) if pause_ranges is not None else dict(_PAUSE_RANGES)
        self._pause_ranges: dict[int, tuple[float, float]] = {}
        for level, bounds in raw_ranges.items():
            try:
                low, high = float(bounds[0]), float(bounds[1])
            except (TypeError, ValueError, IndexError):
                continue
            if not isinstance(level, bool) and low >= 0 and high >= low:
                self._pause_ranges[int(level)] = (low, high)
        low_pct, high_pct = (float(jitter_pct[0]), float(jitter_pct[1]))
        self._jitter_pct = (min(low_pct, high_pct), max(low_pct, high_pct))
        self._max_delay = max(0.0, float(max_delay_sec))
        self._sleeper_windows = EdrPacer.parse_windows(sleeper_windows)
        self._clock = clock or time.time
        self._rng = rng or random.uniform
        self._score = 0.0
        self._last_signal = ""
        self._lock = threading.Lock()

    @staticmethod
    def parse_windows(raw: tuple[str, ...] | list[str] | None) -> tuple[tuple[int, int, int, int], ...]:
        """Parse ``HH:MM-HH:MM`` window strings into minute tuples.

        Args:
            raw: Raw window declarations; invalid entries are skipped.

        Returns:
            Tuples of ``(start_h, start_m, end_h, end_m)`` in 24h local
            time.
        """
        parsed: list[tuple[int, int, int, int]] = []
        for window in raw or ():
            match = _SLEEPER_WINDOW_RE.match(str(window).strip())
            if not match:
                continue
            start_h, start_m, end_h, end_m = (int(part) for part in match.groups())
            if start_h > 23 or end_h > 23 or start_m > 59 or end_m > 59:
                continue
            parsed.append((start_h, start_m, end_h, end_m))
        return tuple(parsed)

    @classmethod
    def from_config(cls, **overrides: Any) -> EdrPacer:
        """Build a pacer from the orchestrator pacing configuration.

        Args:
            overrides: Forwarded to the constructor verbatim, winning
                over the configuration (used by callers that clamp).

        Returns:
            A configured pacer; when the orchestrator config is absent
            or unreadable the built-in defaults apply, and
            ``pacing.enabled = false`` yields an inert pacer.
        """
        try:
            from modules import orchestrator_config

            config = orchestrator_config.pacing()
        except Exception:
            config: dict[str, Any] = dict(_FALLBACK_PACING_LOCAL)
        if not config.get("enabled", True):
            return cls(pause_ranges={}, sleeper_windows=(), max_delay_sec=0.0, **overrides)
        return cls(
            pause_ranges=dict(config.get("edr_pause_ranges") or _PAUSE_RANGES),
            jitter_pct=(
                float(config.get("jitter_pct_min", 0.0) or 0.0),
                float(config.get("jitter_pct_max", 0.0) or 0.0),
            ),
            max_delay_sec=float(config.get("max_delay_sec", _PAUSE_MAX_DELAY_SEC) or 0.0),
            sleeper_windows=tuple(config.get("sleeper_windows") or ()),
            **overrides,
        )

    def observe(self, command: str, duration_sec: float, output: str) -> None:
        """Feed one executed step and update the telemetry estimate.

        Args:
            command: Executed command line.
            duration_sec: Wall-clock seconds the command took.
            output: Captured output (scan for reset/timeout markers).
        """
        signals: list[str] = []
        lowered = (output or "").lower()
        if duration_sec >= self._threshold:
            signals.append(f"slow:{duration_sec:.0f}s")
        for pattern in _EDR_RESET_PATTERNS:
            if pattern in lowered:
                signals.append(f"reset:{pattern}")
                break
        if not signals:
            return
        with self._lock:
            self._score = min(_EDR_HIGH_SIGNAL_SCORE * 2, self._score + _EDR_SIGNAL_WEIGHT)
            self._last_signal = "; ".join(signals)

    def decay(self, factor: float = _EDR_DECAY) -> None:
        """Cool the estimate down (call once per completed step)."""
        with self._lock:
            self._score = max(0.0, self._score - abs(factor))

    @property
    def level(self) -> int:
        """Current pacing level: 0 calm, 1 cautious, 2 stealth."""
        with self._lock:
            if self._score >= _EDR_HIGH_SIGNAL_SCORE * 2:
                return 2
            if self._score >= _EDR_HIGH_SIGNAL_SCORE:
                return 1
            return 0

    @property
    def signal(self) -> str:
        """Human-readable reason for the current level (may be empty)."""
        with self._lock:
            return self._last_signal

    @staticmethod
    def _window_seconds_until_end(
        windows: tuple[tuple[int, int, int, int], ...], now: float | None
    ) -> float:
        """Return seconds until the active window ends (0 when outside).

        Windows may wrap midnight (``23:00-03:00``); a wrapped window
        matches when local time is after the start or before the end.
        """
        moment = time.localtime(now if now is not None else time.time())
        minutes_now = moment.tm_hour * 60 + moment.tm_min
        for start_h, start_m, end_h, end_m in windows:
            start = start_h * 60 + start_m
            end = end_h * 60 + end_m
            if start == end:
                continue
            if start < end:
                if not (start <= minutes_now < end):
                    continue
                return (end - minutes_now) * 60.0 - moment.tm_sec
            if minutes_now >= start:
                return (24 * 60 - minutes_now + end) * 60.0 - moment.tm_sec
            if minutes_now < end:
                return (end - minutes_now) * 60.0 - moment.tm_sec
        return 0.0

    def in_sleeper_window(self, now: float | None = None) -> bool:
        """True when local time falls inside a configured quiet window."""
        moment = self._clock() if now is None else now
        return self._window_seconds_until_end(self._sleeper_windows, moment) > 0.0

    @staticmethod
    def windows_delay(
        windows: tuple[str, ...] | list[str], now: float | None = None
    ) -> float:
        """Static quiet-window delay for callers without a pacer instance.

        Args:
            windows: ``HH:MM-HH:MM`` window declarations.
            now: Injectable epoch seconds (None uses the real clock).

        Returns:
            Seconds until the active window ends, clamped to the
            configured maximum; 0 when outside every window.
        """
        parsed = EdrPacer.parse_windows(windows)
        if not parsed:
            return 0.0
        try:
            from modules import orchestrator_config

            max_delay = float(orchestrator_config.pacing().get("max_delay_sec", _PAUSE_MAX_DELAY_SEC) or 0.0)
        except Exception:
            max_delay = _PAUSE_MAX_DELAY_SEC
        delay = EdrPacer._window_seconds_until_end(parsed, now)
        if delay <= 0.0:
            return 0.0
        return max(0.0, min(delay, max_delay)) if max_delay > 0 else delay

    def sleeper_delay(self, now: float | None = None) -> float:
        """Recommended sleep because of a quiet window (0 when outside).

        The delay is the time until the window end, clamped to
        ``max_delay_sec`` so long windows sleep in bounded chunks and
        every caller re-checks cancellation between chunks.
        """
        moment = self._clock() if now is None else now
        delay = self._window_seconds_until_end(self._sleeper_windows, moment)
        if delay <= 0.0:
            return 0.0
        return max(0.0, min(delay, self._max_delay)) if self._max_delay > 0 else delay

    def inter_step_delay(self) -> float:
        """Recommended sleep before the next step at the current level.

        Combines the level's quiet range (scaled by the configured
        jitter percentage) with the sleeper-window delay, taking the
        larger of the two and clamping to ``max_delay_sec``.
        """
        low, high = self._pause_ranges.get(self.level, (0.0, 0.0))
        delay = self._rng(low, high) if high > low else (low if low > 0 else 0.0)
        jmin, jmax = self._jitter_pct
        if delay > 0.0 and (jmin or jmax):
            delay *= 1.0 + (self._rng(jmin, jmax) / 100.0)
        delay = max(delay, self.sleeper_delay())
        if self._max_delay > 0:
            delay = min(delay, self._max_delay)
        return max(0.0, delay)

    def quieten(self, command: str) -> str:
        """Return a quieter variant of the command at the current level.

        Applies the first matching downgrade rule whose level threshold
        the current level meets; a level of 0 returns the input
        unchanged.
        """
        level = self.level
        if level <= 0:
            return command
        for pattern, replacement, required_level in _QUIET_RULES:
            if level >= required_level and pattern.search(command or ""):
                return pattern.sub(replacement, command, count=1)
        return command

    def describe(self) -> dict[str, Any]:
        """Return a snapshot of the pacer state for admin surfaces."""
        return {
            "level": self.level,
            "signal": self.signal,
            "jitter_pct": self._jitter_pct,
            "max_delay_sec": self._max_delay,
            "sleeper_windows": [
                f"{start_h:02d}:{start_m:02d}-{end_h:02d}:{end_m:02d}"
                for start_h, start_m, end_h, end_m in self._sleeper_windows
            ],
            "in_sleeper_window": self.in_sleeper_window(),
        }


class TargetLimiter:
    """Per-target concurrency cap shared by every loop worker.

    Args:
        max_concurrent: How many distinct targets may be worked at the
            same time (default 3).
    """

    def __init__(self, max_concurrent: int = DEFAULT_TARGET_LIMIT) -> None:
        self._max = max(1, int(max_concurrent))
        self._semaphore = threading.Semaphore(self._max)
        self._lock = threading.Lock()
        self._holders: dict[str, dict[int, int]] = {}

    @property
    def max_concurrent(self) -> int:
        """Configured upper bound of simultaneous targets."""
        return self._max

    @property
    def active_targets(self) -> int:
        """How many distinct targets currently hold a slot."""
        with self._lock:
            return len(self._holders)

    @contextmanager
    def slot(self, target: str):
        """Hold one of at most ``max_concurrent`` target slots.

        Re-entrant per thread: a worker already holding ``target``
        acquires nothing new, so sequencing many commands against one
        target never blocks on itself.

        Args:
            target: Target identifier (empty target bypasses the cap).
        """
        key = (target or "").strip()
        if not key:
            yield
            return
        thread_id = threading.get_ident()
        with self._lock:
            holders = self._holders.setdefault(key, {})
            if thread_id in holders:
                holders[thread_id] += 1
                nested = True
            else:
                nested = False
        if not nested:
            self._semaphore.acquire()
            with self._lock:
                self._holders.setdefault(key, {})[thread_id] = 1
        try:
            yield
        finally:
            with self._lock:
                holders = self._holders.get(key) or {}
                count = holders.get(thread_id, 0)
                if count > 1:
                    holders[thread_id] = count - 1
                    return_held = False
                else:
                    holders.pop(thread_id, None)
                    return_held = not nested and count == 1
                    if not holders:
                        self._holders.pop(key, None)
            if return_held:
                self._semaphore.release()


class FactVectorStore:
    """JSON-persisted TF-IDF fact memory with cosine retrieval.

    Pure stdlib: no chromadb, no FAISS, no embeddings service. Facts
    dedupe by content hash, persist atomically and trim to
    ``max_facts`` oldest-first.
    """

    def __init__(self, path: str | Path, max_facts: int = DEFAULT_MAX_FACTS) -> None:
        self._path = Path(path)
        self._max = max(16, int(max_facts))
        self._facts: list[Fact] = []
        self._lock = threading.Lock()
        self._load()

    @property
    def path(self) -> Path:
        """Backing file path."""
        return self._path

    def __len__(self) -> int:
        return len(self._facts)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Lowercase word tokens minus stopwords."""
        return [token for token in _TOKEN_RE.findall((text or "").lower()) if token not in _STOPWORDS]

    @staticmethod
    def _vectorize(tokens: list[str]) -> dict[str, float]:
        """Term-frequency vector over one document."""
        counts: dict[str, float] = {}
        for token in tokens:
            counts[token] = counts.get(token, 0.0) + 1.0
        total = math.sqrt(sum(weight * weight for weight in counts.values())) or 1.0
        return {token: weight / total for token, weight in counts.items()}

    def add(self, text: str, meta: dict | None = None) -> bool:
        """Embed and store one fact; returns False for duplicates.

        Args:
            text: Fact content (command plus output digest).
            meta: Optional metadata attached to the fact.

        Returns:
            True when a new fact was stored.
        """
        content = (text or "").strip()
        if len(content) < 8:
            return False
        digest = hashlib.sha1(content.encode("utf-8", errors="replace")).hexdigest()
        with self._lock:
            for fact in self._facts:
                if fact.meta.get("digest") == digest:
                    return False
            vectors = self._vectorize(self._tokenize(content))
            if not vectors:
                return False
            self._facts.append(
                Fact(
                    text=content[:2000],
                    meta={**(meta or {}), "digest": digest},
                    ts=time.time(),
                    tokens=vectors,
                )
            )
            if len(self._facts) > self._max:
                self._facts = self._facts[-self._max :]
        self.save()
        return True

    def search(self, query: str, k: int = DEFAULT_SEARCH_RESULTS) -> list[dict]:
        """Return the ``k`` facts most similar to the query.

        Args:
            query: Current goal or step context.
            k: Maximum results.

        Returns:
            List of ``{"text", "meta", "score"}`` dicts, best first.
        """
        query_vector = self._vectorize(self._tokenize(query or ""))
        if not query_vector:
            return []
        k = max(1, int(k))
        scored: list[tuple[float, Fact]] = []
        with self._lock:
            for fact in self._facts:
                score = 0.0
                for token, weight in query_vector.items():
                    other = fact.tokens.get(token)
                    if other is not None:
                        score += weight * other
                if score > 0.0:
                    scored.append((score, fact))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {"text": fact.text, "meta": dict(fact.meta), "score": round(score, 6)}
            for score, fact in scored[:k]
        ]

    def search_block(self, query: str, k: int = DEFAULT_SEARCH_RESULTS, max_chars: int = 1200) -> str:
        """Render retrieved facts as a prompt-ready block (may be empty)."""
        rows = self.search(query, k=k)
        if not rows:
            return ""
        lines = [f"- {row['text'][:200]}" for row in rows]
        block = "\n".join(lines)
        return block[:max_chars]

    def clear(self) -> None:
        """Drop every fact (manual reset path)."""
        with self._lock:
            self._facts = []
        self.save()

    def save(self) -> None:
        """Persist atomically; I/O errors never surface to the loop."""
        directory = self._path.parent
        try:
            directory.mkdir(parents=True, exist_ok=True)
            payload = {
                "facts": [
                    {"text": fact.text, "meta": fact.meta, "ts": fact.ts}
                    for fact in self._facts
                ]
            }
            fd, tmp_name = tempfile.mkstemp(dir=str(directory), prefix=".facts_")
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False)
            os.replace(tmp_name, self._path)
        except OSError:
            try:
                os.unlink(tmp_name)  # type: ignore[possibly-undefined]
            except (OSError, UnboundLocalError):
                pass

    def _load(self) -> None:
        if not self._path.is_file():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for item in payload.get("facts", []) or []:
            if not isinstance(item, dict):
                continue
            text = str(item.get("text", "")).strip()
            if not text:
                continue
            self._facts.append(
                Fact(
                    text=text,
                    meta=dict(item.get("meta") or {}),
                    ts=float(item.get("ts", 0.0) or 0.0),
                    tokens=self._vectorize(self._tokenize(text)),
                )
            )
        if len(self._facts) > self._max:
            self._facts = self._facts[-self._max :]


_LISTING_HEADS = frozenset({"ls", "dir", "du", "tree"})
_LISTING_MIN_LINES = 120
_LISTING_MAX_AVG_LINE = 80
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
_LISTING_LEGIT_FIND_FLAGS = (" -perm ", " -name ", " -exec ", " -ok ")
LS_REFUSAL = "listing command forbidden in the autonomous loop; the loop already knows its environment: use the structured verbs (auto_populate, facts_show, lazy_scope, lazy_traffic) or the guard evidence search"


def listing_forbidden(command: str) -> str:
    """Return the listing veto reason, empty when the command may run.

    Contract (operator policy): the autonomous loop never pages the
    operator filesystem. ``ls/dir/du/tree`` are rejected with any
    arguments; bare ``find`` is rejected too — only find chains with a
    post-exploitation filter (``-perm``/``-name``/``-exec``/``-ok``,
    SUID hunting and friends) pass. The call sites are the loop
    chokepoints; an operator terminal running LazyOwn itself is not
    affected.

    Args:
        command: The command line proposed by the model.

    Returns:
        Refusal text when the family is vetoed, otherwise ``""``.
    """
    head, _, rest = (str(command or "").strip()).partition(" ")
    stripped = head.lower().strip("-").strip("./")
    if stripped in _LISTING_HEADS:
        return LS_REFUSAL
    if stripped == "find":
        lowered = str(rest or "").lower()
        if not any(flag in lowered for flag in _LISTING_LEGIT_FIND_FLAGS):
            return LS_REFUSAL
    return ""


class ListingNoiseDetector:
    """Detect enumeration-only steps whose output carries no intel.

    An ``ls``/``dir``/``du``/``tree`` step whose output is one very long
    wall of path entries (a session-artifact inventory) is the shape
    behind a self-amplifying loop: the listing gets recorded as traffic,
    the recorder mirror writes new artifact files for it, and the next
    listing looks like fresh work. The detector only recommends; callers
    decide to settle the intent instead of feeding the wall back.
    """

    def observe(self, command: str, output: str) -> bool:
        """Return True when the step is a pure directory listing dump.

        Args:
            command: The executed command line; only the pure enumeration
                heads count (``ls/dir/du/tree``, bare ``find`` excluded
                because find chains often are real post-exploitation
                logic).
            output: Captured step output.

        Returns:
            True for a long listing-shaped wall, False otherwise.
        """
        head = (str(command or "").split() or [""])[0].lower().strip("./")
        if head not in _LISTING_HEADS:
            return False
        text = _ANSI_RE.sub("", str(output or ""))
        lines = [line for line in text.splitlines() if line.strip()]
        if len(lines) < _LISTING_MIN_LINES:
            return False
        average = sum(len(line) for line in lines) / len(lines)
        return average <= _LISTING_MAX_AVG_LINE


__all__ = [
    "DEFAULT_REPEAT_WINDOW",
    "EdrPacer",
    "Fact",
    "FactVectorStore",
    "ListingNoiseDetector",
    "RepeatDetector",
    "TargetLimiter",
    "listing_forbidden",
]
