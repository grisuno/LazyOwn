# tests

*Community 9 | 4 files | cohesion 0.75*

## Definition

This community groups 4 file(s) rooted at `tests` with dominant language py (cohesion 0.75). Central symbols: `CorsConfigError`, `CorsPolicy`, `TestFlaskSocketIOIntegration`, `TestIsAllowed`, `TestOriginsForSocketIO`, `TestResolveOrigins`, `__init__`, `_clean`. Core file: `tests/test_cors_policy.py` (17 symbols). Documented purpose: CORS origin allowlist policy for the LazyOwn C2 web layer.  Contract: this module owns the single source of truth for which origins the C2 web layer and its Soc.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/cors.py` | py | utility | 15 | yes |
| `tests/test_cors_behavior.py` | py | testing | 4 | yes |
| `tests/test_cors_policy.py` | py | testing | 17 | yes |
| `tests/test_cors_socketio_regression.py` | py | testing | 8 | yes |

## Key Symbols

- `CorsConfigError` (class, `lazyc2/security/cors.py:46`) `class CorsConfigError(ValueError)` - Raised when the CORS configuration is invalid for the current env.
- `CorsPolicy` (class, `lazyc2/security/cors.py:50`) `class CorsPolicy` - Immutable CORS allowlist derived from the LazyOwn runtime config.
- `__init__` (method, `lazyc2/security/cors.py:70`) `def __init__(self, env, lhost, allowed_origins, c2_port, extra_socketio_ports)`
- `env` (method, `lazyc2/security/cors.py:85`) `def env(self)` - Return the normalized environment tag (``"PROD"`` or ``"DEV"``).
- `resolve_origins` (method, `lazyc2/security/cors.py:89`) `def resolve_origins(self)` - Return the validated allowlist of origins for the current env.
- `origins_for_socketio` (method, `lazyc2/security/cors.py:110`) `def origins_for_socketio(self)` - Return the allowlist to feed ``flask_socketio.SocketIO``.
- `is_allowed` (method, `lazyc2/security/cors.py:136`) `def is_allowed(self, origin)` - Return ``True`` if ``origin`` matches any allowed entry.
- `_socketio_ports` (method, `lazyc2/security/cors.py:157`) `def _socketio_ports(self)`
- `_collect_candidates` (method, `lazyc2/security/cors.py:166`) `def _collect_candidates(self)`
- `_clean` (method, `lazyc2/security/cors.py:175`) `def _clean(candidates)`
- `_dev_fallback_origins` (method, `lazyc2/security/cors.py:185`) `def _dev_fallback_origins(self)`
- `_dev_fallback` (method, `lazyc2/security/cors.py:195`) `def _dev_fallback(self)`
- `_origin_matches` (method, `lazyc2/security/cors.py:199`) `def _origin_matches(allowed, candidate)` - Return ``True`` if ``candidate`` matches ``allowed`` ignoring port.
- `_scheme_of` (method, `lazyc2/security/cors.py:223`) `def _scheme_of(origin)`
- `_host_of` (method, `lazyc2/security/cors.py:230`) `def _host_of(origin)`
- `test_given_wildcard_in_prod_when_resolving_then_raises` (function, `tests/test_cors_behavior.py:16`) `def test_given_wildcard_in_prod_when_resolving_then_raises()` - Given a PROD env with a wildcard, when origins are resolved, then raise.
- `test_given_empty_in_dev_when_resolving_then_falls_back_to_lhost` (function, `tests/test_cors_behavior.py:23`) `def test_given_empty_in_dev_when_resolving_then_falls_back_to_lhost()` - Given DEV env with empty allowlist, when resolved, then http+https://lhost are used.
- `test_given_unknown_origin_when_handshake_then_denied` (function, `tests/test_cors_behavior.py:31`) `def test_given_unknown_origin_when_handshake_then_denied()` - Given an origin not in the allowlist, when checked, then it is denied.
- `test_given_matching_origin_when_handshake_then_allowed` (function, `tests/test_cors_behavior.py:41`) `def test_given_matching_origin_when_handshake_then_allowed()` - Given an origin in the allowlist, when checked, then it is allowed.
- `TestResolveOrigins` (class, `tests/test_cors_policy.py:24`) `class TestResolveOrigins` - Verify origin allowlist derivation from configuration.
- `test_wildcard_is_rejected` (method, `tests/test_cors_policy.py:27`) `def test_wildcard_is_rejected(self)`
- `test_wildcard_in_csv_is_dropped` (method, `tests/test_cors_policy.py:31`) `def test_wildcard_in_csv_is_dropped(self)`
- `test_prod_empty_allowlist_raises` (method, `tests/test_cors_policy.py:42`) `def test_prod_empty_allowlist_raises(self)`
- `test_dev_empty_allowlist_falls_back_to_lhost` (method, `tests/test_cors_policy.py:46`) `def test_dev_empty_allowlist_falls_back_to_lhost(self)`
- `test_csv_is_split_and_trimmed` (method, `tests/test_cors_policy.py:52`) `def test_csv_is_split_and_trimmed(self)`
- `test_list_input_is_preserved` (method, `tests/test_cors_policy.py:61`) `def test_list_input_is_preserved(self)`
- `test_empty_entries_in_csv_are_skipped` (method, `tests/test_cors_policy.py:69`) `def test_empty_entries_in_csv_are_skipped(self)`
- `TestIsAllowed` (class, `tests/test_cors_policy.py:78`) `class TestIsAllowed` - Verify the runtime origin check.
- `test_exact_match_is_allowed` (method, `tests/test_cors_policy.py:81`) `def test_exact_match_is_allowed(self)`
- `test_non_matching_origin_is_denied` (method, `tests/test_cors_policy.py:85`) `def test_non_matching_origin_is_denied(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 3
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 4 <-> 9 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports lazyc2/security/cors.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.75?

## Sources

- `lazyc2/security/cors.py`
- `tests/test_cors_behavior.py`
- `tests/test_cors_policy.py`
- `tests/test_cors_socketio_regression.py`
