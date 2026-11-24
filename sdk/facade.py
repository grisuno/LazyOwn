"""The LazyOwn programmatic facade (``Lazy``).

``Lazy`` is the single, stable, standalone entry point that a lazymode
script (Python in a subprocess, or Lua in a lupa runtime) imports to do
in one call what used to take many separate MCP tool round-trips. It
composes the lower layers (``core`` config and process primitives,
``modules`` parsers) behind a small typed surface:

    lazy.config   read and write payload.json with schema validation
    lazy.sessions read and list campaign artefacts, path-traversal safe
    lazy.recon    run and parse nmap against an in-scope target
    lazy.sh       escape hatch: run one shell command, scope-checked
    lazy.search_exploits   searchsploit lookup

The facade never imports the CLI shell or the Flask C2, so it boots in a
fresh subprocess without the cmd2/Flask startup cost. Offensive helpers
consult an injected ``scope_check`` callback so scope enforcement is not
bypassed; the command runner is injectable so the surface is testable
without touching the network.
"""

from __future__ import annotations

import os
import shlex
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from core.config import load_payload, save_payload
from core.payload_schema import coerce_value, validate_value
from core.process import is_binary_present, run_command
from sdk.errors import ConfigValidationError, SessionPathError

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_PAYLOAD_PATH = _REPO_ROOT / "payload.json"
_DEFAULT_SESSIONS_DIR = _REPO_ROOT / "sessions"

_DEFAULT_NMAP_FLAGS = "-sV -T4"
_DEFAULT_SH_TIMEOUT = 300.0
_DEFAULT_NMAP_TIMEOUT = 1800.0
_DEFAULT_SEARCH_TIMEOUT = 60.0
_DEFAULT_READ_MAX_BYTES = 10 * 1024 * 1024
_SCAN_ARTIFACT_TEMPLATE = "scan_{target}.nmap.xml"
_SAFE_NAME_EXTRA = "-_."

CommandRunner = Callable[[str, float | None], str]
ScopeCheck = Callable[[str, str], None]


def _safe_session_name(name: str, sessions_dir: Path) -> Path:
    """Resolve *name* to an absolute path confined to *sessions_dir*.

    Applies the mandatory two-layer defence. First every path segment is
    checked against a whitelist (alphanumerics plus ``-_.``) and rejected
    if it is a traversal token, so nested artefacts such as
    ``logs/beacon.log`` or ``10.0.0.1/80/http/out.txt`` are supported
    while ``..`` segments, absolute paths and backslashes are refused.
    Then an ``os.path.realpath`` prefix check confirms the resolved path
    stays inside the sessions directory.

    Args:
        name: Operator- or script-supplied artefact path, possibly nested.
        sessions_dir: The only directory session reads are allowed in.

    Returns:
        The validated absolute path inside *sessions_dir*.

    Raises:
        SessionPathError: When a segment is invalid or the resolved path
            escapes *sessions_dir*.
    """
    raw = str(name).strip()
    if not raw or raw.startswith("/") or "\\" in raw:
        raise SessionPathError("Invalid session artefact name")
    segments = [part for part in raw.split("/") if part not in ("", ".")]
    if not segments:
        raise SessionPathError("Invalid session artefact name")
    for part in segments:
        if part == ".." or any(c not in _SAFE_NAME_EXTRA and not c.isalnum() for c in part):
            raise SessionPathError("Invalid session artefact name")
    allowed = os.path.realpath(sessions_dir)
    candidate = os.path.realpath(os.path.join(allowed, *segments))
    if candidate != allowed and not candidate.startswith(allowed + os.sep):
        raise SessionPathError("Session path traversal blocked")
    return Path(candidate)


class ConfigApi:
    """Typed read and write access to ``payload.json``.

    Reads are always fresh so an operator edit made through the CLI while
    a lazymode script runs is observed. Writes are coerced and validated
    against the payload schema before they are persisted.
    """

    def __init__(self, payload_path: Path) -> None:
        """Bind the config API to a concrete payload file.

        Args:
            payload_path: Absolute path of the ``payload.json`` to serve.
        """
        self._payload_path = payload_path

    def all(self) -> dict[str, Any]:
        """Return the entire current payload as a fresh dict."""
        return load_payload(self._payload_path)

    def get(self, key: str, default: Any = None) -> Any:
        """Return one payload value.

        Args:
            key: Payload key to read.
            default: Value returned when the key is absent.

        Returns:
            The stored value, or *default* when the key is missing.
        """
        return self.all().get(key, default)

    def set(self, key: str, value: Any) -> Any:
        """Coerce, validate and persist one payload value.

        Args:
            key: Payload key to write.
            value: Raw value; coerced to the key's schema kind first.

        Returns:
            The coerced value that was persisted.

        Raises:
            ConfigValidationError: When the coerced value fails schema
                validation for *key*.
        """
        coerced = coerce_value(key, value)
        issue = validate_value(key, coerced)
        if issue is not None:
            raise ConfigValidationError(f"{key}: {getattr(issue, 'message', issue)}")
        data = self.all()
        data[key] = coerced
        save_payload(data, self._payload_path)
        return coerced


