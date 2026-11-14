"""Adaptive fallback arbiter: prerequisites, one-shot memory, no lockouts.

Every scenario states Given, When, Then.
"""

from __future__ import annotations

from modules.failure_verdict import FailureClass, FailureVerdict
from modules.lazy_fallback import FALLBACK_GRAPH, AdaptiveFallbackArbiter


def _verdict(failure_class: FailureClass) -> FailureVerdict:
    """Build a verdict for one class using the shared action matrix."""
    from modules.failure_verdict import CLASS_ACTIONS

    return FailureVerdict(failure_class, CLASS_ACTIONS[failure_class], "test")


def test_kerberoast_failure_gets_ordered_alternatives():
    """Given a failed kerberoast attempt with SMB and Kerberos evidence,
    When suggested two times, Then alternatives come in graph order and
    never repeat."""
    arbiter = AdaptiveFallbackArbiter()
    verdict = _verdict(FailureClass.AUTH)
    services = frozenset({"microsoft-ds", "kerberos-sec"})
    first = arbiter.suggest(
        "python3 modules/atomic_exploit_bridge.py run --id ad_lab_kerberoast --rhost dc",
        verdict,
        services=services,
        has_credentials=False,
    )
    second = arbiter.suggest(
        "python3 modules/atomic_exploit_bridge.py run --id ad_lab_kerberoast --rhost dc",
        verdict,
        services=services,
        has_credentials=False,
    )
    assert first is not None and first.technique_id == "ad_lab_asreproast"
    assert second is not None and second.technique_id == "ad_lab_samr_enum"


def test_lockout_never_gets_an_alternative():
    """Given a lockout verdict, When the arbiter is asked, Then nothing
    is proposed and nothing is recorded: no spray past a lockout."""
    arbiter = AdaptiveFallbackArbiter()
    alternative = arbiter.suggest(
        "spray command",
        _verdict(FailureClass.LOCKOUT),
        services=frozenset({"microsoft-ds"}),
    )
    assert alternative is None


def test_service_gates_fail_closed_on_unknown_evidence():
    """Given unknown service evidence (None), When the first viable
    alternative needs SMB, Then it is not proposed."""
    arbiter = AdaptiveFallbackArbiter()
    alternative = arbiter.suggest(
        "secretsdump command",
        _verdict(FailureClass.PERMISSION),
        services=None,
    )
    assert alternative is None


def test_service_gates_skip_unserved_candidates():
    """Given SMB-only evidence, When secretsdump alternatives all need
    LDAP, Then nothing is proposed."""
    arbiter = AdaptiveFallbackArbiter()
    alternative = arbiter.suggest(
        "dcsync secretsdump attempt",
        _verdict(FailureClass.PERMISSION),
        services=frozenset({"microsoft-ds"}),
    )
    assert alternative is None


def test_credential_gates_fail_closed_when_unknown():
    """Given unknown credential evidence, When the only catalogue candidate
    needs credentials, Then it is skipped."""
    arbiter = AdaptiveFallbackArbiter((FALLBACK_GRAPH[0],))
    blocked = arbiter.suggest(
        "kerberoast command",
        _verdict(FailureClass.AUTH),
        services=frozenset({"microsoft-ds", "kerberos-sec"}),
        has_credentials=None,
        catalogue={"ad_lab_passspray"},
    )
    assert blocked is None


def test_unknown_catalogue_ids_never_propose():
    """Given a catalogue map without the candidate ids, When suggested,
    Then nothing is proposed (unknown technique, no fire)."""
    arbiter = AdaptiveFallbackArbiter()
    alternative = arbiter.suggest(
        "kerberoast command",
        _verdict(FailureClass.AUTH),
        services=frozenset({"microsoft-ds", "kerberos-sec"}),
        catalogue=set(),
    )
    assert alternative is None


def test_tool_missing_or_scope_verdicts_get_no_alternatives():
    """Given skip/abort verdicts, When suggested, Then nothing happens."""
    arbiter = AdaptiveFallbackArbiter()
    for failure_class in (FailureClass.TOOL_MISSING, FailureClass.SCOPE):
        alternative = arbiter.suggest("kerberoast command", _verdict(failure_class))
        assert alternative is None


def test_unmatched_command_gets_no_alternatives():
    """Given a command outside every family, When suggested, Then the
    arbiter stays silent: no keyword, no alternative."""
    arbiter = AdaptiveFallbackArbiter()
    alternative = arbiter.suggest(
        "nmap -sT dc01",
        _verdict(FailureClass.AUTH),
        services=frozenset({"microsoft-ds"}),
    )
    assert alternative is None


def test_graph_is_well_formed():
    """Given the curated graph, When read, Then every family declares at
    least one matching keyword and every alternative declares a reason."""
    for family in FALLBACK_GRAPH:
        assert family.match
        for alternative in family.alternatives:
            assert alternative.technique_id
            assert alternative.reason
