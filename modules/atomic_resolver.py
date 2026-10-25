"""Central MITRE ATT&CK <-> Atomic Red Team translator.

Single source of truth for resolving human-friendly technique IDs
(T1078, T1059.001) to concrete Atomic Red Team tests (GUID + command)
and vice versa. Consumed by CLI (atomic_tests / atomic_gen),
MCP (lazyown_atomic_resolve / lazyown_ttp_chain), playbook_engine,
and the autonomous loop.

Security invariants:
    1. No shell execution — repo sync uses safe_git_clone (argv list).
    2. All technique IDs validated against strict regex before use.
    3. All GUIDs validated as UUID before use.
    4. YAML parsed with yaml.safe_load, per-file size cap, symlink safe.
    5. Resolved paths confined under the atomics directory (no traversal).
    6. No credentials, no network except explicit ensure_repo().
"""

from __future__ import annotations

import glob
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

log = logging.getLogger("atomic_resolver")

_BASE_DIR = Path(__file__).resolve().parent.parent
_DEFAULT_ATOMICS = _BASE_DIR / "external" / ".exploit" / "atomic-red-team" / "atomics"
_ATOMIC_REPO_URL = "https://github.com/redcanaryco/atomic-red-team.git"

_MITRE_RE = re.compile(r"^T\d{4}(\.\d{3})?$")
_GUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
_PLATFORM_ALLOWLIST = frozenset(
    {
        "windows",
        "macos",
        "linux",
        "office-365",
        "azure-ad",
        "google-workspace",
        "saas",
        "iaas",
        "containers",
        "iaas:aws",
        "iaas:azure",
        "iaas:gcp",
    }
)

_MAX_YAML_BYTES = 2_000_000
_MAX_INDEX_FILES = 5000


def normalize_mitre_id(raw: str) -> str:
    """Normalize and validate a MITRE technique ID.

    Args:
        raw: Candidate ID such as ``t1078``, `` T1059.001 ``.

    Returns:
        Uppercased canonical ID (``T1078``, ``T1059.001``).

    Raises:
        ValueError: If the value is not a valid technique ID.
    """
    candidate = (raw or "").strip().upper()
    if not _MITRE_RE.match(candidate):
        raise ValueError(f"Invalid MITRE technique ID: {raw!r}")
    return candidate


def is_mitre_id(raw: str) -> bool:
    """Return True when *raw* looks like a MITRE technique ID."""
    try:
        normalize_mitre_id(raw)
        return True
    except ValueError:
        return False


def normalize_guid(raw: str) -> str:
    """Normalize and validate an Atomic test GUID.

    Raises:
        ValueError: If the value is not a UUID.
    """
    candidate = (raw or "").strip().lower()
    if not _GUID_RE.match(candidate):
        raise ValueError(f"Invalid Atomic test GUID: {raw!r}")
    try:
        uuid.UUID(candidate)
    except ValueError as exc:
        raise ValueError(f"Invalid Atomic test GUID: {raw!r}") from exc
    return candidate


def is_guid(raw: str) -> bool:
    """Return True when *raw* looks like an Atomic test GUID."""
    try:
        normalize_guid(raw)
        return True
    except ValueError:
        return False


def normalize_platform(raw: str) -> str:
    """Validate a platform against the allowlist.

    Raises:
        ValueError: On unknown platform.
    """
    candidate = (raw or "").strip().lower()
    if candidate not in _PLATFORM_ALLOWLIST:
        raise ValueError(f"Unknown platform: {raw!r}")
    return candidate


