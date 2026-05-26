"""Command chain registry: explicit prerequisites and dynamic next steps.

The chain answers two questions for both the human operator and the AI:

1. ``prev(cmd)`` — what should have run **before** ``cmd`` so it makes sense.
   These are static prerequisites declared once and shared by CLI and MCP.
2. ``next(cmd, params, target)`` — what to run **after** ``cmd``. Combines a
   static kill-chain map (deterministic, fast) with a dynamic resolver that
   consults the latest nmap services and the exploration engine so the
   recommendation reflects the actual attack surface.

Design (SOLID):

- ``ChainConfig`` centralises every magic value (history filename, default
  fan-out, service-to-followup table).
- ``PrerequisiteRegistry`` owns the static prev map (one reason to change).
- ``StaticNextRegistry`` reuses ``cli.reactive_hints._KILL_CHAIN_NEXT`` so the
  static next-hop table stays single-source.
- ``ServiceNextResolver`` is a pure ranking primitive over discovered
  services.
- ``DynamicNextResolver`` composes static + service + exploration-engine
  signals into an ordered, de-duplicated suggestion list with provenance.
- ``CommandChain`` is the facade consumed by CLI (``do_prev`` / ``do_next``),
  MCP (``lazyown_command_prev`` / ``lazyown_command_next``), and any future
  TUI widget.

Zero coupling to ``cmd2``, ``flask``, ``rich`` or ``lazyown.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from cli.exploration import (
    ANY_OS,
    DiscoveredService,
    ExplorationConfig,
    ExplorationEngine,
    resolve_current_os,
)
from cli.reactive_hints import _KILL_CHAIN_NEXT, _PHASE_PRIORITY

SOURCE_STATIC: str = "static"
SOURCE_SERVICE: str = "service"
SOURCE_ADDON: str = "addon"
SOURCE_TOOL: str = "tool"
SOURCE_PHASE: str = "phase"

_DEFAULT_PREREQUISITES: Mapping[str, tuple[str, ...]] = {
    "ping": (),
    "arpscan": (),
    "hosts_discovery": (),
    "lazynmap": ("ping",),
    "rustscan": ("ping",),
    "nmap": ("ping",),
    "gobuster": ("lazynmap",),
    "ffuf": ("lazynmap",),
    "feroxbuster": ("lazynmap",),
    "nikto": ("lazynmap",),
    "whatweb": ("lazynmap",),
    "wfuzz": ("lazynmap",),
    "sqlmap": ("lazynmap", "gobuster"),
    "enum4linux": ("lazynmap",),
    "smbclient": ("lazynmap",),
    "crackmapexec": ("enum4linux",),
    "secretsdump": ("crackmapexec",),
    "kerbrute": ("lazynmap",),
    "GetNPUsers": ("kerbrute",),
    "GetUserSPNs": ("kerbrute",),
    "searchsploit": ("lazynmap",),
    "responder": (),
    "hashcat": ("responder",),
    "john": ("responder",),
    "linpeas": ("ssh",),
    "pspy64": ("ssh",),
    "find_suid": ("ssh",),
    "sudo_privesc": ("ssh",),
    "winpeas": ("evil-winrm",),
    "evil-winrm": ("secretsdump",),
    "psexec": ("secretsdump",),
    "mimikatz": ("evil-winrm",),
    "snmpwalk": ("lazynmap",),
    "dnsenum": ("lazynmap",),
    "ldapsearch": ("lazynmap",),
    "xfreerdp": ("lazynmap",),
}

_DEFAULT_SERVICE_FOLLOWUPS: Mapping[str, tuple[str, ...]] = {
    "http": ("gobuster", "ffuf", "nikto", "whatweb", "feroxbuster"),
    "https": ("gobuster", "ffuf", "nikto", "whatweb", "feroxbuster"),
    "http-proxy": ("gobuster", "ffuf"),
    "ssh": ("ssh",),
    "ftp": ("ftp",),
    "smb": ("enum4linux", "crackmapexec", "smbclient"),
    "netbios-ssn": ("enum4linux", "crackmapexec", "smbclient"),
    "microsoft-ds": ("enum4linux", "crackmapexec", "smbclient"),
    "mysql": ("sqlmap",),
    "ms-sql-s": ("sqlmap", "crackmapexec"),
    "postgresql": ("sqlmap",),
    "mongod": ("nosqlmap",),
    "dns": ("dnsenum",),
    "domain": ("dnsenum",),
    "ldap": ("kerbrute", "GetNPUsers", "ldapsearch"),
    "ldaps": ("kerbrute", "GetNPUsers", "ldapsearch"),
    "kerberos-sec": ("kerbrute", "GetNPUsers"),
    "rdp": ("xfreerdp",),
    "ms-wbt-server": ("xfreerdp",),
    "snmp": ("snmpwalk", "onesixtyone"),
    "vnc": ("vncviewer",),
    "telnet": ("telnet",),
    "smtp": ("smtp-user-enum",),
    "pop3": ("hydra",),
    "imap": ("hydra",),
}


@dataclass(frozen=True)
class ChainConfig:
    """Centralised constants for the command chain module."""

    default_limit: int = 5
    prerequisites: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(_DEFAULT_PREREQUISITES)
    )
    service_followups: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: dict(_DEFAULT_SERVICE_FOLLOWUPS)
    )


@dataclass(frozen=True)
class NextStep:
    """A single recommended next command, with provenance for the operator."""

    name: str
    source: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-friendly representation of the step."""

        return {"name": self.name, "source": self.source, "reason": self.reason}


