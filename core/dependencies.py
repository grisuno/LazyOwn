"""Graceful optional-import handling for heavy third-party dependencies.

Historically ``utils.py`` imported every third-party library at module top
level. A single missing package (for example ``pycryptodome`` or
``python-libnmap``) raised :class:`ImportError` before any code ran, which
crashed the whole framework -- CLI, C2 and MCP server alike -- with an opaque
traceback and no guidance on how to recover.

This module makes optional dependencies fail late and loudly instead of early
and silently:

- :func:`optional_import` and :func:`optional_attr` return the real module or
  attribute when the package is installed (identical runtime behaviour), and a
  :class:`_DeferredImport` proxy when it is missing. The proxy raises
  :class:`MissingDependencyError` only when the feature is actually used, with
  the exact ``pip install`` command needed to fix it.
- :data:`OPTIONAL_PYTHON_DEPENDENCIES` is the single source of truth for the
  install hint of every dependency bound lazily by ``utils.py``.

Scope: this module owns *runtime resilience* for lazily-imported Python
packages only. The operator-facing preflight report (Python version, virtual
environment, external binaries, certificates, SecLists) lives in
:mod:`cli.doctor`, which is rendered with ``rich`` and reachable through the
``doctor`` CLI command. This module deliberately depends only on the Python
standard library so that ``python3 -m core.dependencies`` keeps working as a
last-resort diagnostic even when ``rich`` or ``cmd2`` themselves fail to
import.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any


class MissingDependencyError(ImportError):
    """Raised when an optional dependency is used but is not installed.

    The error message includes the import name, the owning feature and the
    exact ``pip install`` command that resolves it, so the operator never has
    to map a bare ``ModuleNotFoundError`` back to a package name by hand.
    """

    def __init__(self, import_name: str, pip_package: str, feature: str) -> None:
        """Build a remediation-oriented error message.

        Args:
            import_name: The dotted import path that failed (for example
                ``Crypto.Cipher``).
            pip_package: The PyPI distribution that provides ``import_name``.
            feature: Human-readable description of the capability that needs
                the dependency.
        """
        self.import_name = import_name
        self.pip_package = pip_package
        self.feature = feature
        super().__init__(
            f"Optional dependency '{import_name}' is required for {feature} "
            f"but is not installed. Install it with: pip install {pip_package} "
            f"(or run: pip install -r requirements.txt)."
        )


@dataclass(frozen=True)
class DependencySpec:
    """Declarative metadata for a single optional Python dependency.

    Attributes:
        import_name: The dotted import path consumed by the framework.
        pip_package: The PyPI distribution that provides ``import_name``.
        feature: Human-readable capability that the dependency unlocks.
    """

    import_name: str
    pip_package: str
    feature: str


OPTIONAL_PYTHON_DEPENDENCIES: dict[str, DependencySpec] = {
    "donut": DependencySpec("donut", "donut", "in-memory shellcode generation"),
    "pandas": DependencySpec("pandas", "pandas", "CSV and dataframe reporting"),
    "PIL": DependencySpec("PIL", "pillow", "image processing for captured media"),
    "lupa": DependencySpec("lupa", "lupa", "Lua plugin runtime"),
    "Crypto.Cipher": DependencySpec("Crypto.Cipher", "pycryptodome", "AES beacon encryption"),
    "Crypto.Util.Padding": DependencySpec("Crypto.Util.Padding", "pycryptodome", "AES block padding"),
    "pykeepass": DependencySpec("pykeepass", "pykeepass", "KeePass credential database parsing"),
    "stix2": DependencySpec("stix2", "stix2", "STIX threat-intelligence export"),
    "libnmap": DependencySpec("libnmap", "python-libnmap", "nmap scan parsing and orchestration"),
    "libnmap.parser": DependencySpec("libnmap.parser", "python-libnmap", "nmap XML result parsing"),
    "libnmap.process": DependencySpec("libnmap.process", "python-libnmap", "nmap process orchestration"),
    "netaddr": DependencySpec("netaddr", "netaddr", "IP address and range arithmetic"),
    "impacket.dcerpc.v5": DependencySpec("impacket.dcerpc.v5", "impacket", "DCE/RPC transport for Windows attacks"),
    "impacket.dcerpc.v5.dcomrt": DependencySpec(
        "impacket.dcerpc.v5.dcomrt", "impacket", "DCOM object exporter enumeration"
    ),
    "impacket.dcerpc.v5.rpcrt": DependencySpec("impacket.dcerpc.v5.rpcrt", "impacket", "DCE/RPC authentication levels"),
}


class _DeferredImport:
    """Stand-in for a missing optional dependency.

    The proxy is returned by :func:`optional_import` and :func:`optional_attr`
    when the underlying package cannot be imported. Binding the proxy to a name
    is safe; any attempt to actually use it (attribute access, call, iteration,
    subscription, length) raises :class:`MissingDependencyError` with
    installation guidance. This defers the failure from import time to first
    use, so the framework still boots. The proxy is falsy so callers can
    feature-detect with a plain ``if optional_dependency:`` guard.
    """

    __slots__ = ("_spec",)

    def __init__(self, spec: DependencySpec) -> None:
        """Store the dependency spec used to build remediation errors.

        Args:
            spec: Metadata describing the missing dependency.
        """
        object.__setattr__(self, "_spec", spec)

    def _raise(self) -> Any:
        """Raise a :class:`MissingDependencyError` for the proxied dependency.

        Raises:
            MissingDependencyError: Always.
        """
        spec: DependencySpec = object.__getattribute__(self, "_spec")
        raise MissingDependencyError(spec.import_name, spec.pip_package, spec.feature)

    def __getattr__(self, _name: str) -> Any:
        """Reject attribute access on a missing dependency."""
        return self._raise()

    def __call__(self, *_args: Any, **_kwargs: Any) -> Any:
        """Reject calling a missing dependency."""
        return self._raise()

    def __getitem__(self, _key: Any) -> Any:
        """Reject subscription of a missing dependency."""
        return self._raise()

    def __iter__(self) -> Any:
        """Reject iteration over a missing dependency."""
        return self._raise()

    def __len__(self) -> int:
        """Reject ``len()`` on a missing dependency."""
        return self._raise()

    def __bool__(self) -> bool:
        """Report the dependency as absent for feature-detection checks."""
        return False


def _spec_for(import_name: str, pip_package: str | None, feature: str | None) -> DependencySpec:
    """Resolve the canonical spec for ``import_name``.

    Looks the import name up in :data:`OPTIONAL_PYTHON_DEPENDENCIES` first so
    metadata lives in exactly one place. Falls back to caller-supplied values,
    then to sensible defaults, so an undeclared dependency still degrades
    gracefully.

    Args:
        import_name: The dotted import path being resolved.
        pip_package: Optional override for the PyPI distribution name.
        feature: Optional override for the capability description.

    Returns:
        A :class:`DependencySpec` describing the dependency.
    """
    registered = OPTIONAL_PYTHON_DEPENDENCIES.get(import_name)
    if registered is not None:
        return registered
    return DependencySpec(
        import_name=import_name,
        pip_package=pip_package or import_name,
        feature=feature or import_name,
    )


def optional_import(
    import_name: str,
    *,
    pip_package: str | None = None,
    feature: str | None = None,
) -> Any:
    """Import an optional module, returning a deferred proxy when absent.

    Args:
        import_name: The dotted module path to import.
        pip_package: Override for the PyPI distribution name. Ignored when
            ``import_name`` is already declared in the registry.
        feature: Override for the capability description. Ignored when
            ``import_name`` is already declared in the registry.

    Returns:
        The imported module when available, otherwise a :class:`_DeferredImport`
        proxy that raises :class:`MissingDependencyError` on first use.
    """
    spec = _spec_for(import_name, pip_package, feature)
    try:
        return importlib.import_module(import_name)
    except ImportError:
        return _DeferredImport(spec)


def optional_attr(
    import_name: str,
    attr: str,
    *,
    pip_package: str | None = None,
    feature: str | None = None,
) -> Any:
    """Import an attribute from an optional module, deferring failure.

    The ``attr`` may be a plain attribute (class, function, constant) or a
    submodule (for example ``AES`` in ``Crypto.Cipher``). When attribute
    access fails, the function transparently retries by importing
    ``f"{import_name}.{attr}"`` as a submodule, mirroring the semantics of
    ``from {import_name} import {attr}``.

    Args:
        import_name: The dotted module path to import.
        attr: The attribute or submodule to retrieve from the imported module.
        pip_package: Override for the PyPI distribution name. Ignored when
            ``import_name`` is already declared in the registry.
        feature: Override for the capability description. Ignored when
            ``import_name`` is already declared in the registry.

    Returns:
        The requested attribute or submodule when available, otherwise a
        :class:`_DeferredImport` proxy that raises
        :class:`MissingDependencyError` on first use.
    """
    spec = _spec_for(import_name, pip_package, feature)
    try:
        module = importlib.import_module(import_name)
    except ImportError:
        return _DeferredImport(spec)
    try:
        return getattr(module, attr)
    except AttributeError:
        pass
    try:
        return importlib.import_module(f"{import_name}.{attr}")
    except ImportError:
        return _DeferredImport(spec)


@dataclass(frozen=True)
class DependencyStatus:
    """Result of probing a single Python dependency.

    Attributes:
        spec: The dependency that was probed.
        available: ``True`` when the dependency imported successfully.
        detail: Installed version when available, otherwise the import error.
    """

    spec: DependencySpec
    available: bool
    detail: str


@dataclass(frozen=True)
class DependencyReport:
    """Aggregated readiness snapshot of the lazily-imported Python packages.

    Attributes:
        results: Status for every declared optional Python dependency.
    """

    results: tuple[DependencyStatus, ...]

    @property
    def missing(self) -> tuple[DependencyStatus, ...]:
        """Return the optional Python dependencies that are not installed."""
        return tuple(status for status in self.results if not status.available)

    @property
    def ok(self) -> bool:
        """Return ``True`` when every declared dependency is present."""
        return not self.missing


def probe_python_dependency(spec: DependencySpec) -> DependencyStatus:
    """Probe a single Python dependency by importing it.

    Args:
        spec: The dependency to probe.

    Returns:
        A :class:`DependencyStatus` describing availability and version.
    """
    try:
        module = importlib.import_module(spec.import_name)
    except ImportError as exc:
        return DependencyStatus(spec=spec, available=False, detail=str(exc))
    version = getattr(module, "__version__", "")
    root_name = spec.import_name.split(".", 1)[0]
    if not version and root_name != spec.import_name:
        try:
            root_module = importlib.import_module(root_name)
            version = getattr(root_module, "__version__", "")
        except ImportError:
            version = ""
    return DependencyStatus(spec=spec, available=True, detail=version or "installed")


def collect_dependency_report() -> DependencyReport:
    """Probe every declared optional Python dependency.

    Returns:
        A :class:`DependencyReport` aggregating the status of all dependencies
        in :data:`OPTIONAL_PYTHON_DEPENDENCIES`.
    """
    results = tuple(probe_python_dependency(spec) for spec in OPTIONAL_PYTHON_DEPENDENCIES.values())
    return DependencyReport(results=results)


def format_report(report: DependencyReport, *, use_color: bool = True) -> str:
    """Render a :class:`DependencyReport` as an aligned, human-readable block.

    Args:
        report: The report to render.
        use_color: When ``True`` wrap status markers in ANSI colour codes.

    Returns:
        A multi-line string suitable for printing to a terminal.
    """
    green = "\033[92m" if use_color else ""
    red = "\033[91m" if use_color else ""
    yellow = "\033[93m" if use_color else ""
    bold = "\033[1m" if use_color else ""
    reset = "\033[0m" if use_color else ""

    lines: list[str] = [
        f"{bold}LazyOwn optional Python dependencies{reset}",
        "",
    ]
    for status in report.results:
        if status.available:
            marker = f"{green}OK{reset}"
            note = status.detail
        else:
            marker = f"{red}MISSING{reset}"
            note = f"pip install {status.spec.pip_package}  ({status.spec.feature})"
        lines.append(f"  [{marker}] {status.spec.import_name:<28} {note}")

    lines.append("")
    if report.ok:
        lines.append(f"{green}All optional dependencies are installed.{reset}")
    else:
        lines.append(
            f"{yellow}{len(report.missing)} optional dependency(ies) missing. "
            f"The dependent features will raise a clear error when used. "
            f"Run: pip install -r requirements.txt{reset}"
        )
    lines.append(
        "For the full preflight check (binaries, certificates, SecLists) "
        "run the 'doctor' command inside the LazyOwn shell."
    )
    return "\n".join(lines)


def main() -> int:
    """Print the optional-dependency report and return a process exit code.

    Returns:
        ``0`` when every declared dependency is present, ``1`` otherwise. The
        non-zero code lets shell scripts gate on a clean environment.
    """
    report = collect_dependency_report()
    print(format_report(report))
    return 0 if report.ok else 1


__all__ = [
    "MissingDependencyError",
    "DependencySpec",
    "OPTIONAL_PYTHON_DEPENDENCIES",
    "optional_import",
    "optional_attr",
    "DependencyStatus",
    "DependencyReport",
    "probe_python_dependency",
    "collect_dependency_report",
    "format_report",
    "main",
]


if __name__ == "__main__":
    raise SystemExit(main())
