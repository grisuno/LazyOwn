"""Regression suite for the GitHub code-scanning mitigations.

The CodeQL ruleset shipped on the repository flagged a number of patterns that
this suite locks in once they are mitigated. Every test class targets a
single rule so a failure points at the specific contract that drifted.

Architecture:

- :class:`MitigationSuiteConfig` is the only place where paths, ``ast``
  conventions and the catalogue of fixed handlers live. Adding a new
  mitigation means appending one entry, not editing assertions.
- One test class per CodeQL rule. Behavioural tests run end-to-end where
  practical (e.g. the regex sanitiser); structural tests parse the source
  with :mod:`ast` so they do not require a running Flask app.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pytest


@dataclass(frozen=True)
class MitigationSuiteConfig:
    """Centralised constants for the vulnerability-mitigation suite.

    Every literal the suite depends on lives here. ``frozen=True`` prevents
    accidental mutation by per-test consumers.
    """

    forbidden_response_substrings: tuple[str, ...] = (
        "jsonify({'error': str(e)})",
        'jsonify({"error": str(e)})',
        "jsonify({'error': str(ex)})",
        'jsonify({"error": str(ex)})',
        "jsonify({'error': str(exc)})",
        'jsonify({"error": str(exc)})',
    )
    sanitised_handlers: tuple[tuple[str, str], ...] = (
        ("lazyc2.py", "log"),
        ("lazyc2.py", "palette_api"),
    )
    handler_module_paths: dict[str, str] = field(
        default_factory=lambda: {
            "lazyc2.py": "lazyc2.py",
            "lazyphishingai.py": "modules/lazyphishingai.py",
        }
    )
    sentinel_path: str = "lazy_sentinel4.py"
    sentinel_function: str = "sanitize_content"

    @property
    def repo_root(self) -> Path:
        """Absolute path to the repository root."""
        return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def mitigation_config() -> MitigationSuiteConfig:
    """Single, immutable configuration shared by every test class."""
    return MitigationSuiteConfig()


def _read_module(config: MitigationSuiteConfig, relative_path: str) -> str:
    """Return the source text of a module relative to the repo root."""
    target = config.repo_root / relative_path
    if not target.exists():
        pytest.fail(f"{relative_path} is missing — cannot validate mitigation.")
    return target.read_text(encoding="utf-8")


def _iter_function_bodies(src: str) -> Iterable[tuple[str, str]]:
    """Yield ``(function_name, body_source)`` for every function in ``src``."""
    tree = ast.parse(src)
    lines = src.splitlines(keepends=True)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body_start = node.body[0].lineno - 1 if node.body else node.lineno - 1
        body_end = node.end_lineno or len(lines)
        yield node.name, "".join(lines[body_start:body_end])


class TestStackTraceSanitisation:
    """``py/stack-trace-exposure`` mitigations are in place."""

    @pytest.fixture(scope="class")
    def lazyc2_src(self, mitigation_config: MitigationSuiteConfig) -> str:
        """The full text of ``lazyc2.py``."""
        return _read_module(mitigation_config, mitigation_config.handler_module_paths["lazyc2.py"])

    @pytest.fixture(scope="class")
    def phishingai_src(self, mitigation_config: MitigationSuiteConfig) -> str:
        """The full text of ``modules/lazyphishingai.py``."""
        return _read_module(
            mitigation_config, mitigation_config.handler_module_paths["lazyphishingai.py"]
        )

    def test_log_handler_returns_generic_message(self, lazyc2_src: str) -> None:
        """``/log`` no longer returns the raw exception string."""
        for name, body in _iter_function_bodies(lazyc2_src):
            if name != "log":
                continue
            assert "str(e)" not in body, "log handler still returns str(e)"
            assert "Internal server error" in body
            return
        pytest.fail("log handler not found in lazyc2.py")

    def test_log_handler_keeps_server_side_logging(self, lazyc2_src: str) -> None:
        """The mitigation preserves the server-side ``logger`` call."""
        for name, body in _iter_function_bodies(lazyc2_src):
            if name != "log":
                continue
            assert "logger.exception" in body or "logger.error" in body
            return
        pytest.fail("log handler not found in lazyc2.py")

    def test_palette_api_returns_generic_message(self, lazyc2_src: str) -> None:
        """``/api/palette`` no longer leaks the file-system path of the index."""
        for name, body in _iter_function_bodies(lazyc2_src):
            if name != "palette_api":
                continue
            assert "str(exc)" not in body, "palette_api still returns str(exc)"
            assert "Command index unavailable" in body
            return
        pytest.fail("palette_api handler not found in lazyc2.py")

    def test_palette_api_keeps_server_side_logging(self, lazyc2_src: str) -> None:
        """The mitigation preserves the server-side ``logger.error`` call."""
        for name, body in _iter_function_bodies(lazyc2_src):
            if name != "palette_api":
                continue
            assert "logger.error" in body
            return
        pytest.fail("palette_api handler not found in lazyc2.py")

    def test_dynamic_route_drops_raw_save_to_log_payload(self, lazyc2_src: str) -> None:
        """The ``dynamic_route`` handler no longer echoes ``response[0]``."""
        for name, body in _iter_function_bodies(lazyc2_src):
            if name != "dynamic_route":
                continue
            assert "jsonify(response[0])" not in body, "dynamic_route still leaks save_to_log payload"
            return
        pytest.fail("dynamic_route handler not found in lazyc2.py")

    def test_phishing_ai_returns_generic_message(self, phishingai_src: str) -> None:
        """The phishing AI module no longer leaks ``str(ex)`` from the API call."""
        assert "jsonify({\"error\": str(ex)})" not in phishingai_src
        assert "Upstream API communication error" in phishingai_src

    def test_no_forbidden_response_substrings_remain(
        self,
        lazyc2_src: str,
        phishingai_src: str,
        mitigation_config: MitigationSuiteConfig,
    ) -> None:
        """No remaining handler echoes a raw exception string in jsonify."""
        for needle in mitigation_config.forbidden_response_substrings:
            assert needle not in lazyc2_src, f"lazyc2.py still contains: {needle}"
            assert needle not in phishingai_src, f"lazyphishingai.py still contains: {needle}"


class TestSentinelRegexSafety:
    """``py/overly-large-range`` mitigation in ``lazy_sentinel4.sanitize_content``.

    The host module pulls in heavyweight optional dependencies (langchain,
    rich, watchdog) that may be absent in lean test environments. To keep
    the regression contract decoupled from those imports the suite reads
    the source, extracts the substitution pattern and exercises it against
    a stable input set.
    """

    @pytest.fixture(scope="class")
    def src(self, mitigation_config: MitigationSuiteConfig) -> str:
        """The full text of ``lazy_sentinel4.py``."""
        return _read_module(mitigation_config, mitigation_config.sentinel_path)

    def _extract_sanitise_pattern(self, src: str) -> str:
        """Return the printable-ASCII pattern wired into ``sanitize_content``."""
        match = re.search(r"re\.sub\(r'(\[\^[^']+)', ' ', text\)", src)
        if match is None:
            pytest.fail("sanitize_content pattern not found in lazy_sentinel4.py")
        return match.group(1)

    def test_no_redundant_character_range_in_sanitise(self, src: str) -> None:
        """The simplified character class is what landed."""
        assert r"[^\x20-\x7E\n\t]" in src
        assert r"[^\x20-\x7E\n\t#*+-_" not in src

    def test_pattern_matches_simplified_form(self, src: str) -> None:
        """The pattern extracted from source is the simplified one."""
        assert self._extract_sanitise_pattern(src) == r"[^\x20-\x7E\n\t]"

    def test_pattern_keeps_printable_ascii(self, src: str) -> None:
        """All printable ASCII characters survive the substitution unchanged."""
        pattern = re.compile(self._extract_sanitise_pattern(src))
        sample = "abc 123 [link](url) `code` *bold* | pipe"
        assert pattern.sub(" ", sample) == sample

    def test_pattern_keeps_tab_and_newline(self, src: str) -> None:
        """``\\t`` and ``\\n`` survive even though they fall outside ``\\x20-\\x7E``."""
        pattern = re.compile(self._extract_sanitise_pattern(src))
        text = "line1\nline2\twith tab"
        assert pattern.sub(" ", text) == text

    def test_pattern_strips_control_bytes(self, src: str) -> None:
        """Bytes below ``\\x20`` (other than tab/newline) are replaced."""
        pattern = re.compile(self._extract_sanitise_pattern(src))
        result = pattern.sub(" ", "clean\x01\x02\x7fbyte")
        assert "\x01" not in result
        assert "\x02" not in result
        assert "\x7f" not in result

    def test_pattern_does_not_strip_brackets(self, src: str) -> None:
        """The mitigation no longer accidentally drops ``]``, ``)`` or ``|``."""
        pattern = re.compile(self._extract_sanitise_pattern(src))
        text = "[ref](url) | pipe"
        assert pattern.sub(" ", text) == text


class TestMitigationConfigInvariants:
    """Smoke tests that the suite configuration matches the repo state."""

    def test_handler_module_paths_exist(self, mitigation_config: MitigationSuiteConfig) -> None:
        """Every handler module referenced by the suite is present on disk."""
        for relative in mitigation_config.handler_module_paths.values():
            assert (mitigation_config.repo_root / relative).exists(), f"missing module: {relative}"

    def test_sentinel_module_exists(self, mitigation_config: MitigationSuiteConfig) -> None:
        """The sentinel module that hosts ``sanitize_content`` is present."""
        assert (mitigation_config.repo_root / mitigation_config.sentinel_path).exists()

    def test_sentinel_function_exposed(self, mitigation_config: MitigationSuiteConfig) -> None:
        """``sanitize_content`` is importable for behavioural tests."""
        src = _read_module(mitigation_config, mitigation_config.sentinel_path)
        names = {
            node.name
            for node in ast.walk(ast.parse(src))
            if isinstance(node, ast.FunctionDef)
        }
        assert mitigation_config.sentinel_function in names
