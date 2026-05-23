"""Exploration engine: trigger and OS aware addon/tool matching.

This module is the single source of truth for two new operator-facing
features:

1. Filtering ``lazyaddons/*.yaml`` and ``tools/*.tool`` entries by the
   nmap services discovered in ``sessions/scan_*.nmap.xml`` and the
   victim platform recorded in ``payload.json`` (``os_id`` / ``platform``).
2. Computing an exploration coverage report consumed by the ``explore``
   shell command, ``suggest_next``, and ``recommend_next``.

Design (SOLID):

- ``ExplorationConfig`` centralises every magic value (default paths,
  glob patterns, MITRE platform whitelist, OS aliases).
- ``DiscoveredService``, ``AddonEntry``, ``ToolEntry`` are immutable
  value objects.
- ``NmapXmlReader`` is the only piece that touches XML.
- ``AddonCatalog`` and ``ToolCatalog`` each have one reason to change
  (their respective on-disk schema).
- ``TriggerMatcher`` is a pure ranking primitive.
- ``ExplorationEngine`` composes the pieces above and exposes the small
  public surface used by the CLI, MCP layer, and tests.

The module has zero coupling to ``cmd2``, ``flask``, ``rich`` or
``lazyown.py`` and every public method returns plain Python types so it
can be reused inside the shell, the MCP server, or the Textual TUI
without modification.
"""

from __future__ import annotations

import csv
import glob
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import defusedxml.ElementTree as ET
import yaml

MITRE_PLATFORMS: frozenset[str] = frozenset(
    {
        "linux",
        "windows",
        "macos",
        "network",
        "containers",
        "saas",
        "iaas",
    }
)

ANY_OS: str = "any"
ALLOWED_OS_VALUES: frozenset[str] = MITRE_PLATFORMS | {ANY_OS}

OS_ID_TO_PLATFORM: Mapping[int, str] = {
    1: "linux",
    2: "windows",
    3: "macos",
}

TRIGGER_WILDCARD: str = "all"


@dataclass(frozen=True)
class ExplorationConfig:
    """Centralised constants for the exploration engine.

    Every path, glob, default value and whitelist lives here so the
    engine is fully data-driven and trivially testable.
    """

    sessions_dir: str = "sessions"
    lazyaddons_dir: str = "lazyaddons"
    tools_dir: str = "tools"
    nmap_xml_glob: str = "scan_*.nmap.xml"
    history_csv: str = "LazyOwn_session_report.csv"
    history_command_columns: tuple[str, ...] = ("tool", "command", "name")
    default_os: str = ANY_OS
    default_trigger: tuple[str, ...] = ()
    coverage_decimals: int = 1


@dataclass(frozen=True)
class DiscoveredService:
    """A single open port discovered by nmap on a host."""

    host: str
    port: int
    proto: str
    service: str
    product: str = ""
    version: str = ""

    @property
    def label(self) -> str:
        """Return a compact human-readable label such as ``smb:445/tcp``."""

        return f"{self.service or 'unknown'}:{self.port}/{self.proto}"


@dataclass(frozen=True)
class AddonEntry:
    """A parsed lazyaddon YAML file with trigger/OS metadata."""

    name: str
    description: str
    category: str
    addon_os: str
    trigger: tuple[str, ...]
    repo_url: str
    enabled: bool
    source_path: str


@dataclass(frozen=True)
class ToolEntry:
    """A parsed ``.tool`` file from the ``tools/`` directory."""

    name: str
    description: str
    category: str
    tool_os: str
    trigger: tuple[str, ...]
    active: bool
    source_path: str


@dataclass(frozen=True)
class CoverageReport:
    """Aggregate exploration metrics for the active engagement."""

    services_total: int
    services_with_run_command: int
    addons_total: int
    addons_enabled: int
    addons_executed: int
    tools_total: int
    tools_executed: int
    history_commands: int

    @property
    def service_coverage(self) -> float:
        """Fraction of discovered services with at least one run command."""

        if self.services_total <= 0:
            return 0.0
        return self.services_with_run_command / self.services_total

    @property
    def addon_coverage(self) -> float:
        """Fraction of enabled addons that have been executed at least once."""

        if self.addons_enabled <= 0:
            return 0.0
        return self.addons_executed / self.addons_enabled

    @property
    def tool_coverage(self) -> float:
        """Fraction of active tools that have been executed at least once."""

        if self.tools_total <= 0:
            return 0.0
        return self.tools_executed / self.tools_total


