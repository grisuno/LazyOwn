"""Adaptive fallback alternatives for failed chain techniques.

When a chain step fails with a fallback-eligible verdict, the arbiter
proposes the next untried alternative from a curated graph over the
LazyOwn Atomic technique catalogue (``exploits/*.yaml``). A proposal is
only ever an option: the runner stays in control and the operator flag
arms the behaviour. Three invariants hold:

1. A lockout verdict never gets an alternative: spraying past a locked
   account is how engagements turn noisy and die loud.
2. Service prerequisites must be observable before an alternative is
   proposed: no SMB technique fires without SMB evidence.
3. One alternative per (failed family, technique) per arbiter lifetime:
   the arbiter never proposes the same attempt twice.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any

from modules.failure_verdict import FailureVerdict

_MAX_COMMAND_CHARS = 300


@dataclass(frozen=True)
class Alternative:
    """One fallback technique candidate.

    Args:
        technique_id: Atomic catalogue id (``exploits/<id>.yaml``).
        reason: One-line rationale shown to the operator.
        requires_services: Service-name tokens that must be observable
            on the target before the alternative is proposed.
        requires_credentials: True when captured credentials must exist.
    """

    technique_id: str
    reason: str
    requires_services: tuple[str, ...] = ()
    requires_credentials: bool = False


@dataclass(frozen=True)
class TechniqueFallback:
    """One failed-technique family with its ordered alternatives.

    Args:
        match: Lowercase keywords; any keyword found in the failed
            command line binds the failure to this family (first family
            declared wins).
        alternatives: Ordered candidates; the arbiter returns the first
            one not yet tried whose prerequisites hold.
    """

    match: tuple[str, ...]
    alternatives: tuple[Alternative, ...]

    def matches(self, command: str) -> bool:
        """Return True when the failed command line binds this family."""
        lowered = (command or "").lower()
        return any(keyword in lowered for keyword in self.match)


FALLBACK_GRAPH: tuple[TechniqueFallback, ...] = (
    TechniqueFallback(
        match=("kerberoast",),
        alternatives=(
            Alternative(
                "ad_lab_asreproast",
                "No crackable SPN hashes; harvest no-preauth accounts instead.",
                requires_services=("kerberos",),
            ),
            Alternative(
                "ad_lab_samr_enum",
                "No account list yet; enumerate users over a null session.",
                requires_services=("microsoft-ds",),
            ),
            Alternative(
                "ad_lab_passspray",
                "Reuse the user list for a policy-aware spray.",
                requires_services=("microsoft-ds",),
                requires_credentials=True,
            ),
        ),
    ),
    TechniqueFallback(
        match=("asreproast",),
        alternatives=(
            Alternative(
                "ad_lab_kerbrute_userenum",
                "No no-preauth accounts; enumerate valid usernames first.",
                requires_services=("kerberos",),
            ),
            Alternative(
                "ad_lab_passpol",
                "Read the password policy before any further spray.",
                requires_services=("microsoft-ds",),
            ),
        ),
    ),
    TechniqueFallback(
        match=("passspray", "password spray", "spray_"),
        alternatives=(
            Alternative(
                "ad_lab_passpol",
                "Spray rejected; check the effective password policy.",
                requires_services=("microsoft-ds",),
            ),
            Alternative(
                "ad_lab_kerbrute_userenum",
                "Spray rejected; refresh the valid user list.",
                requires_services=("kerberos",),
            ),
        ),
    ),
    TechniqueFallback(
        match=("dcsync", "secretsdump", "drsuapi"),
        alternatives=(
            Alternative(
                "ad_lab_delegation_enum",
                "No DCSync rights; hunt an ACL/delegation path instead.",
                requires_services=("ldap",),
            ),
            Alternative(
                "ad_lab_gmsa_enum",
                "No DCSync rights; harvest gMSA secrets instead.",
                requires_services=("ldap",),
            ),
        ),
    ),
    TechniqueFallback(
        match=("psexec", "smbexec", "wmiexec", "atexec", "impacket"),
        alternatives=(
            Alternative(
                "win_coercer_scan",
                "Execution denied; look for coercible delegation targets.",
                requires_services=("microsoft-ds",),
            ),
            Alternative(
                "samba_usermap",
                "Execution denied; probe the known service-map flaw.",
                requires_services=("microsoft-ds",),
            ),
            Alternative(
                "win_smb_signing_enum",
                "Execution denied; map signing posture for relaying.",
                requires_services=("microsoft-ds",),
            ),
        ),
    ),
    TechniqueFallback(
        match=("samr", "rid_cycling", "ldap_enum", "ldapsearch"),
        alternatives=(
            Alternative(
                "ad_lab_rid_cycling",
                "Enumeration denied; cycle RIDs over SMB instead.",
                requires_services=("microsoft-ds",),
            ),
            Alternative(
                "ad_lab_kerbrute_userenum",
                "Enumeration denied; confirm usernames over Kerberos.",
                requires_services=("kerberos",),
            ),
        ),
    ),
)


def _service_satisfied(required: str, services: frozenset[str] | None) -> bool:
    """Return True when the service prerequisite is observable.

    Args:
        required: Lowercase token the observed service name must contain.
        services: Observed lowercase service names; None means unknown,
            which fails closed so unevidenced techniques never fire.
    """
    if services is None:
        return False
    return any(required in observed for observed in services)


class AdaptiveFallbackArbiter:
    """Turn one failed step into at most one adaptive alternative.

    Thread-safe: reentrancy only records attempts and never blocks the
    caller, so a runner paying attention to outcome order still sees a
    consistent tried-set.
    """

    def __init__(self, graph: tuple[TechniqueFallback, ...] = FALLBACK_GRAPH) -> None:
        """Bind the fallback graph; the shared graph is the default.

        Args:
            graph: Ordered families; first-declared wins on overlap.
        """
        self._graph = graph
        self._lock = threading.Lock()
        self._tried: set[tuple[int, int]] = set()

    def suggest(
        self,
        command: str,
        verdict: FailureVerdict,
        services: frozenset[str] | None = None,
        has_credentials: bool | None = None,
        catalogue: Any | None = None,
    ) -> Alternative | None:
        """Return the first viable untried alternative for one failure.

        Args:
            command: Failed command line; bound to a family by keywords.
            verdict: Verdict from ``modules.failure_verdict`` gating
                whether alternatives are allowed at all.
            services: Observable lowercase service names; None fails all
                service-gated candidates closed.
            has_credentials: Whether captured credentials exist; None
                fails credential-gated candidates closed.
            catalogue: Mapping of technique ids the catalogue actually
                exposes (optional; unknown checks skip when absent).

        Returns:
            One :class:`Alternative` or None when no family matches, the
            verdict forbids alternatives, everything was already tried
            or no prerequisite holds. The candidate is recorded.
        """
        family_index = self._bind_family(command)
        if family_index is None:
            return None
        with self._lock:
            for position, candidate in enumerate(self._graph[family_index].alternatives):
                if (family_index, position) in self._tried:
                    continue
                if any(not _service_satisfied(required, services) for required in candidate.requires_services):
                    continue
                if candidate.requires_credentials and has_credentials is not True:
                    continue
                if catalogue is not None and candidate.technique_id not in catalogue:
                    continue
                self._tried.add((family_index, position))
                return candidate
        return None

    def _bind_family(self, command: str) -> int | None:
        """Return the family index the failed command belongs to."""
        lowered = (command or "").lower()[:_MAX_COMMAND_CHARS]
        with self._lock:
            for index, family in enumerate(self._graph):
                if family.matches(lowered):
                    return index
        return None


def catalogue_ids() -> frozenset[str] | None:
    """Return every Atomic technique id actually loadable right now.

    Returns:
        Lowercase-id-aware frozenset of catalogue ids, or None when the
        bridge is unavailable (PyYAML missing, unreadable directory) so
        candidates keep the benefit of the doubt.
    """
    try:
        from modules.atomic_exploit_bridge import load_all

        return frozenset(load_all())
    except Exception:
        return None


__all__ = [
    "AdaptiveFallbackArbiter",
    "Alternative",
    "FALLBACK_GRAPH",
    "TechniqueFallback",
    "catalogue_ids",
]
