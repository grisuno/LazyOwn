"""Chain-of-evidence: depends_on gating, budgets, verdicts and artefact pins."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "modules"))

from modules.chain_registry import load_all, validate_chain  # noqa: E402
from modules.chain_runner import VERDICT_NOT_OBSERVED, VERDICT_OBSERVED, ChainRunner  # noqa: E402


def _chain(tmp_path: Path, steps: list[dict], name: str = "ev") -> dict:
    document = {"name": name, "version": 2, "steps": steps}
    (tmp_path / f"{name}.yaml").write_text(yaml.dump(document), encoding="utf-8")
    return document


def _load(document: dict, tmp_path: Path):
    return load_all(chains_dir=tmp_path)[document["name"]]


def test_validate_hunting_fields() -> None:
    """Registry validates the new hunting fields and rejects malformed ones."""
    ok = {
        "name": "ev",
        "version": 2,
        "steps": [
            {"run": "a", "id": "one", "required_fields": ["user"], "benign_alternatives": ["cron"], "evidence": ["sessions/out.jsonl"]},
            {"run": "b", "id": "two", "depends_on": ["one"], "budget": {"attempts": 2, "seconds": 60}},
            {"run": "c", "id": "three", "evidence_sha256": {"sessions/out.jsonl": "a" * 64}},
        ],
    }
    assert validate_chain(ok) == []
    bad_variants = [
        {"name": "ev", "version": 2, "steps": [{"run": "a", "depends_on": ["ghost"]}]},
        {"name": "ev", "version": 2, "steps": [{"run": "a", "id": "x", "depends_on": ["x"]}]},
        {"name": "ev", "version": 2, "steps": [{"run": "a", "budget": {"attempts": 99}}]},
        {"name": "ev", "version": 2, "steps": [{"run": "a", "budget": {"bogus": 1}}]},
        {"name": "ev", "version": 2, "steps": [{"run": "a", "evidence_sha256": {"p": "not-hex"}}]},
        {"name": "ev", "version": 2, "steps": [{"run": "a", "required_fields": [1]}]},
    ]
    for document in bad_variants:
        assert validate_chain(document), document


def test_dependency_gate_skips_unproven_chain(tmp_path: Path) -> None:
    """A step whose dependency is not observed is skipped with a reason."""
    document = _chain(
        tmp_path,
        [
            {"run": "failstep", "id": "first", "required_fields": ["sig"], "continue_on_error": True},
            {"run": "later", "id": "second", "depends_on": ["first"]},
        ],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            if command == "failstep":
                return False, "", "boom"
            return True, "ok", ""

    result = _Runner(_load(document, tmp_path)).run()
    statuses = {outcome.id: outcome.status for outcome in result.steps}
    assert statuses["first"] == "failed"
    assert statuses["second"] == "skipped"
    second = [outcome for outcome in result.steps if outcome.id == "second"][0]
    assert "attack chain unproven" in second.reason
    assert result.verdicts.get("first") == VERDICT_NOT_OBSERVED


def test_dependency_gate_passes_when_observed(tmp_path: Path) -> None:
    """A dependency with observed evidence lets the dependent step run."""
    evidence = tmp_path / "out.jsonl"
    evidence.write_text('{"user": "root"}\n', encoding="utf-8")
    document = _chain(
        tmp_path,
        [
            {"run": "collect", "id": "first", "evidence": [str(evidence)], "required_fields": ["user"]},
            {"run": "later", "id": "second", "depends_on": ["first"]},
        ],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            return True, "done", ""

    result = _Runner(_load(document, tmp_path)).run()
    assert result.steps[1].status == "ok"
    assert result.chain_proven


def test_observed_verdict_on_success_with_fields(tmp_path: Path) -> None:
    """Success with required fields present yields evidence_observed."""
    evidence = tmp_path / "out.jsonl"
    evidence.write_text('{"user": "root"}\n', encoding="utf-8")
    document = _chain(
        tmp_path,
        [{"run": "collect", "id": "grab", "evidence": [str(evidence)], "required_fields": ["user"]}],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            return True, "done", ""

    result = _Runner(_load(document, tmp_path)).run()
    assert result.steps[0].status == "ok"
    assert result.steps[0].verdict == VERDICT_OBSERVED
    assert result.verdicts.get("grab") == VERDICT_OBSERVED


def test_missing_required_field_is_insufficient(tmp_path: Path) -> None:
    """Success but absent required fields yields insufficient_data."""
    evidence = tmp_path / "out.jsonl"
    evidence.write_text('{"other": 1}\n', encoding="utf-8")
    document = _chain(
        tmp_path,
        [{"run": "collect", "id": "grab", "evidence": [str(evidence)], "required_fields": ["user"]}],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            return True, "done", ""

    result = _Runner(_load(document, tmp_path)).run()
    assert result.steps[0].verdict == "insufficient_data"


def test_evidence_sha256_pin(tmp_path: Path) -> None:
    """A pinned digest verifies; a wrong one fails the step."""
    evidence = tmp_path / "out.jsonl"
    evidence.write_text('{"user": "root"}\n', encoding="utf-8")
    digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
    good = _chain(
        tmp_path,
        [{"run": "collect", "id": "grab", "evidence": [str(evidence)], "evidence_sha256": {str(evidence): digest}}],
        name="evgood",
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            return True, "done", ""

    result = _Runner(_load(good, tmp_path)).run()
    assert result.steps[0].status == "ok"
    bad = _chain(
        tmp_path,
        [{"run": "collect", "id": "grab", "evidence": [str(evidence)], "evidence_sha256": {str(evidence): "b" * 64}}],
        name="evbad",
    )
    result = _Runner(_load(bad, tmp_path)).run()
    assert result.steps[0].status == "failed"
    assert "hash mismatch" in result.steps[0].reason


def test_budget_caps_attempts(tmp_path: Path) -> None:
    """budget.attempts caps total executions including retries."""
    calls: list[str] = []
    document = _chain(
        tmp_path,
        [{"run": "flaky", "id": "grab", "retries": 4, "budget": {"attempts": 2}}],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            calls.append(command)
            return False, "", "no"

    result = _Runner(_load(document, tmp_path), retry_backoff=0).run()
    assert result.steps[0].attempts == 2
    assert len(calls) == 2
    assert result.steps[0].budget_used == {"attempts": 2}


def test_budget_seconds_caps_timeout(tmp_path: Path) -> None:
    """budget.seconds caps the step timeout when the step declares none."""
    seen: dict[str, int] = {}

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            seen["timeout"] = timeout
            return True, "done", ""

    document = _chain(tmp_path, [{"run": "quick", "id": "grab", "budget": {"seconds": 10}}])
    result = _Runner(_load(document, tmp_path), default_timeout=300).run()
    assert result.steps[0].status == "ok"
    assert seen["timeout"] == 10


def test_legacy_chains_unchanged(tmp_path: Path) -> None:
    """Chains without hunting fields behave exactly as before."""
    document = _chain(
        tmp_path,
        [{"run": "alpha", "id": "a", "continue_on_error": True}, {"run": "beta", "id": "b"}],
    )

    class _Runner(ChainRunner):
        def _execute(self, command: str, timeout: int, expect_exits: tuple[int, ...] = ()):
            if command == "alpha":
                return False, "", "nope"
            return True, "ok", ""

    result = _Runner(_load(document, tmp_path)).run()
    assert not result.aborted
    assert result.steps[0].status == "failed"
    assert result.steps[0].verdict == ""
    assert result.steps[1].status == "ok"
