# modules: lazy_triage

*Community 23 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `modules` with dominant language py (cohesion 1.00). Central symbols: `SignatureStore`, `__init__`, `_load`, `_save`, `apply_rules`, `fresh_signature`, `hard_evidence`, `rank`. Core file: `tests/test_lazy_triage.py` (11 symbols). Documented purpose: Triage doctrine: evidence floors, verdict algebra and signature dedup.  Deterministic pre-LLM classification of one finding so the model can never invent proof..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/lazy_triage.py` | py | utility | 10 | yes |
| `tests/test_lazy_triage.py` | py | testing | 11 | yes |

## Key Symbols

- `rank` (function, `modules/lazy_triage.py:42`) `def rank(verdict)` - Return the comparison rank of a triage verdict.
- `hard_evidence` (function, `modules/lazy_triage.py:47`) `def hard_evidence(kind, facts)` - Classify one finding from its deterministic evidence floor.
- `apply_rules` (function, `modules/lazy_triage.py:80`) `def apply_rules(verdict, kind, facts)` - Constrain a (model or operator) verdict by the evidence floor.
- `signature_for` (function, `modules/lazy_triage.py:108`) `def signature_for(kind, fields)` - Return the evidence signature of one classification request.
- `SignatureStore` (class, `modules/lazy_triage.py:135`) `class SignatureStore` - Bounded TTL store of already-answered evidence signatures.
- `__init__` (method, `modules/lazy_triage.py:138`) `def __init__(self, sessions_dir, ttl)` - Bind the store file under sessions/lazy.
- `fresh_signature` (method, `modules/lazy_triage.py:144`) `def fresh_signature(self, signature, now)` - Return the previous signature row when it is inside the TTL window.
- `reset` (method, `modules/lazy_triage.py:162`) `def reset(self)` - Drop every signature row.
- `_load` (method, `modules/lazy_triage.py:166`) `def _load(self)`
- `_save` (method, `modules/lazy_triage.py:176`) `def _save(self, store)`
- `test_floor_confirms_shell_and_exploit_success` (function, `tests/test_lazy_triage.py:27`) `def test_floor_confirms_shell_and_exploit_success()` - Given an exploit with shell, When the floor reads it, Then it confirms.
- `test_cve_match_without_version_is_unknown` (function, `tests/test_lazy_triage.py:35`) `def test_cve_match_without_version_is_unknown()` - Given a matched CVE with no version, When the floor reads it, Then it stays unknown.
- `test_apply_rules_never_drops_below_floor` (function, `tests/test_lazy_triage.py:41`) `def test_apply_rules_never_drops_below_floor()` - Given a dismissive verdict and hard evidence, When applied, Then the floor wins.
- `test_unbacked_confirmed_demotes_to_likely` (function, `tests/test_lazy_triage.py:47`) `def test_unbacked_confirmed_demotes_to_likely()` - Given model-confirmed with weak evidence, When applied, Then it demotes to likely.
- `test_backed_confirmed_stays` (function, `tests/test_lazy_triage.py:53`) `def test_backed_confirmed_stays()` - Given model-confirmed with hard evidence, When applied, Then it stays confirmed.
- `test_version_unknown_is_immovable` (function, `tests/test_lazy_triage.py:58`) `def test_version_unknown_is_immovable()` - Given model-unknown on any kind, When applied, Then it never moves.
- `test_signature_excludes_asset_fields` (function, `tests/test_lazy_triage.py:65`) `def test_signature_excludes_asset_fields()` - Given two different hosts, When signing, Then both share one signature.
- `test_signature_keeps_evidence_terms` (function, `tests/test_lazy_triage.py:72`) `def test_signature_keeps_evidence_terms()` - Given changed evidence, When signing, Then signatures diverge.
- `test_signature_respects_ttl` (function, `tests/test_lazy_triage.py:79`) `def test_signature_respects_ttl(tmp_path, monkeypatch)` - Given a fresh answer inside the window, When checked twice, Then only one reserve.
- `test_signature_store_persists` (function, `tests/test_lazy_triage.py:88`) `def test_signature_store_persists(tmp_path)` - Given a marked store, When reloaded, Then the reserve still reads.
- `test_replay_within_ttl` (function, `tests/test_lazy_triage.py:96`) `def test_replay_within_ttl(tmp_path)` - Given a second store instance reading the same file, When fresh, Then reuse happens.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 1
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in modules: lazy_triage changed?
- Should modules: lazy_triage be split, given cohesion 1.00?

## Sources

- `modules/lazy_triage.py`
- `tests/test_lazy_triage.py`