class NmapXmlReader:
    """Read discovered services from nmap XML files in ``sessions/``.

    Falls back to the stdlib XML parser to avoid coupling to ``libnmap``
    which is only an optional runtime dependency in tests.
    """

    def __init__(self, config: ExplorationConfig | None = None) -> None:
        """Store the configuration used to locate the nmap XML directory."""

        self.config = config or ExplorationConfig()

    def discover(self, target: str | None = None) -> list[DiscoveredService]:
        """Return every open service across every nmap XML in sessions.

        Args:
            target: Optional rhost filter. When provided, only files that
                contain the target in their filename are read.
        Returns:
            A flat list of :class:`DiscoveredService` instances.
        """

        services: list[DiscoveredService] = []
        for xml_path in self._iter_xml_paths(target):
            services.extend(self._parse_one(xml_path))
        return services

    def _iter_xml_paths(self, target: str | None) -> Iterable[Path]:
        """Yield matching nmap XML paths, optionally filtered by target."""

        sessions = Path(self.config.sessions_dir)
        if not sessions.is_dir():
            return []
        pattern = self.config.nmap_xml_glob
        for path_str in sorted(glob.glob(str(sessions / pattern))):
            path = Path(path_str)
            if target and target not in path.name:
                continue
            yield path

    @staticmethod
    def _parse_one(xml_path: Path) -> list[DiscoveredService]:
        """Parse a single nmap XML file. Tolerates malformed input."""

        results: list[DiscoveredService] = []
        try:
            tree = ET.parse(str(xml_path))
        except (ET.ParseError, OSError, ET.EntitiesForbidden, ET.ExternalReferenceForbidden):
            return results
        root = tree.getroot()
        for host_el in root.findall("host"):
            address_el = host_el.find("address")
            if address_el is None:
                continue
            host = address_el.get("addr", "").strip()
            if not host:
                continue
            for port_el in host_el.findall("./ports/port"):
                state_el = port_el.find("state")
                if state_el is None or state_el.get("state") != "open":
                    continue
                try:
                    port_int = int(port_el.get("portid", "0"))
                except ValueError:
                    continue
                proto = port_el.get("protocol", "tcp")
                service_el = port_el.find("service")
                service_name = service_el.get("name", "") if service_el is not None else ""
                product = service_el.get("product", "") if service_el is not None else ""
                version = service_el.get("version", "") if service_el is not None else ""
                results.append(
                    DiscoveredService(
                        host=host,
                        port=port_int,
                        proto=proto,
                        service=service_name,
                        product=product,
                        version=version,
                    )
                )
        return results


class AddonCatalog:
    """Load every ``lazyaddons/*.yaml`` exposing ``os`` and ``trigger``.

    Missing fields default to ``os: any`` and ``trigger: []`` so existing
    addons continue to load without modification. Parsed entries are
    cached per-process by ``(path, mtime)`` so repeated ``load()`` calls
    inside long-lived sessions (CLI shell, MCP server) re-parse only the
    YAML files that actually changed on disk.
    """

    _entry_cache: dict[str, tuple[float, AddonEntry]] = {}

    def __init__(self, config: ExplorationConfig | None = None) -> None:
        """Store the configuration used to locate the addons directory."""

        self.config = config or ExplorationConfig()

    def load(self) -> list[AddonEntry]:
        """Return every parseable addon as an :class:`AddonEntry`."""

        addons_dir = Path(self.config.lazyaddons_dir)
        if not addons_dir.is_dir():
            return []
        entries: list[AddonEntry] = []
        for path_str in sorted(glob.glob(str(addons_dir / "*.yaml"))):
            entry = self._load_with_cache(Path(path_str))
            if entry is not None:
                entries.append(entry)
        return entries

    def _load_with_cache(self, path: Path) -> AddonEntry | None:
        """Return the cached entry when the file mtime is unchanged."""

        try:
            mtime = path.stat().st_mtime
        except OSError:
            return None
        key = str(path.resolve())
        cached = AddonCatalog._entry_cache.get(key)
        if cached is not None and cached[0] == mtime:
            return cached[1]
        entry = self._parse_one(path)
        if entry is not None:
            AddonCatalog._entry_cache[key] = (mtime, entry)
        return entry

    @classmethod
    def clear_cache(cls) -> None:
        """Drop the per-process addon cache (mainly used by tests)."""

        cls._entry_cache.clear()

    def _parse_one(self, path: Path) -> AddonEntry | None:
        """Parse a single addon file. Returns ``None`` on parse failure."""

        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            return None
        if not isinstance(data, dict):
            return None
        name = str(data.get("name") or path.stem).strip()
        description = str(data.get("description") or "").strip()
        category = str(data.get("category") or "14. Yaml Addon.").strip()
        addon_os = normalise_os(data.get("os"), default=self.config.default_os)
        trigger = normalise_trigger(data.get("trigger"))
        tool_block = data.get("tool") or {}
        repo_url = str(tool_block.get("repo_url") or "").strip()
        enabled = bool(data.get("enabled", False))
        return AddonEntry(
            name=name,
            description=description,
            category=category,
            addon_os=addon_os,
            trigger=trigger,
            repo_url=repo_url,
            enabled=enabled,
            source_path=str(path),
        )


