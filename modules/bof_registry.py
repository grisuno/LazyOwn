"""Beacon Object File (BOF) registry and marketplace for LazyOwn.

Catalogs, indexes, and manages BOFs compatible with the TrustedSec
SA BOF API. Supports both Windows COFF BOFs (Cobalt Strike compatible)
and Linux ELF BOFs (BlacksandBeacon). Provides search, install, info,
and update operations against a curated catalog.

The catalog is a static index of known BOFs with metadata: name,
description, author, repository URL, compatible platforms, required
arguments, MITRE ATT&CK technique references, and SHA-256 hashes.

Contracts:
    - BofEntry: immutable dataclass representing one BOF
    - BofCatalog: curated catalog of known BOFs
    - BofRegistry: manages installed BOFs on disk with version tracking
    - BofMarketplace: search/install/uninstall/info operations
    - BofValidator: validates BOF integrity (hash check, platform compatibility)

Design (SOLID):
    - Single Responsibility: catalog, registry, marketplace, and validation
      are separate classes with distinct concerns.
    - Open/Closed: new BOFs added via BofCatalog.register() without modifying
      the marketplace class.
    - Liskov: disk registry and in-memory catalog share no interface contract.
    - Interface Segregation: search, install, and validate are separate concerns.
    - Dependency Inversion: marketplace depends on catalog + registry abstractions.

Usage:
    from modules.bof_registry import BofMarketplace

    mp = BofMarketplace(sessions_dir="sessions")
    results = mp.search("ldap")
    for entry in results:
        print(entry.name, entry.description)
    mp.install("ldap_enum")
    mp.info("ldap_enum")
    mp.uninstall("ldap_enum")
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

log = logging.getLogger("bof_registry")

BOF_INSTALL_DIR_NAME = "bofs"
BOF_MANIFEST_FILENAME = "bof_manifest.json"
BOF_CACHE_FILENAME = "bof_cache.json"
DEFAULT_CATALOG_URL = "https://github.com/trustedsec/CS-Situational-Awareness-BOF"
CATALOG_CACHE_TTL_S = 86400


class BofPlatform(str, Enum):  # noqa: UP042
    """Target platform for a Beacon Object File."""

    WINDOWS = "windows"
    LINUX = "linux"


class BofCategory(str, Enum):  # noqa: UP042
    """Functional category of a BOF."""

    RECON = "reconnaissance"
    ENUM = "enumeration"
    CRED = "credential_access"
    PERSIST = "persistence"
    PRIVESC = "privilege_escalation"
    LAT = "lateral_movement"
    EVASION = "evasion"
    EXEC = "execution"
    COLLECTION = "collection"
    EXFIL = "exfiltration"
    GENERAL = "general"


@dataclass(frozen=True)
class BofEntry:
    """Immutable catalog entry for a single Beacon Object File.

    Attributes:
        name: Unique identifier (e.g., 'ldap_enum').
        description: Human-readable description.
        author: Author or organization.
        url: Repository URL.
        source_file: Relative path to the C source file in the repo.
        platform: Target platform for the compiled BOF.
        category: Functional category.
        required_args: List of required argument names.
        optional_args: List of optional argument names.
        mitre_technique: MITRE ATT&CK technique ID (e.g., 'T1018').
        sha256: SHA-256 hash of the canonical source file (empty until audited).
        min_beacon_version: Minimum beacon version required.
        dependencies: List of dependency BOF names.
    """

    name: str
    description: str
    author: str
    url: str
    source_file: str
    platform: BofPlatform = BofPlatform.WINDOWS
    category: BofCategory = BofCategory.GENERAL
    required_args: list[str] = field(default_factory=list)
    optional_args: list[str] = field(default_factory=list)
    mitre_technique: str = ""
    sha256: str = ""
    min_beacon_version: str = "1.0"
    dependencies: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "url": self.url,
            "source_file": self.source_file,
            "platform": self.platform.value,
            "category": self.category.value,
            "required_args": self.required_args,
            "optional_args": self.optional_args,
            "mitre_technique": self.mitre_technique,
            "sha256": self.sha256,
            "min_beacon_version": self.min_beacon_version,
            "dependencies": self.dependencies,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> BofEntry:
        """Build from a dictionary."""
        return cls(
            name=str(raw["name"]),
            description=str(raw.get("description", "")),
            author=str(raw.get("author", "Unknown")),
            url=str(raw.get("url", "")),
            source_file=str(raw.get("source_file", "")),
            platform=BofPlatform(raw.get("platform", "windows")),
            category=BofCategory(raw.get("category", "general")),
            required_args=list(raw.get("required_args", [])),
            optional_args=list(raw.get("optional_args", [])),
            mitre_technique=str(raw.get("mitre_technique", "")),
            sha256=str(raw.get("sha256", "")),
            min_beacon_version=str(raw.get("min_beacon_version", "1.0")),
            dependencies=list(raw.get("dependencies", [])),
        )


@dataclass
class BofCatalog:
    """Curated catalog of known Beacon Object Files.

    The catalog is a static index maintained by the LazyOwn team. Entries
    are added via ``register()`` and persisted to disk as JSON for sharing
    between operator sessions.
    """

    entries: dict[str, BofEntry] = field(default_factory=dict)

    def register(self, entry: BofEntry) -> None:
        """Register a BOF entry in the catalog."""
        self.entries[entry.name] = entry
        log.debug("Registered BOF '%s' in catalog", entry.name)

    def register_many(self, entries: list[BofEntry]) -> None:
        """Register multiple BOF entries at once."""
        for entry in entries:
            self.register(entry)

    def get(self, name: str) -> BofEntry:
        """Retrieve a BOF entry by name.

        Raises KeyError if not found.
        """
        if name not in self.entries:
            available = ", ".join(sorted(self.entries.keys())[:20])
            total = len(self.entries)
            raise KeyError(
                f"BOF '{name}' not found in catalog ({total} entries). "
                f"First 20: {available}"
            )
        return self.entries[name]

    def search(self, query: str) -> list[BofEntry]:
        """Search catalog by keyword across name, description, and technique.

        Args:
            query: Case-insensitive search keyword.

        Returns:
            List of matching BofEntry objects, sorted by relevance.
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return list(self.entries.values())
        results: list[tuple[int, BofEntry]] = []
        for entry in self.entries.values():
            score = 0
            if query_lower == entry.name.lower():
                score += 100
            elif query_lower in entry.name.lower():
                score += 50
            if query_lower in entry.description.lower():
                score += 30
            if query_lower == entry.mitre_technique.lower():
                score += 40
            if query_lower in entry.category.value.lower():
                score += 20
            for arg in entry.required_args + entry.optional_args:
                if query_lower in arg.lower():
                    score += 10
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results]

    def list_by_category(self, category: BofCategory) -> list[BofEntry]:
        """Return all BOFs in a specific category."""
        return [e for e in self.entries.values() if e.category == category]

    def list_by_platform(self, platform: BofPlatform) -> list[BofEntry]:
        """Return all BOFs for a specific platform."""
        return [e for e in self.entries.values() if e.platform == platform]

    def list_all(self) -> list[BofEntry]:
        """Return all catalog entries sorted by name."""
        return sorted(self.entries.values(), key=lambda e: e.name)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the entire catalog to a dictionary."""
        return {
            "entries": {name: entry.to_dict() for name, entry in self.entries.items()},
            "updated_at": datetime.now(UTC).isoformat(),
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> BofCatalog:
        """Build a catalog from a dictionary."""
        catalog = cls()
        for entry_raw in raw.get("entries", {}).values():
            catalog.register(BofEntry.from_dict(entry_raw))
        return catalog

    @classmethod
    def load(cls, path: str | Path) -> BofCatalog:
        """Load a catalog from a JSON file."""
        p = Path(path)
        if not p.exists():
            return cls()
        with p.open("r", encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    def save(self, path: str | Path) -> None:
        """Save the catalog to a JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2)