def _normalise(name: str) -> str:
    """Strip an optional ``do_`` prefix and lowercase the verb."""

    if not name:
        return ""
    head = name.split()[0].strip()
    if head.startswith("do_"):
        head = head[3:]
    return head


class PrerequisiteRegistry:
    """Static prev-map registry. One reason to change: the prerequisite table."""

    def __init__(self, config: ChainConfig | None = None) -> None:
        """Store the configuration that owns the prerequisite table."""

        self.config = config or ChainConfig()

    def prerequisites(self, cmd: str) -> list[str]:
        """Return the ordered list of prerequisite commands for ``cmd``."""

        key = _normalise(cmd)
        return list(self.config.prerequisites.get(key, ()))

    def missing(self, cmd: str, history: Sequence[str]) -> list[str]:
        """Return prerequisites that have **not** yet appeared in ``history``."""

        seen = {_normalise(h) for h in history if h}
        return [p for p in self.prerequisites(cmd) if _normalise(p) not in seen]


class StaticNextRegistry:
    """Wrapper over the legacy ``_KILL_CHAIN_NEXT`` map (shared source)."""

    def next_for(self, cmd: str) -> list[str]:
        """Return the deterministic kill-chain successors of ``cmd``."""

        key = _normalise(cmd)
        return list(_KILL_CHAIN_NEXT.get(key, ()))

    def phase_priority(self, phase: str) -> list[str]:
        """Return the phase-priority verbs used as a fallback."""

        key = (phase or "recon").strip().lower()
        return list(_PHASE_PRIORITY.get(key, _PHASE_PRIORITY.get("recon", ())))


class ServiceNextResolver:
    """Map nmap-discovered services to follow-up verbs."""

    def __init__(self, config: ChainConfig | None = None) -> None:
        """Store the configuration providing the service follow-up table."""

        self.config = config or ChainConfig()

    def followups(self, services: Sequence[DiscoveredService]) -> list[tuple[str, str]]:
        """Return ``(verb, reason)`` pairs for every triggered follow-up."""

        out: list[tuple[str, str]] = []
        seen: set[str] = set()
        for svc in services:
            verbs = self.config.service_followups.get((svc.service or "").lower())
            if not verbs:
                continue
            for verb in verbs:
                if verb in seen:
                    continue
                seen.add(verb)
                reason = f"open {svc.service} on {svc.host}:{svc.port}/{svc.proto}"
                out.append((verb, reason))
        return out