class ToolCatalog:
    """Load every ``tools/*.tool`` exposing ``os`` and ``trigger``.

    The ``.tool`` schema already carries a ``trigger`` list; this catalog
    adds OS awareness with a ``any`` default so the legacy files keep
    working. Parsed entries are cached per-process by ``(path, mtime)``
    so repeated ``load()`` calls only re-parse changed files.
    """

    _entry_cache: dict[str, tuple[float, ToolEntry]] = {}

    def __init__(self, config: ExplorationConfig | None = None) -> None:
        """Store the configuration used to locate the tools directory."""

        self.config = config or ExplorationConfig()

    def load(self) -> list[ToolEntry]:
        """Return every parseable ``.tool`` file as a :class:`ToolEntry`."""

        tools_dir = Path(self.config.tools_dir)
        if not tools_dir.is_dir():
            return []
        entries: list[ToolEntry] = []
        for path_str in sorted(glob.glob(str(tools_dir / "*.tool"))):
            entry = self._load_with_cache(Path(path_str))
            if entry is not None:
                entries.append(entry)
        return entries

    def _load_with_cache(self, path: Path) -> ToolEntry | None:
        """Return the cached entry when the file mtime is unchanged."""

        try:
            mtime = path.stat().st_mtime
        except OSError:
            return None
        key = str(path.resolve())
        cached = ToolCatalog._entry_cache.get(key)
        if cached is not None and cached[0] == mtime:
            return cached[1]
        entry = self._parse_one(path)
        if entry is not None:
            ToolCatalog._entry_cache[key] = (mtime, entry)
        return entry

    @classmethod
    def clear_cache(cls) -> None:
        """Drop the per-process tool cache (mainly used by tests)."""

        cls._entry_cache.clear()

    def _parse_one(self, path: Path) -> ToolEntry | None:
        """Parse a single tool file. Returns ``None`` on parse failure."""

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        if not isinstance(data, dict):
            return None
        name = str(data.get("toolname") or path.stem).strip()
        description = str(data.get("description") or "").strip()
        category = str(data.get("category") or "").strip()
        tool_os = normalise_os(data.get("os"), default=self.config.default_os)
        trigger = normalise_trigger(data.get("trigger"))
        active = bool(data.get("active", False))
        return ToolEntry(
            name=name,
            description=description,
            category=category,
            tool_os=tool_os,
            trigger=trigger,
            active=active,
            source_path=str(path),
        )


