# modules: lazyc2

*Community 1 | 128 files | cohesion 0.52*

## Definition

This community groups 128 file(s) rooted at `modules` with dominant language py (cohesion 0.52). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AESKeyManager`, `AIResult`, `AccessFact`. Core file: `lazyc2.py` (288 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `modules` (37 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ai_fallback.py` | py | utility | 8 | yes |
| `modules/beacon_history.py` | py | utility | 7 | yes |

### `tests` (33 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aci_planner.py` | py | testing | 95 | yes |
| `tests/test_addon_creator.py` | py | testing | 86 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/command_allowlist.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |

### `skills` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/daemon_health.py` | py | utility | 16 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/api_authz.py` | py | presentation | 31 | yes |
| `core/executor.py` | py | utility | 6 | yes |

### `lazyc2/extensions` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |

### `contrib/legacy` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyhoneypot.py` | py | utility | 15 | yes |

### `lazyc2` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazy_sentinel4.py` | py | utility | 47 | no |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_facts.py` | py | testing | 37 | yes |

*... and 108 more files in this community.*


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
- `_yellow` (function, `cli/commands/estorides.py:43`) `def _yellow(text)`
- `_green` (function, `cli/commands/estorides.py:47`) `def _green(text)`
- `EstoridesCommandSet` (class, `cli/commands/estorides.py:51`) `class EstoridesCommandSet(LazyOwnCommandSet)` - Bidirectional Estorides <-> LazyOwn integration commands.
- `_check_estorides` (method, `cli/commands/estorides.py:57`) `def _check_estorides(self)` - Check that estorides is cloned and available.
- `do_estorides_seed` (method, `cli/commands/estorides.py:73`) `def do_estorides_seed(self, line)` - Feed LazyOwn hosts/domains into Estorides for passive OSINT discovery.
- `do_estorides_import` (method, `cli/commands/estorides.py:189`) `def do_estorides_import(self, line)` - Import Estorides-discovered entities into LazyOwn database and scope.
- `_preview_entities` (method, `cli/commands/estorides.py:319`) `def _preview_entities(self, entities)` - Show a preview of entities grouped by type.
- `do_estorides_loop` (method, `cli/commands/estorides.py:337`) `def do_estorides_loop(self, line)` - Run the bidirectional Estorides <-> LazyOwn feedback loop.
- `do_estorides_surface` (method, `cli/commands/estorides.py:441`) `def do_estorides_surface(self, line)` - Show the combined active + passive attack surface.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 445
- Cross-boundary resolved imports (EXTRACTED): 322

## Connections

- [EXTRACTED] depends_on community 10 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 11 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/toposwarm_bridge.py` via `subprocess` (5 hops)
- [cycle] `skills/autonomous_daemon.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_authz.py` (testing) -> `core/api_authz.py` (presentation)

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `contrib/legacy/lazyssh.py`)? What purpose do they serve?
- Can the cycle `skills/autonomous_daemon.py` -> `modules/pipeline_engine.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.52?

## Sources

- `cli/commands/automation.py`
- `cli/commands/collaboration.py`
- `cli/commands/estorides.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyssh.py`
- `core/api_authz.py`
- `core/executor.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `lazy_sentinel4.py`
- `lazyc2.py`
- `lazyc2/__init__.py`
- `lazyc2/addon_creator.py`
- `lazyc2/app_factory.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api.py`
- *... and 108 more*
