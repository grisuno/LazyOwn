# skills/hermes-lazyown

*Community 20 | 7 files | cohesion 0.85*

## Definition

This community groups 7 file(s) rooted at `skills/hermes-lazyown` with dominant language py (cohesion 0.85). Central symbols: `CheckpointSerializer`, `CompactionResult`, `CompactionStrategy`, `ConfigBridge`, `ConfigBridgeError`, `ConfigKeys`, `DefaultCompaction`, `Defaults`. Core file: `skills/hermes-lazyown/mcp_server.py` (28 symbols). Documented purpose: Dynamic Claude.md rule generator for the Hermes-LazyOwn integration.  Produces instruction snippets that Hermes injects into the system prompt based on the curr.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |
| `skills/hermes-lazyown/config_bridge.py` | py | infrastructure | 16 | yes |
| `skills/hermes-lazyown/constants.py` | py | utility | 15 | yes |
| `skills/hermes-lazyown/executor.py` | py | utility | 13 | yes |
| `skills/hermes-lazyown/hermes_sync.py` | py | utility | 14 | yes |
| `skills/hermes-lazyown/mcp_server.py` | py | utility | 28 | yes |
| `skills/hermes-lazyown/output_compactor.py` | py | utility | 20 | yes |

## Key Symbols

- `RuleSetBuilder` (class, `skills/hermes-lazyown/claudemd_rules.py:15`) `class RuleSetBuilder` - Builds a dynamic rule set string suitable for Hermes system prompt injection.
- `__init__` (method, `skills/hermes-lazyown/claudemd_rules.py:25`) `def __init__(self)`
- `with_phase` (method, `skills/hermes-lazyown/claudemd_rules.py:32`) `def with_phase(self, phase)` - Set the current engagement phase.
- `with_target` (method, `skills/hermes-lazyown/claudemd_rules.py:37`) `def with_target(self, rhost)` - Set the active target IP.
- `with_services` (method, `skills/hermes-lazyown/claudemd_rules.py:42`) `def with_services(self, services)` - Set discovered services (e.g., ['http:80', 'smb:445']).
- `with_creds` (method, `skills/hermes-lazyown/claudemd_rules.py:47`) `def with_creds(self, found)` - Set whether credentials have been discovered.
- `with_hermes` (method, `skills/hermes-lazyown/claudemd_rules.py:52`) `def with_hermes(self, is_hermes)` - Set whether running inside a Hermes session.
- `build` (method, `skills/hermes-lazyown/claudemd_rules.py:57`) `def build(self)` - Build and return the complete rule set markdown.
- `_base_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:71`) `def _base_rules(self)`
- `_phase_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:83`) `def _phase_rules(self)`
- `_service_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:127`) `def _service_rules(self)`
- `_credential_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:146`) `def _credential_rules(self)`
- `_hermes_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:159`) `def _hermes_rules(self)`
- `generate_rules` (method, `skills/hermes-lazyown/claudemd_rules.py:174`) `def generate_rules(phase, rhost, services, creds_found, is_hermes)` - Convenience function: build a rule set from parameters.
- `ConfigBridgeError` (class, `skills/hermes-lazyown/config_bridge.py:17`) `class ConfigBridgeError(Exception)` - Raised when the configuration bridge cannot resolve a required value.
- `ConfigBridge` (class, `skills/hermes-lazyown/config_bridge.py:23`) `class ConfigBridge` - Unified configuration accessor for the Hermes-LazyOwn integration.
- `__init__` (method, `skills/hermes-lazyown/config_bridge.py:35`) `def __init__(self, payload_path)`
- `get` (method, `skills/hermes-lazyown/config_bridge.py:42`) `def get(self, key, default)` - Return the value for *key*, or *default* if not found anywhere.
- `get_required` (method, `skills/hermes-lazyown/config_bridge.py:46`) `def get_required(self, key)` - Return the value for *key*, raising ConfigBridgeError if missing.
- `get_str` (method, `skills/hermes-lazyown/config_bridge.py:53`) `def get_str(self, key, default)` - Return the string value for *key*.
- `get_int` (method, `skills/hermes-lazyown/config_bridge.py:58`) `def get_int(self, key, default)` - Return the integer value for *key*.
- `get_bool` (method, `skills/hermes-lazyown/config_bridge.py:66`) `def get_bool(self, key, default)` - Return the boolean value for *key*.
- `refresh` (method, `skills/hermes-lazyown/config_bridge.py:75`) `def refresh(self)` - Invalidate all caches so the next read reloads from disk.
- `active_target` (method, `skills/hermes-lazyown/config_bridge.py:80`) `def active_target(self)` - Return a dict with the minimal target context (rhost, domain, os_id).
- `attacker_context` (method, `skills/hermes-lazyown/config_bridge.py:90`) `def attacker_context(self)` - Return a dict with the attacker context (lhost, lport, etc.).
- `is_hermes_session` (method, `skills/hermes-lazyown/config_bridge.py:99`) `def is_hermes_session(self)` - Return True if running inside a Hermes agent session.
- `_resolve` (method, `skills/hermes-lazyown/config_bridge.py:105`) `def _resolve(self, key, default)` - Resolve a key across env -> payload -> built-in default.
- `_from_env` (method, `skills/hermes-lazyown/config_bridge.py:117`) `def _from_env(self, key)` - Map payload keys to env var names and return the value, if set.
- `_from_payload` (method, `skills/hermes-lazyown/config_bridge.py:134`) `def _from_payload(self, key)` - Return the value from payload.json, loading the file if needed.
- `_load_payload` (method, `skills/hermes-lazyown/config_bridge.py:139`) `def _load_payload(self)` - Lazy-load payload.json with mtime check.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 11
- Cross-boundary resolved imports (EXTRACTED): 2

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in skills/hermes-lazyown changed?
- Should skills/hermes-lazyown be split, given cohesion 0.85?

## Sources

- `skills/hermes-lazyown/claudemd_rules.py`
- `skills/hermes-lazyown/config_bridge.py`
- `skills/hermes-lazyown/constants.py`
- `skills/hermes-lazyown/executor.py`
- `skills/hermes-lazyown/hermes_sync.py`
- `skills/hermes-lazyown/mcp_server.py`
- `skills/hermes-lazyown/output_compactor.py`