class TriggerMatcher:
    """Match addons and tools against discovered services + current OS."""

    def __init__(self, current_os: str = ANY_OS) -> None:
        """Store the platform used to filter incompatible entries."""

        self.current_os = normalise_os(current_os, default=ANY_OS)

    def addons_for_service(
        self,
        service: DiscoveredService,
        addons: Sequence[AddonEntry],
    ) -> list[AddonEntry]:
        """Return addons whose trigger and OS match the given service."""

        matches: list[AddonEntry] = []
        for addon in addons:
            if not addon.enabled:
                continue
            if not self._os_compatible(addon.addon_os):
                continue
            if self._trigger_matches(addon.trigger, service.service):
                matches.append(addon)
        return matches

    def tools_for_service(
        self,
        service: DiscoveredService,
        tools: Sequence[ToolEntry],
    ) -> list[ToolEntry]:
        """Return active tools whose trigger and OS match the service."""

        matches: list[ToolEntry] = []
        for tool in tools:
            if not tool.active:
                continue
            if not self._os_compatible(tool.tool_os):
                continue
            if self._trigger_matches(tool.trigger, service.service):
                matches.append(tool)
        return matches

    def _os_compatible(self, candidate_os: str) -> bool:
        """Return True when ``candidate_os`` is ``any`` or equals current OS."""

        if candidate_os == ANY_OS or self.current_os == ANY_OS:
            return True
        return candidate_os == self.current_os

    @staticmethod
    def _trigger_matches(trigger: Sequence[str], service_name: str) -> bool:
        """Return True when ``service_name`` is listed in trigger or wildcard."""

        if not trigger:
            return False
        if TRIGGER_WILDCARD in trigger:
            return True
        return service_name in trigger


class HistoryReader:
    """Read previously executed commands from the session CSV transcript."""

    def __init__(self, config: ExplorationConfig | None = None) -> None:
        """Store the configuration used to locate the transcript file."""

        self.config = config or ExplorationConfig()

    def executed_commands(self) -> set[str]:
        """Return the set of unique tool/command names already run."""

        csv_path = Path(self.config.sessions_dir) / self.config.history_csv
        if not csv_path.is_file():
            return set()
        seen: set[str] = set()
        try:
            with csv_path.open(newline="", encoding="utf-8", errors="ignore") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    for col in self.config.history_command_columns:
                        raw = (row.get(col) or "").strip()
                        if not raw:
                            continue
                        head = raw.split()[0]
                        seen.add(head)
                        seen.add(head.removeprefix("do_"))
                        seen.add(f"do_{head}")
        except OSError:
            return seen
        return seen


class ExplorationEngine:
    """Compose nmap + addons + tools + history into a coverage view.

    This is the entry point used by ``do_explore``, ``do_suggest_next``
    and ``do_recommend_next``. It does no I/O on its own — every read is
    delegated to a single-responsibility collaborator.
    """

    def __init__(
        self,
        config: ExplorationConfig | None = None,
        current_os: str = ANY_OS,
    ) -> None:
        """Wire collaborators together using the supplied configuration."""

        self.config = config or ExplorationConfig()
        self.current_os = normalise_os(current_os, default=ANY_OS)
        self.nmap_reader = NmapXmlReader(self.config)
        self.addon_catalog = AddonCatalog(self.config)
        self.tool_catalog = ToolCatalog(self.config)
        self.history_reader = HistoryReader(self.config)
        self.matcher = TriggerMatcher(self.current_os)

    def services(self, target: str | None = None) -> list[DiscoveredService]:
        """Return the discovered services for the engagement."""

        return self.nmap_reader.discover(target)

    def addons(self) -> list[AddonEntry]:
        """Return the parsed lazyaddon catalogue."""

        return self.addon_catalog.load()

    def tools(self) -> list[ToolEntry]:
        """Return the parsed ``.tool`` catalogue."""

        return self.tool_catalog.load()

    def history(self) -> set[str]:
        """Return the set of already-executed command names."""

        return self.history_reader.executed_commands()

    def suggestions_for_target(
        self,
        target: str | None = None,
    ) -> dict[str, dict[str, list[AddonEntry | ToolEntry]]]:
        """Group matching addons and tools by service for a target.

        Returns:
            Mapping ``service.label -> {"addons": [...], "tools": [...]}``
            covering every open port in the latest scan for the target.
        """

        addons = self.addons()
        tools = self.tools()
        grouped: dict[str, dict[str, list[AddonEntry | ToolEntry]]] = {}
        for service in self.services(target):
            grouped.setdefault(
                service.label,
                {"addons": [], "tools": []},
            )
            grouped[service.label]["addons"] = list(self.matcher.addons_for_service(service, addons))
            grouped[service.label]["tools"] = list(self.matcher.tools_for_service(service, tools))
        return grouped

    def unexplored_addons(
        self,
        target: str | None = None,
    ) -> list[AddonEntry]:
        """Return addons triggered by the scan that have never been run."""

        history = self.history()
        seen_addons: set[str] = set()
        unexplored: list[AddonEntry] = []
        for groups in self.suggestions_for_target(target).values():
            for addon in groups["addons"]:
                if not isinstance(addon, AddonEntry):
                    continue
                if addon.name in seen_addons:
                    continue
                seen_addons.add(addon.name)
                if addon.name in history:
                    continue
                unexplored.append(addon)
        return unexplored

    def unexplored_tools(
        self,
        target: str | None = None,
    ) -> list[ToolEntry]:
        """Return tools triggered by the scan that have never been run."""

        history = self.history()
        seen_tools: set[str] = set()
        unexplored: list[ToolEntry] = []
        for groups in self.suggestions_for_target(target).values():
            for tool in groups["tools"]:
                if not isinstance(tool, ToolEntry):
                    continue
                if tool.name in seen_tools:
                    continue
                seen_tools.add(tool.name)
                if tool.name in history:
                    continue
                unexplored.append(tool)
        return unexplored

    def coverage(self, target: str | None = None) -> CoverageReport:
        """Return an aggregate :class:`CoverageReport` for the engagement."""

        services = self.services(target)
        history = self.history()
        addons = self.addons()
        tools = self.tools()

        services_with_command = 0
        addon_executed_names: set[str] = set()
        tool_executed_names: set[str] = set()

        for service in services:
            matching_addons = self.matcher.addons_for_service(service, addons)
            matching_tools = self.matcher.tools_for_service(service, tools)
            any_run = False
            for addon in matching_addons:
                if addon.name in history:
                    addon_executed_names.add(addon.name)
                    any_run = True
            for tool in matching_tools:
                if tool.name in history:
                    tool_executed_names.add(tool.name)
                    any_run = True
            if any_run:
                services_with_command += 1

        for addon in addons:
            if addon.name in history:
                addon_executed_names.add(addon.name)
        for tool in tools:
            if tool.name in history:
                tool_executed_names.add(tool.name)

        return CoverageReport(
            services_total=len(services),
            services_with_run_command=services_with_command,
            addons_total=len(addons),
            addons_enabled=sum(1 for a in addons if a.enabled),
            addons_executed=len(addon_executed_names),
            tools_total=sum(1 for t in tools if t.active),
            tools_executed=len(tool_executed_names),
            history_commands=len(history),
        )


