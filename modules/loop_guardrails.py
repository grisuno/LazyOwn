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
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

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
    """Sliding-window detector for identical repeated commands.

    Args:
        window: How many recent commands to watch.
    """

    def __init__(self, window: int = DEFAULT_REPEAT_WINDOW) -> None:
        self._window = max(2, int(window))
        self._recent: deque[str] = deque(maxlen=self._window)

    def record(self, command: str) -> bool:
        """Add one executed command; returns True when the window fills.

        Args:
            command: Exact command line as executed.

        Returns:
            True when the last ``window`` recorded commands are all
            identical (stuck loop signal).
        """
        text = (command or "").strip()
        if not text:
            return False
        self._recent.append(text)
        return self.stuck

    @property
    def stuck(self) -> bool:
        """True when the window is full of one identical command."""
        if len(self._recent) < self._window:
            return False
        first = self._recent[0]
        return all(entry == first for entry in self._recent)

    def last_commands(self) -> list[str]:
        """Snapshot of the recent command window (oldest first)."""
        return list(self._recent)

    def reset(self) -> None:
        """Clear the window (operator intervention acknowledged)."""
        self._recent.clear()


class EdrPacer:
    """Defense-aware pacing driven by observed execution anomalies.

    The pacer never blocks by itself: it only recommends. ``observe``
    feeds one executed command with its wall-clock duration and output;
    the internal score decays over time so a single anomaly does not
    permanently slow the loop.
    """

    def __init__(self, duration_threshold: float = _EDR_DURATION_THRESHOLD_SEC) -> None:
        self._threshold = max(1.0, float(duration_threshold))
        self._score = 0.0
        self._last_signal = ""
        self._lock = threading.Lock()

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

    def inter_step_delay(self) -> float:
        """Recommended sleep before the next step at the current level."""
        level = self.level
        if level not in _PAUSE_RANGES:
            return 0.0
        low, high = _PAUSE_RANGES[level]
        return random.uniform(low, high)

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


__all__ = [
    "DEFAULT_REPEAT_WINDOW",
    "DEFAULT_TARGET_LIMIT",
    "EdrPacer",
    "FactVectorStore",
    "RepeatDetector",
    "TargetLimiter",
]
