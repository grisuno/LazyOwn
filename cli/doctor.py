"""Environment health check (preflight doctor) for the LazyOwn framework.

Complements the setup wizard. Where ``wizard`` / ``wizard --check`` validate the
operator's *configuration* (the values in ``payload.json``), ``doctor`` validates
the *installation* itself: the running Python version, whether the virtual
environment is active, importability of the third-party packages that
``install.sh`` provisions, the presence of the C2 TLS certificates, the
``payload.json`` config file, the SecLists wordlists, and the external kill-chain
tooling.

Design contract:
    - Zero imports from ``lazyown.py`` or ``lazyc2.py`` (Dependency Inversion);
      the command surface depends on this module, never the reverse.
    - Pure check functions return :class:`CheckResult` objects and never print,
      so they are unit-testable without capturing stdout. Rendering is isolated
      in :func:`render_report`.
    - External-tool and SecLists detection is delegated to :mod:`cli.wizard` so
      the framework keeps a single source of truth for those checks (DRY).
    - System-touching dependencies (the package finder, the binary checker, the
      filesystem root) are injected so tests can stub them deterministically.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.wizard import (
    BinaryStatus,
    _find_seclists_root,
    check_binaries,
)

MIN_PYTHON_VERSION: tuple[int, int] = (3, 10)

STATUS_OK = "ok"
STATUS_WARN = "warn"
STATUS_FAIL = "fail"

_CERT_FILES: tuple[str, str] = ("cert.pem", "key.pem")
_PAYLOAD_FILE = "payload.json"
_VENV_DIR = "env"


@dataclass(frozen=True)
class PackageSpec:
    """Declarative description of a Python dependency the framework imports.

    Attributes:
        import_name: Module name passed to the import machinery. Differs from
            the distribution name for several packages (``yaml`` vs ``pyyaml``,
            ``bs4`` vs ``beautifulsoup4``, ``Crypto`` vs ``pycryptodome``).
        pip_name: Distribution name shown in the remediation hint.
        purpose: One-line description of what breaks without the package.
        required: When ``True`` a missing package is a hard failure; when
            ``False`` it is advisory because only an optional feature degrades.
    """

    import_name: str
    pip_name: str
    purpose: str
    required: bool


_REQUIRED_PACKAGES: tuple[PackageSpec, ...] = (
    PackageSpec("cmd2", "cmd2", "Interactive CLI shell engine", True),
    PackageSpec("flask", "flask", "C2 web server", True),
    PackageSpec("flask_socketio", "flask-socketio", "C2 real-time sockets", True),
    PackageSpec("requests", "requests", "HTTP client used across recon", True),
    PackageSpec("rich", "rich", "Terminal rendering (wizard, doctor, hints)", True),
    PackageSpec("yaml", "pyyaml", "Addon and playbook parsing", True),
    PackageSpec("pandas", "pandas", "Session report and tabular data", True),
    PackageSpec("pyarrow", "pyarrow", "Parquet knowledge bases", True),
    PackageSpec("bs4", "beautifulsoup4", "HTML scraping for exploit search", True),
    PackageSpec("networkx", "networkx", "Surface and world-model graphs", True),
    PackageSpec("Crypto", "pycryptodome", "XOR and crypto helpers", True),
    PackageSpec("libnmap", "python-libnmap", "Nmap XML parsing", True),
    PackageSpec("scapy", "scapy", "ARP and packet helpers", False),
    PackageSpec("groq", "groq", "Groq LLM backend", False),
    PackageSpec("impacket", "impacket", "Active Directory and SMB tooling", False),
    PackageSpec("textual", "textual", "Dashboard TUI", False),
)


@dataclass(frozen=True)
class CheckResult:
    """Outcome of a single preflight check.

    Attributes:
        name: Short human-readable label for the check.
        status: One of :data:`STATUS_OK`, :data:`STATUS_WARN`, :data:`STATUS_FAIL`.
        detail: Description of what was found.
        hint: Optional remediation command shown when the check is not ``ok``.
    """

    name: str
    status: str
    detail: str
    hint: str = ""


@dataclass
class DoctorReport:
    """Aggregated result of a full preflight run."""

    checks: list[CheckResult] = field(default_factory=list)

    @property
    def failures(self) -> list[CheckResult]:
        """Return the checks whose status is :data:`STATUS_FAIL`."""
        return [c for c in self.checks if c.status == STATUS_FAIL]

    @property
    def warnings(self) -> list[CheckResult]:
        """Return the checks whose status is :data:`STATUS_WARN`."""
        return [c for c in self.checks if c.status == STATUS_WARN]

    @property
    def healthy(self) -> bool:
        """Return ``True`` when no check failed (warnings are tolerated)."""
        return not self.failures

    @property
    def overall_status(self) -> str:
        """Return the worst status across every check."""
        if self.failures:
            return STATUS_FAIL
        if self.warnings:
            return STATUS_WARN
        return STATUS_OK


def check_python_version(
    version_info: Sequence[int] = sys.version_info,
) -> CheckResult:
    """Verify the interpreter satisfies :data:`MIN_PYTHON_VERSION`.

    Args:
        version_info: Two-or-more element sequence of ``(major, minor, ...)``.
            Injected so tests can assert both the satisfied and unsatisfied
            branches without spawning a second interpreter.

    Returns:
        A :class:`CheckResult` flagged ``fail`` below the minimum version.
    """
    major, minor = version_info[0], version_info[1]
    current = f"{major}.{minor}"
    required = f"{MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}"
    if (major, minor) >= MIN_PYTHON_VERSION:
        return CheckResult("Python version", STATUS_OK, f"{current} (>= {required})")
    return CheckResult(
        "Python version",
        STATUS_FAIL,
        f"{current} is older than the required {required}",
        hint="Install Python 3.10+ and rebuild the virtual environment",
    )


def check_virtualenv(
    *,
    prefix: str = sys.prefix,
    base_prefix: str | None = getattr(sys, "base_prefix", None),
    root: Path,
) -> CheckResult:
    """Report whether the framework is running inside its virtual environment.

    Args:
        prefix: Active interpreter prefix (``sys.prefix``).
        base_prefix: System interpreter prefix (``sys.base_prefix``). ``None``
            collapses to ``prefix`` for ancient interpreters.
        root: Repository root used to locate the ``env/`` directory.

    Returns:
        ``ok`` when an isolated environment is active; ``warn`` otherwise so the
        operator is nudged to activate ``env/`` without blocking the session.
    """
    resolved_base = base_prefix if base_prefix is not None else prefix
    if prefix != resolved_base:
        return CheckResult("Virtual environment", STATUS_OK, f"active at {prefix}")
    env_path = root / _VENV_DIR
    if env_path.is_dir():
        return CheckResult(
            "Virtual environment",
            STATUS_WARN,
            "env/ exists but is not active",
            hint="source env/bin/activate",
        )
    return CheckResult(
        "Virtual environment",
        STATUS_WARN,
        "no virtual environment detected",
        hint="bash install.sh",
    )


def check_packages(
    specs: Sequence[PackageSpec] = _REQUIRED_PACKAGES,
    finder: Callable[[str], object | None] = importlib.util.find_spec,
) -> list[CheckResult]:
    """Verify every dependency in ``specs`` is importable without importing it.

    Uses :func:`importlib.util.find_spec` so the check stays side-effect free:
    no third-party module is actually executed, mirroring the safety contract of
    :func:`cli.wizard.check_binaries`.

    Args:
        specs: Package specifications to verify.
        finder: ``find_spec``-compatible callable. Injected for tests.

    Returns:
        One :class:`CheckResult` per spec, in input order.
    """
    results: list[CheckResult] = []
    for spec in specs:
        present = False
        try:
            present = finder(spec.import_name) is not None
        except (ImportError, ModuleNotFoundError, ValueError):
            present = False
        if present:
            results.append(CheckResult(spec.import_name, STATUS_OK, spec.purpose))
        else:
            status = STATUS_FAIL if spec.required else STATUS_WARN
            results.append(
                CheckResult(
                    spec.import_name,
                    status,
                    spec.purpose,
                    hint=f"pip install {spec.pip_name}",
                )
            )
    return results


def check_certificates(root: Path) -> CheckResult:
    """Verify the self-signed C2 certificate pair exists.

    Args:
        root: Repository root containing ``cert.pem`` / ``key.pem``.

    Returns:
        ``warn`` when either file is missing because the certificates are only
        needed once the C2 starts, not for CLI-only recon.
    """
    missing = [name for name in _CERT_FILES if not (root / name).is_file()]
    if not missing:
        return CheckResult("C2 certificates", STATUS_OK, "cert.pem and key.pem present")
    return CheckResult(
        "C2 certificates",
        STATUS_WARN,
        f"missing {', '.join(missing)}",
        hint="bash gen_cert.sh",
    )


def check_payload(root: Path) -> CheckResult:
    """Verify ``payload.json`` exists in the repository root.

    Args:
        root: Repository root.

    Returns:
        ``fail`` when absent because every component reads this single config
        source; the framework cannot run without it.
    """
    if (root / _PAYLOAD_FILE).is_file():
        return CheckResult("Config file", STATUS_OK, f"{_PAYLOAD_FILE} present")
    return CheckResult(
        "Config file",
        STATUS_FAIL,
        f"{_PAYLOAD_FILE} not found",
        hint="cp payload.example.json payload.json  (or run wizard)",
    )


def check_seclists(
    finder: Callable[[], str | None] = _find_seclists_root,
) -> CheckResult:
    """Verify a SecLists installation is discoverable on disk.

    Args:
        finder: Callable returning the SecLists root or ``None``. Defaults to
            :func:`cli.wizard._find_seclists_root` so the candidate paths are
            defined once.

    Returns:
        ``warn`` when not found because wordlist paths can be set manually.
    """
    root = finder()
    if root:
        return CheckResult("SecLists", STATUS_OK, root)
    return CheckResult(
        "SecLists",
        STATUS_WARN,
        "no SecLists installation found",
        hint="sudo apt install seclists",
    )


def check_external_tools(
    checker: Callable[[], list[BinaryStatus]] = check_binaries,
) -> list[CheckResult]:
    """Adapt :func:`cli.wizard.check_binaries` into preflight check results.

    Missing external tools are reported as ``warn`` rather than ``fail`` because
    each tool only powers a subset of the kill-chain; recon can proceed while,
    for example, ``evil-winrm`` is absent.

    Args:
        checker: Callable returning :class:`cli.wizard.BinaryStatus` items.

    Returns:
        One :class:`CheckResult` per external tool.
    """
    results: list[CheckResult] = []
    for status in checker():
        spec = status.spec
        if status.present:
            results.append(CheckResult(spec.name, STATUS_OK, spec.purpose))
        else:
            results.append(CheckResult(spec.name, STATUS_WARN, spec.purpose, hint=spec.install_hint))
    return results


def gather_report(root: Path) -> DoctorReport:
    """Run every preflight check and collect the results without printing.

    Args:
        root: Repository root used for file-presence checks.

    Returns:
        A populated :class:`DoctorReport`.
    """
    report = DoctorReport()
    report.checks.append(check_python_version())
    report.checks.append(check_virtualenv(root=root))
    report.checks.append(check_payload(root))
    report.checks.append(check_certificates(root))
    report.checks.append(check_seclists())
    report.checks.extend(check_packages())
    report.checks.extend(check_external_tools())
    return report


def _status_cell(status: str) -> Text:
    if status == STATUS_OK:
        return Text(STATUS_OK, style="bold green")
    if status == STATUS_FAIL:
        return Text(STATUS_FAIL, style="bold red")
    return Text(status, style="yellow")


def render_report(report: DoctorReport, console: Console | None = None) -> None:
    """Render a :class:`DoctorReport` as a rich table with a summary banner.

    Args:
        report: The report to display.
        console: Optional rich console; a default highlight-free console is
            created when omitted.
    """
    out = console or Console(highlight=False, soft_wrap=True)
    table = Table(
        title="LazyOwn preflight check",
        border_style="cyan",
        show_lines=False,
    )
    table.add_column("Check", style="white", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Detail / remediation", style="dim")

    for check in report.checks:
        detail = check.detail
        if check.status != STATUS_OK and check.hint:
            detail = f"{check.detail} -- {check.hint}"
        table.add_row(check.name, _status_cell(check.status), detail)

    out.print()
    out.print(table)

    fail_n = len(report.failures)
    warn_n = len(report.warnings)
    if report.overall_status == STATUS_OK:
        body = "[bold green]All checks passed — the environment is ready.[/]"
        border = "green"
    elif report.overall_status == STATUS_WARN:
        body = f"[bold yellow]{warn_n} warning(s).[/] Core install is healthy; some optional features will be skipped."
        border = "yellow"
    else:
        body = (
            f"[bold red]{fail_n} blocking failure(s)[/] and {warn_n} warning(s). "
            "Resolve the failures before running an engagement."
        )
        border = "red"
    out.print(Panel(body, border_style=border, padding=(0, 2)))
    out.print()


def run(root: Path | None = None, console: Console | None = None) -> DoctorReport:
    """Gather and render the preflight report.

    Args:
        root: Repository root. Defaults to the parent of this package.
        console: Optional rich console for rendering.

    Returns:
        The :class:`DoctorReport` so callers can inspect the result
        programmatically (for example to choose a process exit code).
    """
    resolved_root = root if root is not None else Path(__file__).resolve().parent.parent
    report = gather_report(resolved_root)
    render_report(report, console)
    return report


__all__ = [
    "CheckResult",
    "DoctorReport",
    "PackageSpec",
    "check_certificates",
    "check_external_tools",
    "check_packages",
    "check_payload",
    "check_python_version",
    "check_seclists",
    "check_virtualenv",
    "gather_report",
    "render_report",
    "run",
]
