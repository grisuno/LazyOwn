"""Tests for modules.lazy_findings — engagement findings ledger.

Covers:
    - Row normalization fail-closed (state, level, technique, title)
    - Confirmed-evidence reproducibility gate
    - Engagement id confinement (path traversal rejected)
    - Append + paginated + corrupt-line-tolerant reads
    - Verdict transition mapping (reproduced/fixed/inconclusive)
    - event row mapping for finding/exploit classes
    - redaction of secrets in evidence before persistence
    - state_counts latest-wins semantics and handoff shape
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def ledger_module():
    import modules.lazy_findings as lf

    return lf


@pytest.fixture
def tmp_base():
    with tempfile.TemporaryDirectory() as directory:
        yield Path(directory)


class TestNormalize:
    def test_valid_row_passes(self, ledger_module, tmp_base):
        lf = ledger_module
        row = lf.row_from_event(
            {
                "kind": "finding",
                "title": "sqli probable",
                "severity": "high",
                "command": "curl http://h/x",
                "output": "vulnerable to sqli confirmed GET",
                "mitre_id": "T1190",
                "task_id": "t1",
                "host_value": "10.0.0.5",
            }
        )
        out = lf.normalize_finding(row)
        assert out["state"] == "partial"
        assert out["level"] == "confirmed"
        assert out["technique_id"] == "T1190"

    def test_empty_title_rejected(self, ledger_module):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding({"title": " ", "state": "hypothesis", "level": "identified"})

    def test_unknown_state_rejected(self, ledger_module):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding({"title": "t", "state": "totally-wrong", "level": "identified"})

    def test_unknown_level_rejected(self, ledger_module):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding({"title": "t", "state": "hypothesis", "level": "mega"})

    def test_invented_technique_rejected(self, ledger_module):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding({"title": "t", "state": "partial", "level": "identified", "technique_id": "TX9999"})

    def test_tac_id_accepted(self, ledger_module):
        lf = ledger_module
        row = lf.normalize_finding(
            {"title": "t", "state": "partial", "level": "identified", "technique_id": "TA0001"}
        )
        assert row["technique_id"] == "TA0001"

    def test_confirmed_requires_evidence(self, ledger_module):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding(
                {"title": "t", "state": "confirmed", "level": "identified", "evidence": {"command": "id", "output": ""}}
            )
        with pytest.raises(lf.FindingValidationError):
            lf.normalize_finding({"title": "t", "state": "confirmed", "level": "identified"})

    def test_confirmed_with_reproducible_ok(self, ledger_module):
        lf = ledger_module
        row = lf.normalize_finding(
            {
                "title": "t",
                "state": "confirmed",
                "level": "identified",
                "evidence": {"command": "id", "output": "uid=0(root) mechanism"},
            }
        )
        assert row["state"] == "confirmed"
        assert row["level"] == "confirmed"

    def test_confirmed_with_artifact_ref_ok(self, ledger_module):
        lf = ledger_module
        row = lf.normalize_finding(
            {
                "title": "t",
                "state": "confirmed",
                "level": "identified",
                "evidence": {"artifact_ref": {"execution_id": "e1", "name": "out.bin"}},
            }
        )
        assert row["state"] == "confirmed"


class TestEvents:
    def test_verdict_reproduced_promotes(self, ledger_module):
        lf = ledger_module
        row = lf.row_from_event(
            {
                "kind": "finding",
                "title": "retest #1",
                "task_id": "t1",
                "metadata": {
                    "verdict": "reproduced",
                    "finding_ref": "42",
                    "evidence_command": "curl",
                    "evidence_output": "200 exploiting injection proof row",
                },
            }
        )
        assert row is not None
        assert row["state"] == "confirmed"
        assert row["finding_ref"] == "42"

    def test_verdict_fixed_discards(self, ledger_module):
        lf = ledger_module
        row = lf.row_from_event(
            {"kind": "finding", "title": "retest", "metadata": {"verdict": "fixed", "finding_ref": "7"}}
        )
        assert row["state"] == "discarded"

    def test_verdict_inconclusive_partial(self, ledger_module):
        lf = ledger_module
        row = lf.row_from_event(
            {"kind": "finding", "title": "retest", "metadata": {"verdict": "inconclusive", "finding_ref": "7"}}
        )
        assert row["state"] == "partial"

    def test_unmapped_verdict_ignores(self, ledger_module):
        lf = ledger_module
        assert lf.row_from_event(
            {"kind": "finding", "title": "x", "metadata": {"verdict": "blorp", "finding_ref": "7"}}
        ) is None

    def test_out_of_scope_kind_ignores(self, ledger_module):
        lf = ledger_module
        assert lf.row_from_event({"kind": "report", "title": "report"}) is None

    def test_exploit_success_confirmed(self, ledger_module):
        lf = ledger_module
        row = lf.row_from_event(
            {
                "kind": "exploit",
                "success": True,
                "shell": True,
                "title": "webshell act",
                "command": "curl upload",
                "output": "lazyown_webshell_rce_ok via POST",
                "task_id": "t9",
            }
        )
        assert row["state"] == "confirmed"
        assert row["level"] == "critical"


class TestLedger:
    def test_traversal_rejected(self, ledger_module, tmp_base):
        lf = ledger_module
        with pytest.raises(lf.FindingValidationError):
            lf.FindingsLedger("../evil", tmp_base)

    def test_append_and_read_pg(self, ledger_module, tmp_base):
        lf = ledger_module
        led = lf.FindingsLedger("t1", tmp_base)
        row = led.append(
            {"title": "row one", "state": "partial", "level": "confirmed", "technique_id": "T1083"}
        )
        led.append(
            {"title": "row two", "state": "hypothesis", "level": "identified", "finding_ref": row["finding_ref"]}
        )
        page = led.read(cursor=0, limit=1)
        assert page["total"] == 2 and page["done"] is False
        second = led.read(cursor=1)
        assert second["done"] is True and len(second["findings"]) == 1
        assert led.latest_state(row["finding_ref"]) == "hypothesis"

    def test_corrupt_lines_skipped(self, ledger_module, tmp_base):
        lf = ledger_module
        led = lf.FindingsLedger("t2", tmp_base)
        led.append({"title": "good", "state": "partial", "level": "identified"})
        with led.file_path.open("a", encoding="utf-8") as handle:
            handle.write("GARBAGE LINE\n{broken json\n")
        rows = led.rows()
        assert len(rows) == 1 and rows[0].get("title") == "good"

    def test_redaction_masks_secrets(self, ledger_module, tmp_base):
        lf = ledger_module
        led = lf.FindingsLedger("t3", tmp_base)
        record = led.append(
            {
                "title": "leak order",
                "state": "hypothesis",
                "level": "identified",
                "evidence": {"command": "curl api_key=sk-deadbeef1234", "output": "pwd=supersecret2"},
            }
        )
        stored = led.rows()[0]
        assert "sk-deadbeef1234" not in stored["evidence"]["command"]
        assert "supersecret2" not in stored["evidence"]["output"]
        del record

    def test_redaction_off_shows_verbatim(self, ledger_module, tmp_base):
        lf = ledger_module
        limits = lf.LedgerLimits(redact_secrets=False)
        led = lf.FindingsLedger("t4", tmp_base, limits=limits)
        led.append(
            {
                "title": "operator decides",
                "state": "hypothesis",
                "level": "identified",
                "evidence": {"command": "curl api_key=sk-deadbeef1234", "output": "x"},
            }
        )
        assert "sk-deadbeef1234" in led.rows()[0]["evidence"]["command"]


class TestCountsHandoff:
    def test_state_counts_latest_wins(self, ledger_module):
        lf = ledger_module
        rows = [
            {"finding_ref": "a", "state": "partial"},
            {"finding_ref": "b", "state": "confirmed"},
            {"finding_ref": "a", "state": "confirmed"},
        ]
        counts = lf.state_counts(rows)
        assert counts["confirmed"] == 2 and counts["partial"] == 0

    def test_handoff_decision(self, ledger_module):
        lf = ledger_module
        rows = [{"finding_ref": "a", "state": "confirmed", "title": "t", "evidence": {}}]
        handoff = lf.build_handoff(rows, status="exhausted", rounds=2)
        assert handoff["states"]["confirmed"] == 1
        assert "confirmed findings" in handoff["next_decision"]
        empty = lf.build_handoff([], status="exhausted", rounds=2)
        assert "route exhausted" in empty["next_decision"]


class TestDiscardRow:
    def test_discard_row_normalized(self, ledger_module):
        lf = ledger_module
        row = lf.discard_row("sudo had no entries", command="sudo -l", engagement_id="t1")
        assert row["state"] == "discarded"
        assert "sudo" in row["title"]
