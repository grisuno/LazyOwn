"""Tests for cli.phase_labels — canonical phase display labels contract."""

from __future__ import annotations

import json
from pathlib import Path

from cli.phase_labels import PHASE_LABELS, phase_label

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_known_phase_labels():
    assert PHASE_LABELS["recon"] == "Reconnaissance"
    assert PHASE_LABELS["privesc"] == "Privilege Escalation"
    assert PHASE_LABELS["c2"] == "Command & Control"


def test_phase_label_falls_back_to_title_case():
    assert phase_label("recon") == "Reconnaissance"
    assert phase_label("not-a-phase") == "Not-A-Phase"
    assert phase_label("") == "Unknown"
    assert phase_label(None) == "Unknown"


def test_phase_label_keys_cover_command_index_phases():
    index = json.loads((REPO_ROOT / "cli" / "command_index.json").read_text(encoding="utf-8"))
    for bucket in index.get("phase_to_commands", {}):
        assert bucket in PHASE_LABELS


def test_contextual_help_reuses_canonical_labels():
    import cli.contextual_help as ch

    assert ch.PHASE_LABELS is PHASE_LABELS


def test_tips_engine_reuses_canonical_labels():
    import cli.tips_engine as te

    assert te.PHASE_LABELS is PHASE_LABELS
