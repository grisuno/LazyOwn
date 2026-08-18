"""Lesson ingestion bridge between EpisodeReflectionEngine and MoERouter.

After a campaign completes, :class:`EpisodeReflectionEngine` in
``skills/lazyown_campaign.py`` extracts :class:`LessonLearned` records and
persists them to ``sessions/campaign_lessons.jsonl`` and Hive Memory
(ChromaDB).  However, those lessons were never fed back into the MoE router
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

_BOOST_REWARD: float = 0.3
_BOOST_DETECTION_PROB: float = 0.0

_LESSON_TO_EXPERT: dict[str, str] = {
    "credential_access": "credential_expert",
    "lateral_movement":  "lateral_expert",
    "privesc":           "privesc_expert",
    "exfiltration":      "exfil_expert",
    "intrusion":         "exploit_expert",
    "persistence":       "persist_expert",
    "scope_coverage":    "recon_expert",
    "campaign_duration": "recon_expert",
}


@dataclass
class LessonLearned:
    """Minimal representation of a campaign lesson for ingestion."""

    campaign_id:   str
    campaign_name: str
    topic:         str
    lesson:        str
    context:       str
    derived_at:    str = ""

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
    ) -> None:
        self._lessons_file = lessons_file or _LESSONS_FILE
        self._router = router
        self._trainer = trainer
        self._boost_reward = boost_reward

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
                    expert_id, lesson.topic,
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
                    expert_id, lesson.topic,
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


__all__ = [
    "LessonLearned",
    "LessonIngestor",
    "ingest_campaign_lessons",
    "_LESSON_TO_EXPERT",
]
