"""Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter.

After a campaign completes, :class:`EpisodeReflectionEngine` in
``skills/lazyown_campaign.py`` extracts :class:`LessonLearned` records and
persists them to ``sessions/campaign_lessons.jsonl`` and Hive Memory
(LazyHebb).  However, those lessons were never fed back into the MoE router
or RL trainer to influence future expert selection.

This module closes that gap.  :class:`LessonIngestor` reads lessons and
applies lightweight adjustments to:

1. ``ExpertPerformanceStore`` — boosts the EMA reward for experts that
   executed techniques matching the lesson's topic.
2. ``RLTrainer`` — applies a small positive reward to the
   ``(task_type, expert)`` Q-entry so the epsilon-greedy policy prefers
   that expert for the same task type in future campaigns.

Design (SOLID)
--------------
- Single Responsibility : lesson → expert mapping + weight adjustment only.
- Open/Closed           : new lesson topics added to ``_LESSON_TO_EXPERT``.
- Dependency Inversion  : depends on ``get_router`` / ``get_trainer``
  factory functions, not concrete classes.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_LESSONS_FILE = _SESSIONS_DIR / "campaign_lessons.jsonl"
_SEEN_FILE = _SESSIONS_DIR / "lesson_ingestor_seen.json"

_BOOST_REWARD: float = 0.3
_BOOST_DETECTION_PROB: float = 0.0

_LESSON_TO_EXPERT: dict[str, str] = {
    "credential_access": "credential_expert",
    "lateral_movement": "lateral_expert",
    "privesc": "privesc_expert",
    "exfiltration": "exfil_expert",
    "intrusion": "exploit_expert",
    "persistence": "persist_expert",
    "scope_coverage": "recon_expert",
    "campaign_duration": "recon_expert",
}


@dataclass
class LessonLearned:
    """Minimal representation of a campaign lesson for ingestion."""

    campaign_id: str
    campaign_name: str
    topic: str
    lesson: str
    context: str
    derived_at: str = ""

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> LessonLearned:
        return cls(
            campaign_id=d.get("campaign_id", ""),
            campaign_name=d.get("campaign_name", ""),
            topic=d.get("topic", ""),
            lesson=d.get("lesson", ""),
            context=d.get("context", ""),
            derived_at=d.get("derived_at", ""),
        )


class LessonIngestor:
    """Bridge between post-campaign lessons and the MoE/RL routing layer.

    Reads lessons from ``sessions/campaign_lessons.jsonl`` (or an explicit
    list) and applies small reward boosts to the RL Q-table and the MoE
    performance store so that experts which previously succeeded for a
    given topic are preferred in future campaigns.
    """

    def __init__(
        self,
        lessons_file: Path | None = None,
        router: Any | None = None,
        trainer: Any | None = None,
        boost_reward: float = _BOOST_REWARD,
        seen_file: Path | None = None,
    ) -> None:
        self._lessons_file = lessons_file or _LESSONS_FILE
        self._router = router
        self._trainer = trainer
        self._boost_reward = boost_reward
        self._seen_file = seen_file or _SEEN_FILE

    def _get_router(self) -> Any | None:
        if self._router is not None:
            return self._router
        try:
            from modules.moe_router import get_router

            self._router = get_router()
            return self._router
        except Exception as exc:
            log.debug("LessonIngestor: router unavailable: %s", exc)
            return None

    def _get_trainer(self) -> Any | None:
        if self._trainer is not None:
            return self._trainer
        try:
            from modules.rl_trainer import get_trainer

            self._trainer = get_trainer()
            return self._trainer
        except Exception as exc:
            log.debug("LessonIngestor: trainer unavailable: %s", exc)
            return None

    def _expert_for_topic(self, topic: str) -> str | None:
        return _LESSON_TO_EXPERT.get(topic)

    def ingest(self, lesson: LessonLearned) -> bool:
        """Apply a single lesson to the MoE performance store and RL Q-table.

        Args:
            lesson: A :class:`LessonLearned` record.

        Returns:
            ``True`` when at least one backend was updated, ``False`` when
            the lesson topic was unmapped or no backend was available.
        """
        expert_id = self._expert_for_topic(lesson.topic)
        if expert_id is None:
            log.debug("LessonIngestor: no expert mapping for topic '%s'", lesson.topic)
            return False

        updated = False

        router = self._get_router()
        if router is not None:
            try:
                store = router._store
                store.record(
                    expert_id=expert_id,
                    task_type=lesson.topic,
                    reward=self._boost_reward,
                    detection_prob=_BOOST_DETECTION_PROB,
                )
                log.info(
                    "LessonIngestor: boosted MoE performance for %s on topic '%s'",
                    expert_id,
                    lesson.topic,
                )
                updated = True
            except Exception as exc:
                log.debug("LessonIngestor: MoE store update failed: %s", exc)

        trainer = self._get_trainer()
        if trainer is not None:
            try:
                state_key = trainer.encode_state(lesson.topic, "exploitation")
                trainer.update(
                    state=state_key,
                    action=expert_id,
                    reward=self._boost_reward,
                    next_state=state_key,
                    candidates=[expert_id],
                    detection_prob=_BOOST_DETECTION_PROB,
                )
                trainer.save()
                log.info(
                    "LessonIngestor: boosted RL Q-value for %s on topic '%s'",
                    expert_id,
                    lesson.topic,
                )
                updated = True
            except Exception as exc:
                log.debug("LessonIngestor: RL trainer update failed: %s", exc)

        return updated

    def ingest_all(self, lessons: list[LessonLearned] | None = None) -> int:
        """Ingest a batch of lessons.

        When *lessons* is ``None``, reads from the lessons JSONL file.

        Returns:
            Number of lessons successfully ingested.
        """
        if lessons is None:
            lessons = self._load_from_file()

        count = 0
        for lesson in lessons:
            if self.ingest(lesson):
                count += 1
        return count

    @staticmethod
    def _fingerprint(lesson: LessonLearned) -> str:
        """Return a stable content hash identifying one lesson."""
        import hashlib

        seed = "|".join([lesson.campaign_id, lesson.topic, lesson.lesson, lesson.derived_at])
        return hashlib.sha256(seed.encode("utf-8", "replace")).hexdigest()[:16]

    def _load_seen(self) -> set[str]:
        """Return the set of lesson fingerprints already boosted. Fail-open."""
        try:
            if self._seen_file.exists():
                data = json.loads(self._seen_file.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return {str(x) for x in data}
        except Exception as exc:
            log.debug("LessonIngestor: seen load failed: %s", exc)
        return set()

    def _save_seen(self, seen: set[str]) -> None:
        """Persist the fingerprint set atomically. Fail-open."""
        try:
            import os

            self._seen_file.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._seen_file.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(sorted(seen)), encoding="utf-8")
            os.replace(tmp, self._seen_file)
        except Exception as exc:
            log.debug("LessonIngestor: seen save failed: %s", exc)

    def ingest_new(self) -> int:
        """Ingest only lessons not boosted before, so each boosts exactly once.

        Idempotent across loops: a lesson's reward boost is applied once and its
        fingerprint persisted, so calling this at every loop startup absorbs a
        prior loop's new lessons without re-inflating the Q-table. Never raises.

        Returns:
            Number of newly ingested lessons.
        """
        try:
            seen = self._load_seen()
            count = 0
            dirty = False
            for lesson in self._load_from_file():
                fp = self._fingerprint(lesson)
                if fp in seen:
                    continue
                if self.ingest(lesson):
                    seen.add(fp)
                    dirty = True
                    count += 1
            if dirty:
                self._save_seen(seen)
            return count
        except Exception as exc:
            log.debug("LessonIngestor: ingest_new failed: %s", exc)
            return 0

    def _load_from_file(self) -> list[LessonLearned]:
        """Load lessons from the JSONL file."""
        if not self._lessons_file.exists():
            return []
        lessons: list[LessonLearned] = []
        try:
            with self._lessons_file.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        lessons.append(LessonLearned.from_dict(json.loads(line)))
                    except Exception:
                        continue
        except Exception as exc:
            log.debug("LessonIngestor: file load failed: %s", exc)
        return lessons


def ingest_campaign_lessons(
    lessons_file: Path | None = None,
) -> int:
    """Module-level convenience function to ingest all campaign lessons.

    Args:
        lessons_file: Optional path to a lessons JSONL file.

    Returns:
        Number of lessons successfully ingested.
    """
    ingestor = LessonIngestor(lessons_file=lessons_file)
    return ingestor.ingest_all()


def ingest_new_campaign_lessons(lessons_file: Path | None = None) -> int:
    """Ingest only lessons not boosted before (idempotent across loops).

    Safe to call at every autonomous-loop startup: a prior loop's new lessons
    are absorbed into the RL Q-table and MoE exactly once before the next loop
    plans, without re-inflating already-learned priors. Never raises.

    Returns:
        Number of newly ingested lessons.
    """
    return LessonIngestor(lessons_file=lessons_file).ingest_new()


__all__ = [
    "LessonLearned",
    "LessonIngestor",
    "ingest_campaign_lessons",
    "_LESSON_TO_EXPERT",
]