@dataclass
class AtomicTest:
    """One concrete Atomic Red Team test."""

    guid: str = ""
    name: str = ""
    description: str = ""
    platforms: list[str] = field(default_factory=list)
    command: str = ""
    prereq_command: str = ""
    get_prereq_command: str = ""
    cleanup_command: str = ""
    executor_name: str = ""
    input_arguments: dict[str, Any] = field(default_factory=dict)
    mitre_id: str = ""

    @property
    def mitre_url(self) -> str:
        """Return the ATT&CK URL for this test."""
        return f"https://attack.mitre.org/techniques/{self.mitre_id.replace('.', '/')}"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "guid": self.guid,
            "atomic_id": self.guid,
            "name": self.name,
            "description": self.description,
            "platforms": list(self.platforms),
            "command": self.command,
            "prereq_command": self.prereq_command,
            "get_prereq_command": self.get_prereq_command,
            "cleanup_command": self.cleanup_command,
            "executor": self.executor_name,
            "input_arguments": dict(self.input_arguments),
            "mitre_id": self.mitre_id,
            "technique_id": self.mitre_id,
            "mitre_url": self.mitre_url,
        }


def _safe_yaml_files(atomics_dir: Path) -> list[Path]:
    """List YAML files confined under *atomics_dir*."""
    base = atomics_dir.resolve()
    pattern = str(base / "**" / "*.yaml")
    out: list[Path] = []
    for found in glob.glob(pattern, recursive=True)[:_MAX_INDEX_FILES]:
        try:
            candidate = Path(found).resolve()
            if base not in candidate.parents and candidate != base:
                continue
            if candidate.is_symlink() and base not in candidate.resolve().parents:
                continue
            if candidate.stat().st_size > _MAX_YAML_BYTES:
                log.warning("Skipping oversized atomic YAML: %s", candidate)
                continue
            out.append(candidate)
        except OSError:
            continue
    return out


def _test_from_raw(test: dict[str, Any], mitre_id: str) -> AtomicTest:
    """Build an AtomicTest from one raw atomic_tests entry."""
    deps = test.get("dependencies") or [{}]
    first_dep = deps[0] if isinstance(deps, list) and deps else {}
    if not isinstance(first_dep, dict):
        first_dep = {}
    executor = test.get("executor") or {}
    if not isinstance(executor, dict):
        executor = {}
    inputs = test.get("input_arguments") or {}
    if not isinstance(inputs, dict):
        inputs = {}
    return AtomicTest(
        guid=str(test.get("auto_generated_guid", "")),
        name=str(test.get("name", "")),
        description=str(test.get("description", "")),
        platforms=list(test.get("supported_platforms", []) or []),
        command=str(executor.get("command", "") or ""),
        prereq_command=str(first_dep.get("prereq_command", "") or ""),
        get_prereq_command=str(first_dep.get("get_prereq_command", "") or ""),
        cleanup_command=str(executor.get("cleanup_command", "") or ""),
        executor_name=str(executor.get("name", "") or ""),
        input_arguments=dict(inputs),
        mitre_id=mitre_id,
    )