def resolve_current_os(payload: Mapping[str, object] | None) -> str:
    """Resolve the current victim platform from a payload-like mapping.

    The lookup honours both the explicit ``platform`` key (new) and the
    legacy numeric ``os_id`` so existing payload.json files keep working.
    Unknown or missing values fall back to :data:`ANY_OS`.
    """

    if not payload:
        return ANY_OS
    explicit = payload.get("platform")
    if isinstance(explicit, str) and explicit.strip().lower() in ALLOWED_OS_VALUES:
        return explicit.strip().lower()
    legacy = payload.get("os_id")
    try:
        legacy_int = int(legacy) if legacy is not None else 0
    except (TypeError, ValueError):
        legacy_int = 0
    return OS_ID_TO_PLATFORM.get(legacy_int, ANY_OS)


def normalise_os(value: object, default: str) -> str:
    """Coerce arbitrary YAML/JSON values to a whitelisted OS string."""

    if not isinstance(value, str):
        return default
    candidate = value.strip().lower()
    if not candidate:
        return default
    if candidate in ALLOWED_OS_VALUES:
        return candidate
    return default


def normalise_trigger(value: object) -> tuple[str, ...]:
    """Coerce arbitrary YAML/JSON values to a tuple of trigger strings."""

    if isinstance(value, str):
        item = value.strip().lower()
        return (item,) if item else ()
    if not isinstance(value, (list, tuple)):
        return ()
    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str):
            continue
        token = item.strip().lower()
        if token:
            cleaned.append(token)
    return tuple(cleaned)


__all__ = [
    "ALLOWED_OS_VALUES",
    "ANY_OS",
    "AddonCatalog",
    "AddonEntry",
    "CoverageReport",
    "DiscoveredService",
    "ExplorationConfig",
    "ExplorationEngine",
    "HistoryReader",
    "MITRE_PLATFORMS",
    "NmapXmlReader",
    "OS_ID_TO_PLATFORM",
    "ToolCatalog",
    "normalise_os",
    "normalise_trigger",
    "ToolEntry",
    "TRIGGER_WILDCARD",
    "TriggerMatcher",
    "resolve_current_os",
]