class SessionsApi:
    """Path-traversal-safe access to the ``sessions/`` campaign artefacts."""

    def __init__(self, sessions_dir: Path) -> None:
        """Bind the sessions API to the campaign-state directory.

        Args:
            sessions_dir: Absolute path of the ``sessions/`` directory.
        """
        self._sessions_dir = sessions_dir

    def list(self, pattern: str = "*") -> list[str]:
        """Return artefact names in the sessions directory.

        Args:
            pattern: Glob pattern matched against top-level entries.

        Returns:
            Sorted artefact names, empty when the directory is absent.
        """
        if not self._sessions_dir.is_dir():
            return []
        return sorted(p.name for p in self._sessions_dir.glob(pattern) if p.is_file())

    def path(self, name: str) -> str:
        """Return the validated absolute path of a session artefact.

        Args:
            name: Artefact name to resolve.

        Returns:
            The absolute path confined to the sessions directory.
        """
        return str(_safe_session_name(name, self._sessions_dir))

    def read(self, name: str, max_bytes: int = _DEFAULT_READ_MAX_BYTES) -> str:
        """Return the text content of a session artefact.

        Args:
            name: Artefact name to read.
            max_bytes: Upper bound on the number of bytes read.

        Returns:
            The decoded file content, empty when the artefact is absent.
        """
        target = _safe_session_name(name, self._sessions_dir)
        if not target.is_file():
            return ""
        with open(target, "rb") as handle:
            raw = handle.read(max_bytes)
        return raw.decode("utf-8", errors="replace")


class ReconApi:
    """Run and parse nmap against a scope-checked target."""

    def __init__(
        self,
        sessions_dir: Path,
        run: CommandRunner,
        scope_check: ScopeCheck,
    ) -> None:
        """Bind the recon API to its directory, runner and scope check.

        Args:
            sessions_dir: Directory scan artefacts are written to.
            run: Command runner returning combined captured output.
            scope_check: Callback raising when a target is out of scope.
        """
        self._sessions_dir = sessions_dir
        self._run = run
        self._scope_check = scope_check

    def nmap(
        self,
        target: str,
        flags: str = _DEFAULT_NMAP_FLAGS,
        timeout: float = _DEFAULT_NMAP_TIMEOUT,
    ) -> list[dict[str, Any]]:
        """Scan *target*, persist the XML artefact and return services.

        Args:
            target: Host to scan; checked against the engagement scope.
            flags: nmap flags controlling the scan technique.
            timeout: Maximum scan runtime in seconds.

        Returns:
            Parsed service rows (port, protocol, service, product,
            version) for the scanned target.

        Raises:
            ScopeBlocked: When *target* is out of scope under enforcement.
            RuntimeError: When the nmap binary is not installed.
        """
        self._scope_check(f"nmap {flags}", target)
        if not is_binary_present("nmap"):
            raise RuntimeError("nmap binary not found")
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        xml_path = _safe_session_name(_SCAN_ARTIFACT_TEMPLATE.format(target=target), self._sessions_dir)
        command = f"nmap {flags} -oX {shlex.quote(str(xml_path))} {shlex.quote(target)}"
        self._run(command, timeout)
        return self.ports(target)

    def ports(self, target: str) -> list[dict[str, Any]]:
        """Return parsed services from the freshest scan artefact.

        Args:
            target: Host whose scan artefact is parsed.

        Returns:
            Parsed service rows, empty when no scan artefact exists.
        """
        from modules.nmap_fingerprint import find_nmap_xml
        from modules.scan_brief import parse_nmap_services

        candidates: Iterable[str] = find_nmap_xml(target, str(self._sessions_dir))
        for candidate in candidates:
            rows = parse_nmap_services(candidate)
            if rows:
                return rows
        return []


class Lazy:
    """The LazyOwn programmatic facade.

    Instantiate once per lazymode script and reach the framework through
    its namespaces. All offensive helpers are scope-checked; the command
    runner and scope check are injectable so the surface is testable and
    so a runner can enforce the operator's scope posture.
    """

    def __init__(
        self,
        payload_path: str | os.PathLike[str] | None = None,
        sessions_dir: str | os.PathLike[str] | None = None,
        scope_check: ScopeCheck | None = None,
        command_runner: CommandRunner | None = None,
    ) -> None:
        """Build the facade and its namespaces.

        Args:
            payload_path: Override for the ``payload.json`` path.
            sessions_dir: Override for the ``sessions/`` directory.
            scope_check: Callback raising ``ScopeBlocked`` for out-of-scope
                targets; when omitted the scope guard is dormant.
            command_runner: Runner returning combined captured output;
                defaults to the shared ``core.process.run_command``.
        """
        self._payload_path = Path(payload_path) if payload_path else _DEFAULT_PAYLOAD_PATH
        self._sessions_dir = Path(sessions_dir) if sessions_dir else _DEFAULT_SESSIONS_DIR
        self._scope_check: ScopeCheck = scope_check or (lambda command, target: None)
        self._run: CommandRunner = command_runner or run_command
        self.config = ConfigApi(self._payload_path)
        self.sessions = SessionsApi(self._sessions_dir)
        self.recon = ReconApi(self._sessions_dir, self._run, self._scope_check)

    def sh(self, command: str, timeout: float | None = _DEFAULT_SH_TIMEOUT) -> str:
        """Run one shell command and return its combined output.

        The escape hatch for operations without a dedicated namespace. The
        command is passed through the scope check with an empty target, so
        a scope posture that cannot resolve a target stays fail-open.

        Args:
            command: Shell command line to execute.
            timeout: Optional per-command timeout in seconds.

        Returns:
            The combined stdout and stderr output.
        """
        self._scope_check(command, "")
        return self._run(command, timeout)

    def search_exploits(self, query: str, timeout: float = _DEFAULT_SEARCH_TIMEOUT) -> str:
        """Return searchsploit results for *query*.

        Args:
            query: Service and version text to search for.
            timeout: Maximum search runtime in seconds.

        Returns:
            The searchsploit output, or a notice when the binary is
            absent.
        """
        if not is_binary_present("searchsploit"):
            return "searchsploit binary not found"
        return self._run(f"searchsploit {shlex.quote(query)}", timeout)