def _build_default_catalog() -> BofCatalog:
    """Build the default curated BOF catalog.

    This catalog includes well-known open-source BOFs compatible with
    the TrustedSec SA BOF API. Maintainers should add verified entries
    to this function.
    """
    catalog = BofCatalog()
    default_entries = [
        BofEntry(
            name="ldap_enum",
            description="Enumerate Active Directory via LDAP: users, groups, computers, OUs, GPOs, ACLs",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/ldap_enum/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["domain"],
            optional_args=["server", "username", "password"],
            mitre_technique="T1087",
        ),
        BofEntry(
            name="adcs_enum",
            description="Enumerate Active Directory Certificate Services: templates, enrollment rights, ESC vulnerabilities",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/adcs_enum/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["domain"],
            optional_args=["server"],
            mitre_technique="T1649",
        ),
        BofEntry(
            name="enum_filter",
            description="Enumerate LDAP search filters to extract high-value targets",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/enum_filter/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["domain", "filter"],
            optional_args=["server"],
            mitre_technique="T1087",
        ),
        BofEntry(
            name="whoami",
            description="Extended whoami: privileges, groups, tokens, session info, UAC flags",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/whoami/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.RECON,
            mitre_technique="T1033",
        ),
        BofEntry(
            name="sc_enum",
            description="Enumerate Windows services: name, display name, state, start type, binary path",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/sc_enum/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            mitre_technique="T1007",
        ),
        BofEntry(
            name="netuser",
            description="Query detailed local and domain user account information",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/netuser/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.RECON,
            required_args=["username"],
            optional_args=["domain"],
            mitre_technique="T1087",
        ),
        BofEntry(
            name="netview",
            description="Enumerate network resources: shares, sessions, connected clients, open files",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/netview/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            optional_args=["server"],
            mitre_technique="T1046",
        ),
        BofEntry(
            name="listdns",
            description="List DNS A records from a domain controller via LDAP",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/listdns/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            optional_args=["domain"],
            mitre_technique="T1590",
        ),
        BofEntry(
            name="reg_query",
            description="Query Windows registry keys and values remotely or locally",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/reg_query/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["key"],
            optional_args=["value", "server"],
            mitre_technique="T1012",
        ),
        BofEntry(
            name="schedtask_create",
            description="Create a scheduled task for persistence on Windows targets",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/schedtask_create/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.PERSIST,
            required_args=["taskname", "command"],
            optional_args=["server", "username", "password", "interval"],
            mitre_technique="T1053",
        ),
        BofEntry(
            name="schedtask_delete",
            description="Delete a scheduled task to clean up persistence artifacts",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/schedtask_delete/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.PERSIST,
            required_args=["taskname"],
            optional_args=["server"],
            mitre_technique="T1053",
        ),
        BofEntry(
            name="service_create",
            description="Create a Windows service for persistence or lateral movement",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/service_create/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.PERSIST,
            required_args=["servicename", "binarypath"],
            optional_args=["displayname", "server"],
            mitre_technique="T1543",
        ),
        BofEntry(
            name="spawn_job",
            description="Spawn a long-running job: keylogger, screenshot daemon, process monitor",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/spawn_job.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.EXEC,
            required_args=["jobtype"],
            optional_args=["interval_ms", "output_file"],
            mitre_technique="T1059",
        ),
        BofEntry(
            name="shell_hostname",
            description="Execute a command via cmd.exe and return captured output",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/shell_hostname/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.EXEC,
            required_args=["command"],
            mitre_technique="T1059",
        ),
        BofEntry(
            name="inject_apc",
            description="Inject shellcode into a remote process via Early Bird APC queuing",
            author="TrustedSec",
            url="https://github.com/trustedsec/CS-Situational-Awareness-BOF",
            source_file="SA/inject_apc/entry.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.EXEC,
            required_args=["pid", "shellcode_file"],
            optional_args=["spoofed_parent"],
            mitre_technique="T1055",
        ),
        BofEntry(
            name="netstat",
            description="Enumerate active TCP and UDP connections with owning process IDs",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/netstat.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.RECON,
            mitre_technique="T1049",
        ),
        BofEntry(
            name="portscan",
            description="Lightweight TCP connect port scan from within beacon process",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/portscan.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.ENUM,
            required_args=["target", "ports"],
            optional_args=["timeout_ms"],
            mitre_technique="T1046",
        ),
        BofEntry(
            name="lsass_dump",
            description="Dump LSASS process memory to disk for offline credential extraction",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/lsass_dump.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.CRED,
            optional_args=["output_path", "method"],
            mitre_technique="T1003",
        ),
        BofEntry(
            name="sam_dump",
            description="Dump SAM, SYSTEM, and SECURITY registry hives for offline cracking",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/sam_dump.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.CRED,
            optional_args=["output_dir"],
            mitre_technique="T1003",
        ),
        BofEntry(
            name="env_enum",
            description="Enumerate environment variables for recon and credential discovery",
            author="LazyOwn",
            url="https://github.com/anomalyco/LazyOwn",
            source_file="bofs/env_enum.c",
            platform=BofPlatform.WINDOWS,
            category=BofCategory.RECON,
            mitre_technique="T1082",
        ),
    ]
    catalog.register_many(default_entries)
    return catalog


