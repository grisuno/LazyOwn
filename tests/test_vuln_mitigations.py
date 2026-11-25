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
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

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
            "lazyphishingai.py": "modules/legacy/lazyphishingai.py",
        }
    )

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
        return _read_module(mitigation_config, mitigation_config.handler_module_paths["lazyphishingai.py"])

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
        assert 'jsonify({"error": str(ex)})' not in phishingai_src
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


class TestMitigationConfigInvariants:
    """Smoke tests that the suite configuration matches the repo state."""

    def test_handler_module_paths_exist(self, mitigation_config: MitigationSuiteConfig) -> None:
        """Every handler module referenced by the suite is present on disk."""
        for relative in mitigation_config.handler_module_paths.values():
            assert (mitigation_config.repo_root / relative).exists(), f"missing module: {relative}"

