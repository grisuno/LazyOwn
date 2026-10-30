"""Chain-to-findings gate contract: insufficient verdicts never confirm.

Every scenario states Given, When, Then. A chain event whose run
produced ``insufficient_data`` verdicts lands as ``partial`` with its
own reason, even with plentiful raw output; an open gate keeps the
historical confirmed path.
"""

from __future__ import annotations

from modules.lazy_findings import LedgerLimits, row_from_event


def _chain_payload(gate: str) -> dict:
    """Build one chain outcome event dict."""
    return {
        "kind": "chain",
        "kind_value": "chain",
        "task_id": "t0001",
        "title": "chain demo",
        "severity": "medium",
        "success": True,
        "shell": False,
        "source": "demo",
        "command": "c2_deplay {target}",
        "output": "captured output long enough to clear the minimum char bar by far",
        "metadata": {"findings_gate": gate, "steps": []},
    }


def test_open_gate_confirms_with_evidence():
    """Given an open gate and real output, When the row maps, Then it confirms."""
    row = row_from_event(_chain_payload("open"), LedgerLimits())
    assert row is not None and row["state"] == "confirmed"


def test_blocked_gate_stays_partial_with_reason():
    """Given a blocked gate, When the row maps, Then the state is partial."""
    row = row_from_event(_chain_payload("blocked"), LedgerLimits())
    assert row is not None
    assert row["state"] == "partial"
    assert row["reason"].startswith("chain verdict insufficient_data")


def test_default_payload_unaffected():
    """Given no gate key, When the row maps, Then legacy behaviour holds."""
    payload = _chain_payload("")
    del payload["metadata"]["findings_gate"]
    row = row_from_event(payload, LedgerLimits())
    assert row is not None and row["state"] == "confirmed"