class BofValidator:
    """Validates BOF integrity and compatibility.

    Checks SHA-256 hashes of downloaded source files against the
    catalog, verifies platform compatibility, and validates that
    required arguments are supplied.
    """

    @staticmethod
    def compute_sha256(filepath: str | Path) -> str:
        """Compute the SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def verify_entry(entry: BofEntry, filepath: str | Path) -> tuple[bool, str]:
        """Verify the SHA-256 of a downloaded BOF source matches the catalog.

        Returns (ok, reason). If entry.sha256 is empty, verification is
        skipped with an informational message.
        """
        if not entry.sha256:
            return True, f"no SHA-256 in catalog for '{entry.name}' (unaudited)"
        actual = BofValidator.compute_sha256(filepath)
        if actual != entry.sha256:
            return False, (
                f"SHA-256 mismatch for '{entry.name}': "
                f"expected {entry.sha256[:16]}..., got {actual[:16]}..."
            )
        return True, "hash verified"

    @staticmethod
    def validate_args(entry: BofEntry, args: dict[str, str]) -> list[str]:
        """Validate that all required arguments are supplied.

        Returns a list of missing argument names (empty = valid).
        """
        missing = []
        for arg in entry.required_args:
            if arg not in args or not args[arg]:
                missing.append(arg)
        return missing


class BofRegistry:
    """Manages BOF installations on disk with version tracking.

    Each installed BOF is tracked in a manifest JSON file with the
    installation timestamp, BOF version, and source URL.
    """

    def __init__(self, sessions_dir: str | Path) -> None:
        self._base = Path(sessions_dir) / BOF_INSTALL_DIR_NAME
        self._base.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self._base / BOF_MANIFEST_FILENAME

    @property
    def install_dir(self) -> Path:
        """Return the BOF installation directory."""
        return self._base

    def _load_manifest(self) -> dict[str, Any]:
        """Load the installation manifest from disk."""
        if not self._manifest_path.exists():
            return {}
        try:
            with self._manifest_path.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Failed to load BOF manifest: %s", exc)
            return {}

    def _save_manifest(self, manifest: dict[str, Any]) -> None:
        """Save the installation manifest to disk."""
        with self._manifest_path.open("w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, default=str)

    def is_installed(self, name: str) -> bool:
        """Return True if a BOF is installed."""
        manifest = self._load_manifest()
        return name in manifest

    def install(self, entry: BofEntry) -> Path:
        """Register a BOF as installed with current timestamp.

        Returns the install directory for this BOF.
        """
        install_subdir = self._base / entry.name
        install_subdir.mkdir(parents=True, exist_ok=True)
        manifest = self._load_manifest()
        manifest[entry.name] = {
            "name": entry.name,
            "version": entry.min_beacon_version,
            "url": entry.url,
            "platform": entry.platform.value,
            "installed_at": datetime.now(UTC).isoformat(),
            "sha256": entry.sha256,
            "category": entry.category.value,
        }
        self._save_manifest(manifest)
        log.info("Installed BOF '%s' at %s", entry.name, install_subdir)
        return install_subdir

    def uninstall(self, name: str, remove_files: bool = True) -> bool:
        """Unregister a BOF from the manifest and optionally remove its files.

        Returns True if the BOF was installed and successfully removed.
        """
        manifest = self._load_manifest()
        if name not in manifest:
            return False
        del manifest[name]
        self._save_manifest(manifest)
        if remove_files:
            install_subdir = self._base / name
            if install_subdir.exists():
                shutil.rmtree(install_subdir, ignore_errors=True)
        log.info("Uninstalled BOF '%s'", name)
        return True

    def list_installed(self) -> list[dict[str, Any]]:
        """Return a list of all installed BOFs with metadata."""
        manifest = self._load_manifest()
        return sorted(manifest.values(), key=lambda x: x.get("name", ""))

    def get_install_info(self, name: str) -> dict[str, Any] | None:
        """Return installation metadata for a BOF, or None if not installed."""
        manifest = self._load_manifest()
        return manifest.get(name)


class BofMarketplace:
    """BOF discovery, installation, and management interface.

    Composes a BofCatalog (curated index) and a BofRegistry (disk
    state) to provide search/install/uninstall/info operations.

    Attributes:
        catalog: The curated BOF catalog.
        registry: The disk-backed BOF registry.
        validator: The BOF hash/args validator.
    """

    def __init__(
        self,
        sessions_dir: str | Path = "sessions",
        catalog: BofCatalog | None = None,
    ) -> None:
        self._sessions_dir = Path(sessions_dir)
        self._catalog = catalog if catalog is not None else _build_default_catalog()
        self._registry = BofRegistry(self._sessions_dir)
        self._validator = BofValidator()

    @property
    def catalog(self) -> BofCatalog:
        """Return the catalog."""
        return self._catalog

    @property
    def registry(self) -> BofRegistry:
        """Return the registry."""
        return self._registry

    def search(self, query: str) -> list[dict[str, Any]]:
        """Search the catalog and return enriched results with install status.

        Args:
            query: Search keyword (name, description, technique, category).

        Returns:
            List of dicts with BOF metadata plus `installed` flag.
        """
        results = self._catalog.search(query)
        installed_names = {i.get("name") for i in self._registry.list_installed()}
        return [
            {
                **entry.to_dict(),
                "installed": entry.name in installed_names,
            }
            for entry in results
        ]

    def info(self, name: str) -> dict[str, Any]:
        """Get detailed information about a BOF by name.

        Includes catalog metadata plus install state.
        Returns a dict with 'error' key if not found.
        """
        try:
            entry = self._catalog.get(name)
        except KeyError:
            return {"error": f"BOF '{name}' not found in catalog"}
        install_info = self._registry.get_install_info(name)
        return {
            "catalog": entry.to_dict(),
            "installed": install_info is not None,
            "install_info": install_info or {},
        }

    def install(self, name: str) -> dict[str, Any]:
        """Install a BOF from the catalog by name.

        Registers the BOF in the disk manifest. Does NOT clone
        the source repository; the operator is expected to have
        the catalog repository already cloned, or use a separate
        install step for source retrieval.

        Returns a dict with status information.
        """
        try:
            entry = self._catalog.get(name)
        except KeyError:
            return {"error": f"BOF '{name}' not found", "name": name}
        if self._registry.is_installed(name):
            return {
                "status": "already_installed",
                "name": name,
                "install_path": str(self._registry.install_dir / name),
            }
        install_path = self._registry.install(entry)
        return {
            "status": "installed",
            "name": name,
            "install_path": str(install_path),
            "platform": entry.platform.value,
            "category": entry.category.value,
        }

    def uninstall(self, name: str) -> dict[str, Any]:
        """Uninstall a BOF by name.

        Returns a dict with uninstall status.
        """
        if not self._registry.is_installed(name):
            return {"error": f"BOF '{name}' is not installed", "name": name}
        removed = self._registry.uninstall(name)
        return {
            "status": "uninstalled" if removed else "failed",
            "name": name,
        }

    def list_installed(self) -> list[dict[str, Any]]:
        """List all installed BOFs with catalog enrichment."""
        installed = self._registry.list_installed()
        enriched = []
        for item in installed:
            try:
                entry = self._catalog.get(item["name"])
                enriched.append({**entry.to_dict(), **item})
            except KeyError:
                enriched.append(item)
        return enriched

    def list_missing_dependencies(self, name: str) -> list[str]:
        """Return a list of dependencies for a BOF that are not installed."""
        try:
            entry = self._catalog.get(name)
        except KeyError:
            return []
        return [
            dep for dep in entry.dependencies
            if not self._registry.is_installed(dep)
        ]

    def bulk_install(self, names: list[str]) -> dict[str, dict[str, Any]]:
        """Install multiple BOFs at once.

        Returns a dict mapping BOF name to result dict.
        """
        results: dict[str, dict[str, Any]] = {}
        for name in names:
            results[name] = self.install(name)
        return results


__all__ = [
    "BofMarketplace",
    "BofRegistry",
    "BofCatalog",
    "BofEntry",
    "BofValidator",
    "BofPlatform",
    "BofCategory",
    "_build_default_catalog",
]
