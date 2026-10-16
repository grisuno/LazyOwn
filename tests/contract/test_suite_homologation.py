"""SDD suite homologation contract for LazyOwn tests.

Every test module in this repository must behave as part of one production
suite: predictable names, registered markers, English identifiers, no emoji
noise, and a deploy gate that can run the full collection without import
errors. Mutation runners must exist for critical security surfaces so weak
tests are caught when mutants survive.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
TESTS_DIR = ROOT / "tests"

REQUIRED_MARKERS = {
    "unit",
    "integration",
    "bdd",
    "contract",
    "mutation",
    "sdd",
    "tdd",
    "slow",
}

REQUIRED_MUTATION_RUNNERS = [
    "run_mutation_killchain.py",
    "run_mutation_opsec.py",
    "run_mutation_shell_semantics.py",
    "run_mutation_no_shell.py",
]

DEPLOY_GATE_COMMAND = "python -m pytest tests/ -q"

_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U00002B00-\U00002BFF"
    "]+"
)


def _test_modules() -> list[Path]:
    """Return sorted legacy test modules at tests/ root.

    Returns:
        Sorted list of test_*.py paths directly under tests/.
    """
    return sorted(TESTS_DIR.glob("test_*.py"))


@pytest.mark.contract
@pytest.mark.sdd
class TestSuiteNaming:
    """SDD naming contract for suite modules."""

    def test_at_least_one_test_module_exists(self) -> None:
        """Suite must contain test modules."""
        assert _test_modules(), "no test_*.py modules found under tests/"

    def test_module_names_are_english_snake_case(self) -> None:
        """Module names use English snake_case without spaces or dashes."""
        pattern = re.compile(r"^test_[a-z0-9_]+\.py$")
        violations = [path.name for path in _test_modules() if not pattern.match(path.name)]
        assert not violations, f"non-homologated names: {violations[:10]}"

    def test_no_emoji_in_test_module_names(self) -> None:
        """Module file names carry no emoji characters."""
        violations = [path.name for path in _test_modules() if _EMOJI_PATTERN.search(path.name)]
        assert not violations, f"emoji in names: {violations[:10]}"


@pytest.mark.contract
@pytest.mark.sdd
class TestPytestMarkers:
    """SDD marker registration contract."""

    def test_required_markers_registered(self) -> None:
        """All suite tiers are registered in pyproject.toml."""
        content = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        missing = [marker for marker in sorted(REQUIRED_MARKERS) if marker not in content]
        assert not missing, f"markers missing from pyproject.toml: {missing}"

    def test_strict_markers_enabled(self) -> None:
        """Strict markers stay enabled so typos fail fast."""
        content = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        assert "--strict-markers" in content, "strict markers flag removed"


@pytest.mark.contract
@pytest.mark.sdd
class TestDeployGate:
    """SDD deploy gate contract for deploynator releases."""

    def test_deploynator_toml_exists(self) -> None:
        """Release gate requires deploynator.toml at repo root."""
        assert (ROOT / "deploynator.toml").is_file(), "missing deploynator.toml"

    def test_deploy_gate_runs_full_suite(self) -> None:
        """Deploy gate command targets the full tests directory."""
        content = (ROOT / "deploynator.toml").read_text(encoding="utf-8")
        assert "python -m pytest tests/ -q" in content, "deploy gate must run pytest on tests/"

    def test_deploy_timeouts_allow_long_runs(self) -> None:
        """Test and docs timeouts allow long production runs."""
        content = (ROOT / "deploynator.toml").read_text(encoding="utf-8")
        assert "timeout_s = 3600" in content, "expected 3600s timeout for long runs"


@pytest.mark.contract
@pytest.mark.sdd
@pytest.mark.mutation
class TestMutationCoverage:
    """SDD mutation contract: critical surfaces require runners."""

    def test_required_mutation_runners_exist(self) -> None:
        """Curated mutation runners exist for critical surfaces."""
        missing = [name for name in REQUIRED_MUTATION_RUNNERS if not (TESTS_DIR / name).is_file()]
        assert not missing, f"missing mutation runners: {missing}"

    def test_mutation_gate_script_exists(self) -> None:
        """Single consolidated mutation gate exists under scripts/."""
        assert (ROOT / "scripts" / "mutation_gate.py").is_file(), "missing scripts/mutation_gate.py"

    def test_mutmut_config_scoped(self) -> None:
        """mutmut config points at a real source and test target."""
        content = (ROOT / "mutmut.cfg").read_text(encoding="utf-8")
        assert "paths_to_mutate" in content, "mutmut.cfg missing paths_to_mutate"
        assert "tests_dir" in content or "tests" in content, "mutmut.cfg missing tests reference"


@pytest.mark.contract
@pytest.mark.sdd
class TestSuiteDocumentation:
    """SDD documentation contract for the normalized suite."""

    def test_suite_guide_exists(self) -> None:
        """Suite guide documents SDD, TDD, BDD, and mutation workflow."""
        assert (TESTS_DIR / "SUITE.md").is_file(), "missing tests/SUITE.md"

    def test_contract_readme_exists(self) -> None:
        """Contract directory carries its README."""
        assert (TESTS_DIR / "contract" / "README.md").is_file(), "missing tests/contract/README.md"

    def test_suite_guide_is_english_without_emoji(self) -> None:
        """Suite guide stays English prose without emoji noise."""
        content = (TESTS_DIR / "SUITE.md").read_text(encoding="utf-8")
        assert "SDD" in content and "TDD" in content, "suite guide must cover SDD and TDD"
        assert "BDD" in content and "mutation" in content.lower(), "suite guide must cover BDD and mutation"
        assert not _EMOJI_PATTERN.search(content), "suite guide must not contain emojis"


if __name__ == "__main__":
    sys.exit("Run with: python -m pytest tests/contract/test_suite_homologation.py -v")
