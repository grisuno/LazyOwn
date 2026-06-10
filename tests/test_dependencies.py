"""Tests for ``core.dependencies`` graceful optional-import handling.

These tests pin the behaviour the refactor relies on:

- An installed dependency resolves to the real module/attribute so runtime
  behaviour is byte-for-byte identical to a direct ``import``.
- A missing dependency never raises at import time; it returns a proxy that
  fails only on use, with a remediation message.
- ``utils.py`` still exposes every lazily-bound symbol so ``lazyown.py``'s
  ``from utils import *`` contract keeps working.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from core.dependencies import (
    OPTIONAL_PYTHON_DEPENDENCIES,
    DependencyReport,
    DependencySpec,
    DependencyStatus,
    MissingDependencyError,
    collect_dependency_report,
    format_report,
    main,
    optional_attr,
    optional_import,
    probe_python_dependency,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

_ABSENT_MODULE = "lazyown_nonexistent_dependency_xyz"
_LAZY_UTILS_SYMBOLS = (
    "AES",
    "pad",
    "pd",
    "donut",
    "libnmap",
    "Image",
    "LuaRuntime",
    "PyKeePass",
    "MemoryStore",
    "Filter",
    "NmapParser",
    "NmapProcess",
    "IPAddress",
    "IPRange",
    "transport",
    "IObjectExporter",
    "RPC_C_AUTHN_LEVEL_NONE",
)


def _run_in_subprocess(snippet: str) -> str:
    """Execute ``snippet`` in a clean subprocess and return trimmed stdout.

    Mirrors ``tests/test_core.py`` so ``utils.py`` argv parsing does not fire
    when the module is imported for assertions.

    Args:
        snippet: Python source executed with ``-c``.

    Returns:
        The trimmed standard output of the subprocess.
    """
    result = subprocess.run(
        [sys.executable, "-c", snippet],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


class TestMissingDependencyError:
    """The remediation error carries enough context to fix the install."""

    def test_message_contains_pip_command(self):
        err = MissingDependencyError("Crypto.Cipher", "pycryptodome", "AES encryption")
        message = str(err)
        assert "pip install pycryptodome" in message
        assert "Crypto.Cipher" in message
        assert "AES encryption" in message

    def test_attributes_are_exposed(self):
        err = MissingDependencyError("pkg", "dist", "feature")
        assert err.import_name == "pkg"
        assert err.pip_package == "dist"
        assert err.feature == "feature"

    def test_is_import_error_subclass(self):
        assert issubclass(MissingDependencyError, ImportError)


class TestOptionalImportPresent:
    """An installed module resolves to the real object."""

    def test_returns_real_module(self):
        module = optional_import("json")
        assert module.dumps({"a": 1}) == '{"a": 1}'

    def test_truthy_when_present(self):
        assert bool(optional_import("json")) is True


class TestOptionalImportAbsent:
    """A missing module degrades to a deferred proxy."""

    def test_returns_falsy_proxy(self):
        proxy = optional_import(_ABSENT_MODULE)
        assert bool(proxy) is False

    def test_attribute_access_raises(self):
        proxy = optional_import(_ABSENT_MODULE)
        with pytest.raises(MissingDependencyError):
            _ = proxy.anything

    def test_call_raises(self):
        proxy = optional_import(_ABSENT_MODULE)
        with pytest.raises(MissingDependencyError):
            proxy()

    def test_subscription_raises(self):
        proxy = optional_import(_ABSENT_MODULE)
        with pytest.raises(MissingDependencyError):
            _ = proxy["key"]

    def test_iteration_raises(self):
        proxy = optional_import(_ABSENT_MODULE)
        with pytest.raises(MissingDependencyError):
            list(proxy)

    def test_len_raises(self):
        proxy = optional_import(_ABSENT_MODULE)
        with pytest.raises(MissingDependencyError):
            len(proxy)


class TestOptionalAttr:
    """Attribute and submodule resolution mirror ``from x import y``."""

    def test_returns_real_attribute(self):
        dumps = optional_attr("json", "dumps")
        assert dumps({"a": 1}) == '{"a": 1}'

    def test_submodule_fallback(self):
        path_module = optional_attr("os", "path")
        assert path_module.join("a", "b").replace("\\", "/") == "a/b"

    def test_missing_module_returns_proxy(self):
        proxy = optional_attr(_ABSENT_MODULE, "thing")
        assert bool(proxy) is False
        with pytest.raises(MissingDependencyError):
            proxy()

    def test_missing_attribute_returns_proxy(self):
        proxy = optional_attr("json", "definitely_not_a_real_attribute")
        assert bool(proxy) is False
        with pytest.raises(MissingDependencyError):
            _ = proxy.value


class TestRegistry:
    """The dependency registry is the single source of truth and is complete."""

    def test_every_spec_is_fully_populated(self):
        for key, spec in OPTIONAL_PYTHON_DEPENDENCIES.items():
            assert isinstance(spec, DependencySpec)
            assert spec.import_name == key
            assert spec.pip_package, f"{key} has no pip package"
            assert spec.feature, f"{key} has no feature description"

    @pytest.mark.parametrize(
        "import_name",
        [
            "Crypto.Cipher",
            "Crypto.Util.Padding",
            "pandas",
            "donut",
            "libnmap",
            "libnmap.parser",
            "libnmap.process",
            "PIL",
            "lupa",
            "pykeepass",
            "stix2",
            "netaddr",
            "impacket.dcerpc.v5",
            "impacket.dcerpc.v5.dcomrt",
            "impacket.dcerpc.v5.rpcrt",
        ],
    )
    def test_lazily_bound_dependency_is_registered(self, import_name):
        assert import_name in OPTIONAL_PYTHON_DEPENDENCIES


class TestProbe:
    """Probing reports availability and version without raising."""

    def test_present_dependency(self):
        spec = DependencySpec("json", "json", "json encoding")
        status = probe_python_dependency(spec)
        assert status.available is True
        assert isinstance(status.detail, str)

    def test_absent_dependency(self):
        spec = DependencySpec(_ABSENT_MODULE, "nothing", "nothing")
        status = probe_python_dependency(spec)
        assert status.available is False
        assert status.detail


class TestReport:
    """The aggregate report classifies missing dependencies correctly."""

    def test_collect_returns_report(self):
        report = collect_dependency_report()
        assert isinstance(report, DependencyReport)
        assert len(report.results) == len(OPTIONAL_PYTHON_DEPENDENCIES)

    def test_missing_and_ok_consistency(self):
        present = DependencyStatus(DependencySpec("a", "a", "a"), True, "1.0")
        absent = DependencyStatus(DependencySpec("b", "b", "b"), False, "err")
        report = DependencyReport(results=(present, absent))
        assert report.ok is False
        assert report.missing == (absent,)

    def test_ok_report_has_no_missing(self):
        present = DependencyStatus(DependencySpec("a", "a", "a"), True, "1.0")
        report = DependencyReport(results=(present,))
        assert report.ok is True
        assert report.missing == ()

    def test_format_report_renders_markers(self):
        present = DependencyStatus(DependencySpec("a", "a", "feat a"), True, "1.0")
        absent = DependencyStatus(DependencySpec("b", "distb", "feat b"), False, "err")
        report = DependencyReport(results=(present, absent))
        text = format_report(report, use_color=False)
        assert "OK" in text
        assert "MISSING" in text
        assert "pip install distb" in text

    def test_main_returns_exit_code(self):
        code = main()
        assert code in (0, 1)


class TestUtilsIntegration:
    """``utils.py`` keeps exporting every lazily-bound symbol."""

    @pytest.mark.parametrize("name", _LAZY_UTILS_SYMBOLS)
    def test_symbol_is_exported(self, name):
        out = _run_in_subprocess(
            f"import sys; sys.argv=['utils_compat']; import utils; print(hasattr(utils, {name!r}))"
        )
        assert out == "True", f"utils.{name} missing — broken lazy-import binding"

    def test_is_binary_present_uses_path_lookup(self):
        out = _run_in_subprocess(
            "import sys; sys.argv=['utils_compat']; import utils; "
            "print(utils.is_binary_present('sh'), "
            "utils.is_binary_present('lazyown_definitely_missing_binary_xyz'))"
        )
        assert out == "True False"
