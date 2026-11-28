"""
modules/lazyown_bridge.py
==========================
Full-coverage structured catalog of all LazyOwn do_ commands mapped to
attack phases, MITRE ATT&CK tactics, and discovered service types.

Integrates with the MCP auto_loop to provide phase-aware, service-matched
command selection without modifying lazyown.py.

Design (SOLID)
--------------
- Single Responsibility : CommandCatalog owns only the command registry;
                          PhaseSelector owns only phase-to-command resolution;
                          ServiceMatcher owns only service-type detection;
                          ContextEnricher owns only arg substitution.
- Open/Closed           : add new phases/tactics via CatalogEntry, no edits needed.
- Liskov                : all Selector subclasses honour Optional[CatalogEntry] contract.
- Interface Segregation : BridgeDispatcher exposes only what auto_loop needs.
- Dependency Inversion  : BridgeDispatcher depends on AbstractSelector abstraction.

Phases
------
recon       -> 01. Reconnaissance
enum        -> 02. Scanning & Enumeration
exploit     -> 03. Exploitation
postexp     -> 04. Post-Exploitation
persist     -> 05. Persistence
privesc     -> 06. Privilege Escalation
cred        -> 07. Credential Access
lateral     -> 08. Lateral Movement
exfil       -> 09. Data Exfiltration
c2          -> 10. Command & Control
report      -> 11. Reporting
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass
class CatalogEntry:
    """A single LazyOwn command with metadata for intelligent selection."""

    command: str
    phase: str
    mitre_tactic: str
    services: list[str] = field(default_factory=list)
    requires_creds: bool = False
    requires_port: bool = False
    description: str = ""
    priority: int = 5
    arg_template: str = ""
    os_target: str = "any"  # "linux", "windows", "any"
    tags: list[str] = field(default_factory=list)  # e.g. ["ad", "kerberos", "web"]

    def build_command(
        self,
        target: str = "",
        port: str = "",
        user: str = "",
        password: str = "",
        domain: str = "",
        url: str = "",
        wordlist: str = "",
        lhost: str = "",
        lport: str = "",
    ) -> str:
        """Return 'command [args]' with known values substituted."""
        args = self.arg_template
        subs = {
            "{target}": target,
            "{port}": port,
            "{user}": user,
            "{password}": password,
            "{domain}": domain,
            "{url}": url or (f"http://{target}" if target else ""),
            "{wordlist}": wordlist or "/usr/share/wordlists/rockyou.txt",
            "{lhost}": lhost,
            "{lport}": lport or "4444",
        }
        for placeholder, value in subs.items():
            if value:
                args = args.replace(placeholder, value)
        args = re.sub(r"\{[^}]+\}", "", args).strip()
        return f"{self.command} {args}".strip() if args else self.command

    def matches_service(self, services: list[str]) -> bool:
        if not self.services:
            return True
        for svc in services:
            svc_lower = svc.lower()
            for required in self.services:
                if required.lower() in svc_lower or svc_lower in required.lower():
                    return True
        return False

    def matches_os(self, os_hint: str) -> bool:
        if self.os_target == "any":
            return True
        return self.os_target.lower() == os_hint.lower()


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------


class CommandCatalog:
    """Full registry of CatalogEntry objects for all LazyOwn phases."""

    def __init__(self) -> None:
        self._entries: list[CatalogEntry] = []
        self._populate()

    def _populate(self) -> None:
        """Load the curated catalogue rows from the declarative data file.

        The rows live in ``modules/data/command_catalog.yaml`` so the
        catalogue stays reviewable and diffable without touching the
        selector machinery. Every row carries the full metadata contract
        (phase, MITRE tactic, services, requirements, priority, argument
        template, OS hint and tags) that the selectors consume.

        Raises:
            FileNotFoundError: When the catalogue data file is missing.
            ValueError: When a row fails validation.
        """
        import yaml

        catalog_path = Path(__file__).resolve().parent / "data" / "command_catalog.yaml"
        document = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
        for row in document.get("entries", []):
            self._entries.append(
                CatalogEntry(
                    command=row["command"],
                    phase=row["phase"],
                    mitre_tactic=row["mitre_tactic"],
                    services=list(row.get("services", [])),
                    requires_creds=bool(row.get("requires_creds", False)),
                    requires_port=bool(row.get("requires_port", False)),
                    description=str(row.get("description", "")),
                    priority=int(row.get("priority", 5)),
                    arg_template=str(row.get("arg_template", "")),
                    os_target=str(row.get("os_target", "any")),
                    tags=list(row.get("tags", [])),
                )
            )

    def by_phase(self, phase: str) -> list[CatalogEntry]:
        return sorted(
            [e for e in self._entries if e.phase == phase],
            key=lambda e: e.priority,
        )

    def by_mitre(self, technique_id: str) -> list[CatalogEntry]:
        tid = technique_id.upper()
        return [e for e in self._entries if tid in e.mitre_tactic.upper()]

    def by_service(self, service_name: str) -> list[CatalogEntry]:
        svc = service_name.lower()
        return [e for e in self._entries if any(s.lower() in svc or svc in s.lower() for s in e.services)]

    def by_tag(self, tag: str) -> list[CatalogEntry]:
        return [e for e in self._entries if tag.lower() in e.tags]

    def by_os(self, os_hint: str) -> list[CatalogEntry]:
        return [e for e in self._entries if e.matches_os(os_hint)]

    def all_phases(self) -> set[str]:
        return {e.phase for e in self._entries}

    def get(self, command: str) -> CatalogEntry | None:
        for e in self._entries:
            if e.command == command:
                return e
        return None

    def count(self) -> int:
        return len(self._entries)


# ---------------------------------------------------------------------------
# Abstract selector
# ---------------------------------------------------------------------------


class AbstractSelector(ABC):
    @abstractmethod
    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: list[str],
        has_creds: bool,
        excluded: set[str],
        os_hint: str = "any",
    ) -> CatalogEntry | None: ...


# ---------------------------------------------------------------------------
# Concrete selectors
# ---------------------------------------------------------------------------


class ServiceAwareSelector(AbstractSelector):
    """Priority + service matching selector with credential gate."""

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: list[str],
        has_creds: bool,
        excluded: set[str],
        os_hint: str = "any",
    ) -> CatalogEntry | None:
        candidates = catalog.by_phase(phase)
        # Pass 1: strict match — service + os + creds
        for entry in candidates:
            if entry.command in excluded:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if os_hint and os_hint != "any" and not entry.matches_os(os_hint):
                continue
            if services and not entry.matches_service(services):
                continue
            return entry
        # Pass 2: relax service filter
        for entry in candidates:
            if entry.command in excluded:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if os_hint and os_hint != "any" and not entry.matches_os(os_hint):
                continue
            return entry
        # Pass 3: relax everything except excluded
        for entry in candidates:
            if entry.command not in excluded:
                return entry
        return None


class MitreAlignedSelector(AbstractSelector):
    """Prefer MITRE-matching commands; fall back to ServiceAwareSelector."""

    def __init__(self, technique_id: str) -> None:
        self._tid = technique_id
        self._fallback = ServiceAwareSelector()

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: list[str],
        has_creds: bool,
        excluded: set[str],
        os_hint: str = "any",
    ) -> CatalogEntry | None:
        for entry in catalog.by_mitre(self._tid):
            if entry.command in excluded:
                continue
            if entry.phase != phase:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if services and not entry.matches_service(services):
                continue
            return entry
        return self._fallback.select(catalog, phase, services, has_creds, excluded, os_hint)


class TagSelector(AbstractSelector):
    """Select commands by tag (e.g. 'kerberos', 'web', 'impacket')."""

    def __init__(self, tag: str) -> None:
        self._tag = tag
        self._fallback = ServiceAwareSelector()

    def select(
        self,
        catalog: CommandCatalog,
        phase: str,
        services: list[str],
        has_creds: bool,
        excluded: set[str],
        os_hint: str = "any",
    ) -> CatalogEntry | None:
        candidates = [
            e
            for e in catalog.by_tag(self._tag)
            if e.phase == phase and e.command not in excluded and not (e.requires_creds and not has_creds)
        ]
        candidates.sort(key=lambda e: e.priority)
        if candidates:
            return candidates[0]
        return self._fallback.select(catalog, phase, services, has_creds, excluded, os_hint)


# ---------------------------------------------------------------------------
# Context enricher
# ---------------------------------------------------------------------------


class ContextEnricher:
    """Builds final command strings from CatalogEntry + WorldModel facts."""

    def enrich(
        self,
        entry: CatalogEntry,
        target: str,
        world_snapshot: dict | None = None,
    ) -> str:
        snapshot = world_snapshot or {}
        hosts = snapshot.get("hosts", {})
        host_info = hosts.get(target, {})
        services_dict = host_info.get("services", {})
        creds_list = snapshot.get("credentials", [])

        user, password = "", ""
        if creds_list:
            first = creds_list[0] if isinstance(creds_list[0], dict) else {}
            user = first.get("username", "")
            password = first.get("password", "")

        port = ""
        for port_str, svc_info in services_dict.items():
            if not isinstance(svc_info, dict):
                continue
            svc_name = svc_info.get("name", "").lower()
            if entry.matches_service([svc_name]):
                port = port_str
                break

        domain = snapshot.get("domain", "")
        lhost = snapshot.get("lhost", "")
        lport = snapshot.get("lport", "4444")

        return entry.build_command(
            target=target,
            port=port,
            user=user,
            password=password,
            domain=domain,
            lhost=lhost,
            lport=str(lport) if lport else "4444",
        )


# ---------------------------------------------------------------------------
# Phase mapper
# ---------------------------------------------------------------------------


class PhaseMapper:
    """Maps WorldModel EngagementPhase values to bridge phase strings.

    Delegates core engagement-to-CLI mapping to :class:`modules.killchain.KillChain`
    as the single source of truth for canonical phases. The bridge maintains its
    own extended namespace (postexp, cred, persist, c2) for tool categorization
    that extends beyond the canonical 8-phase kill chain.
    """

    _NATIVE: set[str] = {
        "recon",
        "enum",
        "exploit",
        "postexp",
        "cred",
        "lateral",
        "privesc",
        "persist",
        "exfil",
        "c2",
        "report",
    }

    # Bridge-specific mapping that extends the canonical KillChain phases.
    # Where KillChain maps ``post_exploitation`` to ``privesc``, the bridge
    # keeps ``postexp`` as a distinct tool-categorisation phase.
    _MAP: dict[str, str] = {
        "recon": "recon",
        "scanning": "recon",
        "enumeration": "enum",
        "exploitation": "exploit",
        "post_exploitation": "postexp",
        "lateral_movement": "lateral",
        "exfiltration": "exfil",
        "reporting": "report",
        "persistence": "persist",
        "privilege_escalation": "privesc",
        "credential_access": "cred",
        "command_and_control": "c2",
        "completed": "report",
        "unknown": "recon",
        "intrusion": "exploit",
        "credential": "cred",
        "privesc": "privesc",
        "lateral": "lateral",
        "exfil": "exfil",
        "c2": "c2",
        "report": "report",
    }

    @staticmethod
    def canonical_kill_chain_order() -> list[str]:
        """Return the canonical 8-phase order from KillChain (single source of truth)."""
        from modules.killchain import KillChain

        return list(KillChain.phases())

    def to_bridge_phase(self, wm_phase: str) -> str:
        lower = wm_phase.lower()
        if lower in self._NATIVE:
            return lower
        if lower in self._MAP:
            return self._MAP[lower]
        from modules.killchain import KillChain

        canonical = KillChain.engagement_phase_to_cli(lower)
        if canonical != "recon":
            return canonical
        return "recon"

    def kill_chain_order(self) -> list[str]:
        """Ordered list of bridge phases following the kill chain."""
        return ["recon", "enum", "exploit", "postexp", "cred", "lateral", "privesc", "persist", "exfil", "c2", "report"]


# ---------------------------------------------------------------------------
# Bridge dispatcher
# ---------------------------------------------------------------------------


class BridgeDispatcher:
    """
    Public facade used by the MCP auto_loop and MCP tool handlers.
    Combines catalog + selector + enricher into a single suggest() call.
    """

    def __init__(
        self,
        catalog: CommandCatalog | None = None,
        selector: AbstractSelector | None = None,
        enricher: ContextEnricher | None = None,
        phase_mapper: PhaseMapper | None = None,
    ) -> None:
        self._catalog = catalog or CommandCatalog()
        self._selector = selector or ServiceAwareSelector()
        self._enricher = enricher or ContextEnricher()
        self._phase_mapper = phase_mapper or PhaseMapper()

    def suggest(
        self,
        phase: str,
        target: str = "",
        services: list[str] | None = None,
        has_creds: bool = False,
        excluded: set[str] | None = None,
        world_snapshot: dict | None = None,
        mitre_hint: str = "",
        tag_hint: str = "",
        os_hint: str = "any",
    ) -> tuple[str, CatalogEntry] | None:
        """
        Return (command_string, entry) or None.

        Parameters
        ----------
        phase       : WorldModel or bridge phase string (auto-translated)
        target      : IP/hostname for arg substitution
        services    : discovered service strings ["http:80", "smb:445", ...]
        has_creds   : credentials known in WorldModel
        excluded    : command names to skip
        world_snapshot : WorldModel.snapshot() dict
        mitre_hint  : prefer commands matching this MITRE technique
        tag_hint    : prefer commands with this tag (e.g. "kerberos")
        os_hint     : "linux", "windows", or "any"
        """
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        svc_list = services or []
        excl = excluded or set()

        if mitre_hint:
            selector: AbstractSelector = MitreAlignedSelector(mitre_hint)
        elif tag_hint:
            selector = TagSelector(tag_hint)
        else:
            selector = self._selector

        entry = selector.select(self._catalog, bridge_phase, svc_list, has_creds, excl, os_hint)
        if entry is None:
            return None

        cmd = self._enricher.enrich(entry, target, world_snapshot)
        return cmd, entry

    def suggest_sequence(
        self,
        phase: str,
        target: str = "",
        services: list[str] | None = None,
        has_creds: bool = False,
        excluded: set[str] | None = None,
        world_snapshot: dict | None = None,
        limit: int = 5,
    ) -> list[tuple[str, CatalogEntry]]:
        """Return up to `limit` non-excluded suggestions for the phase."""
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        candidates = self._catalog.by_phase(bridge_phase)
        svc_list = services or []
        excl = excluded or set()
        results: list[tuple[str, CatalogEntry]] = []
        for entry in candidates:
            if len(results) >= limit:
                break
            if entry.command in excl:
                continue
            if entry.requires_creds and not has_creds:
                continue
            if svc_list and not entry.matches_service(svc_list):
                continue
            cmd = self._enricher.enrich(entry, target, world_snapshot)
            results.append((cmd, entry))
        return results

    def suggest_for_wm_phase(
        self,
        wm_phase_value: str,
        target: str = "",
        services: list[str] | None = None,
        has_creds: bool = False,
        excluded: set[str] | None = None,
        world_snapshot: dict | None = None,
    ) -> tuple[str, CatalogEntry] | None:
        return self.suggest(
            phase=wm_phase_value,
            target=target,
            services=services,
            has_creds=has_creds,
            excluded=excluded,
            world_snapshot=world_snapshot,
        )

    def list_phase(self, phase: str) -> list[CatalogEntry]:
        bridge_phase = self._phase_mapper.to_bridge_phase(phase)
        return self._catalog.by_phase(bridge_phase)

    def all_phases(self) -> set[str]:
        return self._catalog.all_phases()

    def catalog_summary(self) -> dict[str, list[str]]:
        summary: dict[str, list[str]] = {}
        for phase in self._phase_mapper.kill_chain_order():
            entries = self._catalog.by_phase(phase)
            if entries:
                summary[phase] = [e.command for e in entries]
        return summary

    def catalog_summary_filtered(
        self,
        phase: str | None = None,
        os_hint: str = "any",
    ) -> dict[str, list[str]]:
        """Return a kill-chain summary restricted to a phase and target OS.

        Args:
            phase: Optional WorldModel-or-bridge phase identifier. When
                provided the summary contains only that phase (translated
                through :class:`PhaseMapper`). When ``None`` every phase
                in the kill-chain order is included.
            os_hint: Target OS filter (``"any"``, ``"linux"``, ``"windows"``).
                Entries are kept when :meth:`CatalogEntry.matches_os`
                returns ``True``. The value ``"any"`` disables the filter.

        Returns:
            Mapping of phase identifier to the ordered list of command
            names that survived the filters. Empty phases are omitted so
            agents do not waste tokens on blank sections.
        """
        normalized_os = (os_hint or "any").strip().lower() or "any"
        if phase:
            bridge_phase = self._phase_mapper.to_bridge_phase(phase)
            phases: list[str] = [bridge_phase]
        else:
            phases = list(self._phase_mapper.kill_chain_order())

        summary: dict[str, list[str]] = {}
        for current_phase in phases:
            entries = self._catalog.by_phase(current_phase)
            if normalized_os != "any":
                entries = [e for e in entries if e.matches_os(normalized_os)]
            if entries:
                summary[current_phase] = [e.command for e in entries]
        return summary

    def catalog_count(self) -> int:
        return self._catalog.count()

    def phase_kill_chain(self) -> list[str]:
        return self._phase_mapper.kill_chain_order()


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_dispatcher: BridgeDispatcher | None = None


def get_dispatcher() -> BridgeDispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = BridgeDispatcher()
    return _dispatcher
