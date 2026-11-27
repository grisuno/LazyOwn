"""Symbol freeze gate for the ``utils`` barrel surface.

The stdlib-import gate (``test_utils_barrel_deprecation``) stops new
stdlib imports through ``utils``; this gate freezes the module's entire
public attribute surface so no new symbols can be re-exported through
the barrel either. New code must define symbols in ``core.*`` /
``modules.*`` and import them from there. Removals rebase the baseline
down via the update script; additions require a freeze exception and a
baseline bump in the same PR.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = REPO_ROOT / "tests" / "utils_symbol_baseline.json"


def _live_surface() -> set[str]:
    """Return the public attribute names of the ``utils`` module."""
    import utils

    return {name for name in dir(utils) if not name.startswith("_")}


def _baseline() -> set[str]:
    """Load the committed baseline symbol set."""
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    return set(data)


def test_no_new_utils_symbols() -> None:
    """No new public symbol may appear on the ``utils`` barrel."""
    baseline = _baseline()
    additions = sorted(_live_surface() - baseline)
    assert not additions, "new utils barrel symbols outside baseline:\n" + "\n".join(additions)


def test_utils_baseline_has_no_stale_symbols() -> None:
    """Baseline entries for removed symbols must be deleted."""
    baseline = _baseline()
    stale = sorted(baseline - _live_surface())
    assert not stale, f"stale baseline symbols (rebase baseline down): {stale}"


FORBIDDEN_PIPELINE_SYMBOLS = (
    "aggressive_yaml_fix",
    "create_synthetic_yaml",
    "display_news",
    "exploitalert",
    "find_ea",
    "find_ps",
    "find_ss",
    "fix_common_yaml_issues",
    "load_knowledge_base",
    "manual_yaml_extraction",
    "nvddb",
    "packetstormsecurity",
    "parse_yaml_response",
    "preprocess_llm_response",
    "query_ollama",
    "save_playbook",
    "scrape_news",
)


def test_pipeline_symbols_not_reexported() -> None:
    """LLM pipeline and advisory-feed symbols must live in their modules."""
    violations = sorted(n for n in _live_surface() if n in FORBIDDEN_PIPELINE_SYMBOLS)
    assert not violations, (
        "advisory/LLM-pipeline symbols must be imported from their modules, not utils:\n" + "\n".join(violations)
    )