class AtomicResolver:
    """Index and resolve Atomic Red Team tests by MITRE ID or GUID.

    Args:
        atomics_dir: Directory holding ``<TECHNIQUE>/<TECHNIQUE>.yaml`` files.
    """

    def __init__(self, atomics_dir: Path | str = _DEFAULT_ATOMICS) -> None:
        self._atomics = Path(atomics_dir)
        self._by_guid: dict[str, AtomicTest] = {}
        self._by_mitre: dict[str, list[str]] = {}
        self._indexed = False

    @property
    def available(self) -> bool:
        """Return True when the atomics directory exists."""
        return self._atomics.exists()

    def ensure_repo(self) -> bool:
        """Clone or pull the Atomic Red Team repo without shell.

        Returns:
            True when the atomics directory exists afterwards.
        """
        repo_root = self._atomics.parent
        if repo_root.exists():
            try:
                from core.safe_exec import safe_run_argv

                safe_run_argv(
                    ["git", "-C", str(repo_root), "pull", "--ff-only"],
                    timeout=120,
                )
            except Exception as exc:
                log.warning("Atomic repo pull failed: %s", exc)
            return self._atomics.exists()
        try:
            from core.safe_exec import safe_git_clone

            parent = repo_root.parent
            parent.mkdir(parents=True, exist_ok=True)
            safe_git_clone(_ATOMIC_REPO_URL, str(repo_root), timeout=300)
        except Exception as exc:
            log.warning("Atomic repo clone failed: %s", exc)
        return self._atomics.exists()

    def build_index(self, force: bool = False) -> dict[str, list[str]]:
        """Build the MITRE -> [GUID] index (cached unless *force*)."""
        if self._indexed and not force:
            return dict(self._by_mitre)
        if yaml is None:
            raise RuntimeError("PyYAML is required: pip install pyyaml")
        self._by_guid = {}
        self._by_mitre = {}
        if not self.available:
            return {}
        for yaml_file in _safe_yaml_files(self._atomics):
            try:
                with yaml_file.open("r", encoding="utf-8", errors="replace") as fh:
                    data = yaml.safe_load(fh)
            except Exception as exc:
                log.debug("Atomic parse skip %s: %s", yaml_file, exc)
                continue
            if not isinstance(data, dict) or "atomic_tests" not in data:
                continue
            mitre_id = str(data.get("attack_technique", "")).strip().upper()
            if not mitre_id or not is_mitre_id(mitre_id):
                continue
            tests = data.get("atomic_tests") or []
            if not isinstance(tests, list):
                continue
            for entry in tests:
                if not isinstance(entry, dict):
                    continue
                guid = str(entry.get("auto_generated_guid", "")).strip().lower()
                if not guid or not is_guid(guid):
                    continue
                parsed = _test_from_raw(entry, mitre_id)
                self._by_guid[guid] = parsed
                self._by_mitre.setdefault(mitre_id, [])
                if guid not in self._by_mitre[mitre_id]:
                    self._by_mitre[mitre_id].append(guid)
        self._indexed = True
        log.info("Atomic index: %d techniques, %d tests", len(self._by_mitre), len(self._by_guid))
        return dict(self._by_mitre)

    def guids_for_technique(self, mitre_id: str) -> list[str]:
        """Return GUIDs registered for a technique ID (empty when unknown)."""
        normalized = normalize_mitre_id(mitre_id)
        self.build_index()
        return list(self._by_mitre.get(normalized, []))

    def get_by_guid(self, guid: str) -> AtomicTest | None:
        """Return the test for a GUID, or None when unknown."""
        normalized = normalize_guid(guid)
        self.build_index()
        return self._by_guid.get(normalized)

    def list_for_technique(self, mitre_id: str, platform: str = "") -> list[AtomicTest]:
        """List tests for a technique, optionally filtered by platform."""
        normalized = normalize_mitre_id(mitre_id)
        wanted = ""
        if platform:
            wanted = normalize_platform(platform)
        self.build_index()
        out: list[AtomicTest] = []
        for guid in self._by_mitre.get(normalized, []):
            test = self._by_guid.get(guid)
            if test is None:
                continue
            if wanted and wanted not in [p.lower() for p in test.platforms]:
                continue
            out.append(test)
        return out

    def resolve(self, query: str, platform: str = "") -> list[AtomicTest]:
        """Resolve a MITRE ID, GUID, or prefix to matching tests.

        Args:
            query: ``T1078``, ``T1059.001``, a GUID, or a prefix like ``T1059``.
            platform: Optional platform filter.

        Returns:
            Matching tests (possibly empty). Never raises on unknown IDs;
            raises ValueError only on malformed platform filters.
        """
        text = (query or "").strip()
        if not text:
            return []
        wanted = ""
        if platform:
            wanted = normalize_platform(platform)
        self.build_index()
        if is_guid(text):
            found = self._by_guid.get(text.strip().lower())
            if found is None:
                return []
            if wanted and wanted not in [p.lower() for p in found.platforms]:
                return []
            return [found]
        upper = text.upper()
        if is_mitre_id(upper):
            exact = self.list_for_technique(upper, platform=wanted)
            if exact or "." in upper:
                return exact
            # Bare parent (e.g. T1059 with only T1059.001 indexed):
            # fall through to prefix scan below.
        if re.match(r"^T\d{1,4}$", upper):
            matches: list[AtomicTest] = []
            for mitre_id in sorted(self._by_mitre):
                if mitre_id == upper or mitre_id.startswith(upper + ".") or mitre_id.startswith(upper):
                    for guid in self._by_mitre[mitre_id]:
                        test = self._by_guid.get(guid)
                        if test is None:
                            continue
                        if wanted and wanted not in [p.lower() for p in test.platforms]:
                            continue
                        matches.append(test)
            return matches
        return []

    def chain(
        self,
        techniques: list[str],
        platform: str = "linux",
        first_match_only: bool = True,
    ) -> list[AtomicTest]:
        """Translate an ordered APT technique chain to concrete tests.

        Skips unknown techniques (logged) so one bad ID never aborts
        an autonomous emulation. Each known technique contributes its
        first platform-compatible test, or all of them when
        *first_match_only* is False.

        Args:
            techniques: Ordered MITRE IDs such as ``["T1078", "T1059.001"]``.
            platform: Platform filter applied to every technique.
            first_match_only: Keep only the first test per technique.
        """
        wanted = normalize_platform(platform) if platform else ""
        chain_out: list[AtomicTest] = []
        for raw in techniques or []:
            try:
                candidates = self.list_for_technique(raw, platform=wanted)
            except ValueError:
                log.warning("Skipping invalid technique in chain: %r", raw)
                continue
            if not candidates:
                log.info("No atomic test for technique %r platform=%s", raw, wanted)
                continue
            if first_match_only:
                chain_out.append(candidates[0])
            else:
                chain_out.extend(candidates)
        return chain_out

    def stats(self) -> dict[str, int]:
        """Return index counters."""
        self.build_index()
        return {"techniques": len(self._by_mitre), "tests": len(self._by_guid)}


