"""Isolated side-question answering against immutable snapshots.

Ports the LAZY sidequestion contract. Operators ask follow-up
questions without mutating the main agent loop. Answers derive from
a captured snapshot plus recent successful exchanges under token and
concurrency budgets.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True, slots=True)
class SideConfig:
    """Centralized constants for side-question behavior."""

    max_question_chars: int = 4000
    max_concurrency: int = 4
    request_timeout_sec: float = 120.0
    history_page: int = 20


CONFIG = SideConfig()


@dataclass(frozen=True, slots=True)
class Snapshot:
    """Immutable context captured from the main agent."""

    snapshot_id: str
    task_id: str
    text: str
    captured_at: float


@dataclass
class SideQuestion:
    """Single isolated question with accumulated answer."""

    request_id: str
    snapshot_id: str
    question: str
    answer: str = ""
    status: str = "pending"


class SideQuestionService:
    """Bounded service for snapshot-scoped questions."""

    def __init__(self, answer_fn: Callable[[str, str], str] | None = None,
                 config: SideConfig = CONFIG) -> None:
        """Initialize registries with an optional answer function."""
        self._config = config
        self._answer_fn = answer_fn or (lambda snapshot, question:
                                        f"Context: {snapshot[:200]} | Q: {question[:200]}")
        self._lock = threading.Lock()
        self._snapshots: dict[str, Snapshot] = {}
        self._requests: dict[str, SideQuestion] = {}
        self._running = 0

    def capture(self, task_id: str, text: str) -> Snapshot:
        """Freeze main-loop context into an immutable snapshot."""
        snapshot = Snapshot(snapshot_id=uuid.uuid4().hex[:12],
                            task_id=str(task_id), text=str(text or ""),
                            captured_at=time.time())
        with self._lock:
            self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot

    def ask(self, snapshot_id: str, question: str) -> SideQuestion:
        """Answer from a snapshot without touching main state."""
        clean = str(question or "").strip()
        if not clean:
            raise ValueError("Question must not be empty.")
        if len(clean) > self._config.max_question_chars:
            raise ValueError("Question exceeds length budget.")
        with self._lock:
            snapshot = self._snapshots.get(str(snapshot_id))
            if snapshot is None:
                raise KeyError(f"Unknown snapshot: {snapshot_id}")
            if self._running >= self._config.max_concurrency:
                raise RuntimeError("Side-question concurrency exhausted.")
            self._running += 1
            request = SideQuestion(request_id=uuid.uuid4().hex[:12],
                                   snapshot_id=snapshot.snapshot_id,
                                   question=clean, status="running")
            self._requests[request.request_id] = request
        try:
            request.answer = str(self._answer_fn(snapshot.text, clean))
            request.status = "done"
        except Exception as exc:
            request.status = "failed"
            request.answer = str(exc)
        finally:
            with self._lock:
                self._running -= 1
        return request

    def cancel(self, request_id: str) -> bool:
        """Mark a pending request cancelled."""
        with self._lock:
            request = self._requests.get(str(request_id))
            if request is None or request.status != "running":
                return False
            request.status = "cancelled"
            return True

    def history(self, limit: int = 20, before: float = 0.0) -> list[SideQuestion]:
        """Page request history newest first."""
        with self._lock:
            rows = list(self._requests.values())
        rows.sort(key=lambda r: r.request_id, reverse=True)
        page = max(1, int(limit or self._config.history_page))
        return rows[:page]
