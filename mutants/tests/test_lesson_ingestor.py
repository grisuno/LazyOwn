"""Tests for modules/lesson_ingestor.py."""
from __future__ import annotations

import json
from unittest.mock import MagicMock

from modules.lesson_ingestor import (
    _LESSON_TO_EXPERT,
    LessonIngestor,
    LessonLearned,
)


class TestLessonLearned:
    def test_from_dict(self):
        d = {
            "campaign_id": "c1",
            "campaign_name": "test",
            "topic": "credential_access",
            "lesson": "lesson text",
            "context": "ctx",
            "derived_at": "2024-01-01",
        }
        ll = LessonLearned.from_dict(d)
        assert ll.campaign_id == "c1"
        assert ll.topic == "credential_access"

    def test_from_dict_minimal(self):
        ll = LessonLearned.from_dict({})
        assert ll.campaign_id == ""
        assert ll.topic == ""


class TestLessonIngestor:
    def test_expert_mapping(self):
        assert _LESSON_TO_EXPERT["credential_access"] == "credential_expert"
        assert _LESSON_TO_EXPERT["lateral_movement"] == "lateral_expert"
        assert _LESSON_TO_EXPERT["privesc"] == "privesc_expert"
        assert _LESSON_TO_EXPERT["exfiltration"] == "exfil_expert"
        assert _LESSON_TO_EXPERT["intrusion"] == "exploit_expert"

    def test_ingest_with_mock_backends(self, tmp_path):
        router = MagicMock()
        trainer = MagicMock()
        trainer.encode_state.return_value = "state_key"
        ingestor = LessonIngestor(router=router, trainer=trainer)

        lesson = LessonLearned(
            campaign_id="c1",
            campaign_name="test",
            topic="credential_access",
            lesson="cred dump",
            context="ctx",
        )
        result = ingestor.ingest(lesson)
        assert result is True
        router._store.record.assert_called_once()
        trainer.update.assert_called_once()
        trainer.save.assert_called_once()

    def test_ingest_unmapped_topic(self, tmp_path):
        router = MagicMock()
        trainer = MagicMock()
        ingestor = LessonIngestor(router=router, trainer=trainer)

        lesson = LessonLearned(
            campaign_id="c1",
            campaign_name="test",
            topic="unknown_topic",
            lesson="test",
            context="ctx",
        )
        result = ingestor.ingest(lesson)
        assert result is False
        router._store.record.assert_not_called()
        trainer.update.assert_not_called()

    def test_ingest_no_backends(self, monkeypatch):
        monkeypatch.setattr(
            "modules.lesson_ingestor.LessonIngestor._get_router",
            lambda self: None,
        )
        monkeypatch.setattr(
            "modules.lesson_ingestor.LessonIngestor._get_trainer",
            lambda self: None,
        )
        ingestor = LessonIngestor(router=None, trainer=None)
        lesson = LessonLearned(
            campaign_id="c1",
            campaign_name="test",
            topic="credential_access",
            lesson="test",
            context="ctx",
        )
        result = ingestor.ingest(lesson)
        assert result is False

    def test_load_from_file(self, tmp_path):
        lessons_file = tmp_path / "lessons.jsonl"
        lessons_file.write_text(json.dumps({
            "campaign_id": "c1",
            "campaign_name": "test",
            "topic": "credential_access",
            "lesson": "test lesson",
            "context": "ctx",
        }) + "\n")

        ingestor = LessonIngestor(lessons_file=lessons_file)
        lessons = ingestor._load_from_file()
        assert len(lessons) == 1
        assert lessons[0].topic == "credential_access"

    def test_load_from_file_missing(self, tmp_path):
        ingestor = LessonIngestor(lessons_file=tmp_path / "nonexistent.jsonl")
        lessons = ingestor._load_from_file()
        assert len(lessons) == 0

    def test_ingest_all(self, tmp_path):
        router = MagicMock()
        trainer = MagicMock()
        trainer.encode_state.return_value = "state_key"
        ingestor = LessonIngestor(router=router, trainer=trainer)

        lessons = [
            LessonLearned("c1", "t1", "credential_access", "l1", "ctx"),
            LessonLearned("c1", "t1", "lateral_movement", "l2", "ctx"),
        ]
        count = ingestor.ingest_all(lessons)
        assert count == 2
