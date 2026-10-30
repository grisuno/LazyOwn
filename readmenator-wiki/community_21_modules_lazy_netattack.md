# modules: lazy_netattack

*Community 21 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `modules` with dominant language py (cohesion 1.00). Central symbols: `AttackVectorVerdict`, `SurfaceEvidence`, `TestIdentity`, `TestMitm6Downgrade`, `TestRelay`, `TestShape`, `_ad_hosts`, `_ad_in`. Core file: `tests/test_lazy_netattack.py` (17 symbols). Documented purpose: Windows network-attack surface adjudicator for mitm6/LLMNR/SMB relay.  Contract: pure decisions from observed evidence. The kinetic steps of this family (poison.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/lazy_netattack.py` | py | utility | 12 | yes |
| `tests/test_lazy_netattack.py` | py | testing | 17 | yes |

## Key Symbols

- `AttackVectorVerdict` (class, `modules/lazy_netattack.py:88`) `class AttackVectorVerdict` - One family decision with ready-made discovery commands.
- `as_dict` (method, `modules/lazy_netattack.py:107`) `def as_dict(self)` - Return one JSON-safe view.
- `SurfaceEvidence` (class, `modules/lazy_netattack.py:120`) `class SurfaceEvidence` - Evidence bags consumed by :func:`surface_decision`.
- `_svc_blob` (function, `modules/lazy_netattack.py:136`) `def _svc_blob(hosts, evidence)` - Concatenate the service names of the given hosts.
- `_windows_hosts` (function, `modules/lazy_netattack.py:146`) `def _windows_hosts(evidence)` - Return hosts whose OS hint or services identify Windows.
- `_ad_hosts` (function, `modules/lazy_netattack.py:161`) `def _ad_hosts(evidence)` - Return hosts that present actual directory-identity services.
- `_signing_not_required` (function, `modules/lazy_netattack.py:173`) `def _signing_not_required(host, evidence)` - Return True when the host has attested SMB signing disabled.
- `_downgrade_candidates` (function, `modules/lazy_netattack.py:179`) `def _downgrade_candidates(evidence, windows)` - Return Windows hosts with attested LM compatibility level <= 2.
- `surface_decision` (function, `modules/lazy_netattack.py:184`) `def surface_decision(evidence)` - Grade the Windows network-attack families from evidence bags.
- `_signing_required` (function, `modules/lazy_netattack.py:297`) `def _signing_required(host, evidence)` - Return True when the host attested signing required (relay blocked).
- `_ad_in` (function, `modules/lazy_netattack.py:303`) `def _ad_in(evidence, host)` - Return True when one host carries an AD-identity service.
- `hint_text` (function, `modules/lazy_netattack.py:311`) `def hint_text(verdict)` - Shape one loop hint line for a verdict.
- `module` (function, `tests/test_lazy_netattack.py:18`) `def module()`
- `windows_only` (function, `tests/test_lazy_netattack.py:25`) `def windows_only(module)`
- `ad_domain_controller` (function, `tests/test_lazy_netattack.py:35`) `def ad_domain_controller(module)`
- `TestIdentity` (class, `tests/test_lazy_netattack.py:50`) `class TestIdentity`
- `test_windows_hint_matches` (method, `tests/test_lazy_netattack.py:51`) `def test_windows_hint_matches(self, module, windows_only)`
- `test_linux_host_blocked` (method, `tests/test_lazy_netattack.py:56`) `def test_linux_host_blocked(self, module)`
- `TestRelay` (class, `tests/test_lazy_netattack.py:69`) `class TestRelay`
- `test_attested_signing_unlocks_relay` (method, `tests/test_lazy_netattack.py:70`) `def test_attested_signing_unlocks_relay(self, module, ad_domain_controller)`
- `test_unknown_signing_requires_evidence` (method, `tests/test_lazy_netattack.py:75`) `def test_unknown_signing_requires_evidence(self, module, windows_only)`
- `test_attested_signing_required_blocks` (method, `tests/test_lazy_netattack.py:79`) `def test_attested_signing_required_blocks(self, module, windows_only)`
- `TestMitm6Downgrade` (class, `tests/test_lazy_netattack.py:85`) `class TestMitm6Downgrade`
- `test_mitm6_needs_event_and_consent` (method, `tests/test_lazy_netattack.py:86`) `def test_mitm6_needs_event_and_consent(self, module, ad_domain_controller)`
- `test_downgrade_lm2_viable` (method, `tests/test_lazy_netattack.py:91`) `def test_downgrade_lm2_viable(self, module, ad_domain_controller)`
- `test_downgrade_lm5_needs_evidence` (method, `tests/test_lazy_netattack.py:95`) `def test_downgrade_lm5_needs_evidence(self, module, ad_domain_controller)`
- `TestShape` (class, `tests/test_lazy_netattack.py:101`) `class TestShape`
- `test_hint_text_shapes` (method, `tests/test_lazy_netattack.py:102`) `def test_hint_text_shapes(self, module, ad_domain_controller)`
- `test_verdicts_json_safe` (method, `tests/test_lazy_netattack.py:107`) `def test_verdicts_json_safe(self, module, ad_domain_controller)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: lazy_netattack changed?
- Should modules: lazy_netattack be split, given cohesion 1.00?

## Sources

- `modules/lazy_netattack.py`
- `tests/test_lazy_netattack.py`