_resolver: AtomicResolver | None = None


def get_resolver(atomics_dir: Path | str = _DEFAULT_ATOMICS) -> AtomicResolver:
    """Return the module-level resolver singleton."""
    global _resolver
    if _resolver is None:
        _resolver = AtomicResolver(atomics_dir)
    return _resolver


def resolve_technique(
    mitre_id: str,
    platform: str = "",
    atomics_dir: Path | str = _DEFAULT_ATOMICS,
) -> list[dict[str, Any]]:
    """Resolve a technique to JSON-serializable test dicts."""
    resolver = get_resolver(atomics_dir)
    return [t.to_dict() for t in resolver.list_for_technique(mitre_id, platform=platform)]


def resolve_chain(
    techniques: list[str],
    platform: str = "linux",
    atomics_dir: Path | str = _DEFAULT_ATOMICS,
) -> list[dict[str, Any]]:
    """Translate a technique chain to JSON-serializable test dicts."""
    resolver = get_resolver(atomics_dir)
    return [t.to_dict() for t in resolver.chain(techniques, platform=platform)]


def build_variables(
    test: AtomicTest | dict[str, Any],
    rhost: str = "",
    domain: str = "",
    rport: str = "",
    username: str = "",
    password: str = "",
) -> dict[str, str]:
    """Build #{variable} substitution map for a test.

    Unknown input_arguments fall back to their declared defaults so
    autonomous execution never blocks on interactive input.
    """
    if isinstance(test, dict):
        inputs = test.get("input_arguments", {}) or {}
    else:
        inputs = test.input_arguments
    variables: dict[str, str] = {
        "#{ip_address}": rhost,
        "#{endpoint_domain}": rhost,
        "#{username}": username,
        "#{password}": password,
        "#{domain}": domain,
        "#{port}": str(rport),
        "#{hostname}": domain,
    }
    for key, spec in inputs.items():
        token = f"#{{{key}}}"
        if token not in variables:
            default = ""
            if isinstance(spec, dict):
                default = str(spec.get("default", ""))
            variables[token] = default
    return variables


def render_command(template: str, variables: dict[str, str]) -> str:
    """Substitute #{variables} without shell interpretation."""
    rendered = str(template or "")
    for token, value in variables.items():
        rendered = rendered.replace(token, str(value))
    return rendered


def technique_env_override() -> str:
    """Return atomics dir override from env (empty when unset)."""
    return os.environ.get("LAZYOWN_ATOMICS_DIR", "").strip()
