# modules: lazyc2

*Community 4 | 67 files | cohesion 0.47*

## Definition

This community groups 67 file(s) rooted at `tests` with dominant language py (cohesion 0.47). Central symbols: `AESKeyManager`, `AutoRecommender`, `AutomationCommandSet`, `BeaconHistoryConfig`, `CSRFPolicy`, `ColabEvent`, `CollabBusSink`, `CollaborationCommandSet`. Core file: `lazyc2.py` (306 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `tests` (22 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_api_v1.py` | py | testing | 13 | yes |

### `modules` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/beacon_history.py` | py | utility | 7 | yes |
| `modules/collab_bp.py` | py | presentation | 49 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/app_factory.py` | py | presentation | 12 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |
| `cli/commands/collaboration.py` | py | utility | 8 | yes |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/campaign_db.py` | py | utility | 1 | yes |
| `modules/sinks/event_bus.py` | py | infrastructure | 1 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 306 | no |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

*... and 47 more files in this community.*


## Key Symbols

- `AutomationCommandSet` (class, `cli/commands/automation.py:17`) `class AutomationCommandSet(LazyOwnCommandSet)` - Automation & operator workflow commands.
- `do_cred_reuse` (method, `cli/commands/automation.py:24`) `def do_cred_reuse(self, line)` - Analyze captured credentials and suggest spray targets.
- `do_cred_mark_failed` (method, `cli/commands/automation.py:57`) `def do_cred_mark_failed(self, line)` - Mark a credential as failed against a host.
- `do_hooks_list` (method, `cli/commands/automation.py:78`) `def do_hooks_list(self, line)` - List all conditional hook rules.
- `do_hooks_enable` (method, `cli/commands/automation.py:101`) `def do_hooks_enable(self, line)` - Enable or disable a hook rule.
- `do_hooks_add` (method, `cli/commands/automation.py:129`) `def do_hooks_add(self, line)` - Add a new conditional hook rule (JSON string).
- `do_hooks_remove` (method, `cli/commands/automation.py:150`) `def do_hooks_remove(self, line)` - Remove a hook rule by name.
- `do_hooks_fire` (method, `cli/commands/automation.py:172`) `def do_hooks_fire(self, line)` - Manually fire a hook event for testing.
- `do_operators` (method, `cli/commands/automation.py:202`) `def do_operators(self, line)` - List all operator profiles.
- `do_operator_create` (method, `cli/commands/automation.py:229`) `def do_operator_create(self, line)` - Create a new operator profile.
- `do_operator_load` (method, `cli/commands/automation.py:264`) `def do_operator_load(self, line)` - Load effective config for an operator (team baseline + overrides).
- `do_operator_delete` (method, `cli/commands/automation.py:292`) `def do_operator_delete(self, line)` - Delete an operator profile.
- `do_hooks` (method, `cli/commands/automation.py:314`) `def do_hooks(self, line)` - Conditional hooks management — list, enable, disable, add, remove rules.
- `CollaborationCommandSet` (class, `cli/commands/collaboration.py:20`) `class CollaborationCommandSet(LazyOwnCommandSet)` - Multi-operator collaboration commands for the CLI.
- `_get_collab` (method, `cli/commands/collaboration.py:26`) `def _get_collab(self)` - Lazy-load collaboration singletons from modules.collab_bp.
- `_resolve_target` (method, `cli/commands/collaboration.py:38`) `def _resolve_target(self, target)` - Resolve a target argument: explicit IP or rhost from payload.
- `do_lock_target` (method, `cli/commands/collaboration.py:48`) `def do_lock_target(self, line)` - Acquire an advisory lock on a target to prevent tool collisions.
- `do_unlock_target` (method, `cli/commands/collaboration.py:89`) `def do_unlock_target(self, line)` - Release an advisory lock on a target.
- `do_team_status` (method, `cli/commands/collaboration.py:114`) `def do_team_status(self, line)` - Show active operators and target locks.
- `do_team_chat` (method, `cli/commands/collaboration.py:169`) `def do_team_chat(self, line)` - Send a message to all connected operators.
- `do_share_finding` (method, `cli/commands/collaboration.py:199`) `def do_share_finding(self, line)` - Share a finding or credential discovery with the team.
- `_env_tag` (function, `lazyc2.py:218`) `def _env_tag()` - Return the runtime environment tag from ``payload.json``.
- `is_insecure_credential` (function, `lazyc2.py:230`) `def is_insecure_credential(user, pwd)` - Check for weak or default credentials
- `_listen_address` (function, `lazyc2.py:278`) `def _listen_address()` - Return the bind address chosen by :class:`BindAddressResolver`.
- `_is_unspecified_bind_literal` (function, `lazyc2.py:305`) `def _is_unspecified_bind_literal(address)` - Return True when ``address`` is a wildcard bind literal.
- `_select_specific_bind_address` (function, `lazyc2.py:324`) `def _select_specific_bind_address(candidate)` - Return a specific IP literal safe to pass to ``socket.bind``.
- `_probe_bind` (function, `lazyc2.py:357`) `def _probe_bind(address, port, sock_type)` - Probe whether ``(address, port)`` can be bound for ``sock_type``.
- `_resolve_bind_address` (function, `lazyc2.py:402`) `def _resolve_bind_address(preferred, port, sock_type)` - Return an address that can actually be bound to on this host.
- `_JsonLogFormatter` (class, `lazyc2.py:467`) `class _JsonLogFormatter(Formatter)` - Optional structured JSON formatter for C2 access logs.
- `format` (method, `lazyc2.py:470`) `def format(self, record)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 154
- Cross-boundary resolved imports (EXTRACTED): 166

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 5 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `lazyc2/blueprints/api_v1.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `lazyc2.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.47?

## Sources

- `cli/commands/automation.py`
- `cli/commands/collaboration.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api_v1.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/beacon.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/__init__.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- `lazyc2/security/__init__.py`
- `lazyc2/security/command_allowlist.py`
- `lazyc2/security/constants.py`
- *... and 47 more*
