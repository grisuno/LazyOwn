"""Loop-to-loop learning: new campaign lessons feed the RL/MoE once per lesson.

The ingestor applies reward boosts to the Q-table and MoE. Calling it at every
loop startup must not re-boost lessons already absorbed, or the Q-table inflates
without bound. ``ingest_new`` persists a fingerprint per ingested lesson so a
lesson boosts exactly once across runs, while a genuinely new lesson from the
previous loop is absorbed before the next loop plans.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import pytest  # noqa: E402

from modules.lesson_ingestor import LessonIngestor  # noqa: E402


class _Trainer:
    def __init__(self) -> None:
        self.updates = 0

    def encode_state(self, topic, phase="exploitation"):
        return f"{topic}|{phase}"

    def update(self, **kwargs):
        self.updates += 1

    def save(self):
        pass


@pytest.fixture()
def lessons_file(tmp_path):
    path = tmp_path / "campaign_lessons.jsonl"
    rows = [
        {"campaign_id": "c1", "topic": "intrusion", "lesson": "vsftpd backdoor works", "derived_at": "t1"},
        {"campaign_id": "c1", "topic": "credential_access", "lesson": "reuse msfadmin", "derived_at": "t1"},
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    return path


def _ingestor(lessons_file, tmp_path):
    trainer = _Trainer()
    ing = LessonIngestor(
        lessons_file=lessons_file,
        trainer=trainer,
        seen_file=tmp_path / "lesson_ingestor_seen.json",
    )
    return ing, trainer


def test_ingest_new_absorbs_then_skips(lessons_file, tmp_path):
    ing, trainer = _ingestor(lessons_file, tmp_path)
    first = ing.ingest_new()
    assert first == 2
    assert trainer.updates == 2
    second = ing.ingest_new()
    assert second == 0
    assert trainer.updates == 2


def test_ingest_new_absorbs_only_the_new_lesson(lessons_file, tmp_path):
    ing, _ = _ingestor(lessons_file, tmp_path)
    assert ing.ingest_new() == 2
    with lessons_file.open("a", encoding="utf-8") as fh:
        fh.write(
            "\n" + json.dumps({"campaign_id": "c2", "topic": "privesc", "lesson": "distcc exec", "derived_at": "t2"})
        )
    ing2, trainer2 = _ingestor(lessons_file, tmp_path)
    assert ing2.ingest_new() == 1
    assert trainer2.updates == 1


def test_seen_file_persists_across_instances(lessons_file, tmp_path):
    ing, _ = _ingestor(lessons_file, tmp_path)
    ing.ingest_new()
    seen = json.loads((tmp_path / "lesson_ingestor_seen.json").read_text())
    assert len(seen) == 2


def test_ingest_new_fail_open_without_backends(lessons_file, tmp_path):
    ing = LessonIngestor(lessons_file=lessons_file, seen_file=tmp_path / "seen.json")
    ing._get_router = lambda: None
    ing._get_trainer = lambda: None
    assert ing.ingest_new() == 0