class DynamicNextResolver:
    """Compose static, service, and exploration signals into an ordered list."""

    def __init__(
        self,
        config: ChainConfig | None = None,
        static_registry: StaticNextRegistry | None = None,
        service_resolver: ServiceNextResolver | None = None,
        exploration_engine: ExplorationEngine | None = None,
    ) -> None:
        """Wire collaborators together. All arguments are injectable for tests."""

        self.config = config or ChainConfig()
        self.static_registry = static_registry or StaticNextRegistry()
        self.service_resolver = service_resolver or ServiceNextResolver(self.config)
        self.exploration_engine = exploration_engine

    def resolve(
        self,
        cmd: str,
        params: Mapping[str, object] | None = None,
        target: str | None = None,
        phase: str = "",
        limit: int | None = None,
    ) -> list[NextStep]:
        """Return the ordered, de-duplicated next-step recommendations.

        Args:
            cmd: The command that just ran. Pass an empty string when the
                caller wants suggestions for the current engagement instead
                of a specific predecessor.
            params: Live payload mapping (used to resolve victim OS for
                addon/tool filtering). Optional.
            target: Optional rhost filter for nmap XML lookups.
            phase: Current engagement phase identifier. Used only when the
                static and dynamic resolvers return nothing.
            limit: Maximum number of steps to return. Defaults to
                ``ChainConfig.default_limit``.

        Returns:
            Ordered list of :class:`NextStep`. Empty when no signal exists.
        """

        bound = limit if isinstance(limit, int) and limit > 0 else self.config.default_limit
        verb = _normalise(cmd)
        engine = self._ensure_engine(params)
        history = engine.history() if engine else set()

        steps: list[NextStep] = []
        seen: set[str] = set()

        for static_next in self.static_registry.next_for(verb):
            self._append(steps, seen, static_next, SOURCE_STATIC, f"after {verb}", history)
            if len(steps) >= bound:
                return steps

        if engine is not None:
            services = engine.services(target)
            for next_verb, reason in self.service_resolver.followups(services):
                self._append(steps, seen, next_verb, SOURCE_SERVICE, reason, history)
                if len(steps) >= bound:
                    return steps

            for addon in engine.unexplored_addons(target):
                reason = f"addon triggered by scan (os={addon.addon_os})"
                self._append(steps, seen, addon.name, SOURCE_ADDON, reason, history)
                if len(steps) >= bound:
                    return steps

            for tool in engine.unexplored_tools(target):
                reason = f"tool triggered by scan (os={tool.tool_os})"
                self._append(steps, seen, tool.name, SOURCE_TOOL, reason, history)
                if len(steps) >= bound:
                    return steps

        if not steps:
            for verb_p in self.static_registry.phase_priority(phase):
                self._append(steps, seen, verb_p, SOURCE_PHASE, f"phase {phase or 'recon'}", history)
                if len(steps) >= bound:
                    break

        return steps

    def _ensure_engine(
        self, params: Mapping[str, object] | None
    ) -> ExplorationEngine | None:
        if self.exploration_engine is not None:
            return self.exploration_engine
        try:
            current_os = resolve_current_os(params) if params else ANY_OS
            return ExplorationEngine(
                config=ExplorationConfig(), current_os=current_os
            )
        except Exception:
            return None

    @staticmethod
    def _append(
        steps: list[NextStep],
        seen: set[str],
        name: str,
        source: str,
        reason: str,
        history: set[str],
    ) -> None:
        verb = _normalise(name)
        if not verb or verb in seen:
            return
        if verb in history:
            return
        seen.add(verb)
        steps.append(NextStep(name=verb, source=source, reason=reason))


class CommandChain:
    """Facade exposing prev + next to CLI, MCP, and future TUI widgets."""

    def __init__(
        self,
        config: ChainConfig | None = None,
        prerequisites: PrerequisiteRegistry | None = None,
        next_resolver: DynamicNextResolver | None = None,
    ) -> None:
        """Wire collaborators together using the supplied configuration."""

        self.config = config or ChainConfig()
        self.prerequisites = prerequisites or PrerequisiteRegistry(self.config)
        self.next_resolver = next_resolver or DynamicNextResolver(self.config)

    def prev(self, cmd: str) -> list[str]:
        """Return the ordered prerequisite commands for ``cmd``."""

        return self.prerequisites.prerequisites(cmd)

    def missing_prerequisites(self, cmd: str, history: Sequence[str]) -> list[str]:
        """Return prerequisites of ``cmd`` not present in ``history``."""

        return self.prerequisites.missing(cmd, history)

    def next(
        self,
        cmd: str,
        params: Mapping[str, object] | None = None,
        target: str | None = None,
        phase: str = "",
        limit: int | None = None,
    ) -> list[NextStep]:
        """Return ordered next-step recommendations. See :meth:`DynamicNextResolver.resolve`."""

        return self.next_resolver.resolve(
            cmd=cmd, params=params, target=target, phase=phase, limit=limit
        )

    def chain(
        self,
        cmd: str,
        params: Mapping[str, object] | None = None,
        target: str | None = None,
        phase: str = "",
        limit: int | None = None,
    ) -> dict[str, object]:
        """Return a serialisable ``{prev, next}`` view for the given command."""

        next_steps = self.next(
            cmd=cmd, params=params, target=target, phase=phase, limit=limit
        )
        return {
            "command": _normalise(cmd),
            "prev": self.prev(cmd),
            "next": [step.to_dict() for step in next_steps],
        }


__all__ = [
    "ChainConfig",
    "CommandChain",
    "DynamicNextResolver",
    "NextStep",
    "PrerequisiteRegistry",
    "ServiceNextResolver",
    "SOURCE_ADDON",
    "SOURCE_PHASE",
    "SOURCE_SERVICE",
    "SOURCE_STATIC",
    "SOURCE_TOOL",
    "StaticNextRegistry",
]
