# modules: lazyc2

*Community 1 | 173 files | cohesion 0.49*

## Definition

This community groups 173 file(s) rooted at `tests` with dominant language py (cohesion 0.49). Central symbols: `AESKeyManager`, `AddonUpdateResult`, `AdvisoryLedger`, `AutoRecommender`, `AutomationCommandSet`, `AutonomousAgent`, `BeaconConfig`, `BeaconConfigBuilder`. Core file: `lazyc2.py` (330 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `tests` (50 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_addon_creator.py` | py | testing | 86 | yes |

### `modules` (47 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/addon_updater.py` | py | utility | 10 | yes |
| `modules/beacon_config_builder.py` | py | infrastructure | 16 | yes |

### `lazyc2/security` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |

### `contrib/legacy` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `lazyc2/blueprints` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |

### `skills` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

### `modules/guardrails` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/guardrails/__init__.py` | py | utility | 0 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |

### `lazyc2/extensions` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/__init__.py` | py | infrastructure | 0 | yes |

### `skills/mcp_tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/campaign.py` | py | utility | 2 | yes |

### `cli/commands` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 330 | no |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/campaign_db.py` | py | utility | 1 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `browser_sync_extension` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `browser_sync_extension/background.js` | js | infrastructure | 7 | no |

### `modules/loop` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/loop/control_plane.py` | py | utility | 1 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_harness_e2e.py` | py | testing | 10 | yes |

*... and 153 more files in this community.*


## Key Symbols

- `config` (function, `browser_sync_extension/background.js:8`)
- `domainAllowed` (function, `browser_sync_extension/background.js:18`)
- `highEntropyHints` (function, `browser_sync_extension/background.js:30`)
- `sanitizeHeader` (function, `browser_sync_extension/background.js:64`)
- `collectProfile` (function, `browser_sync_extension/background.js:68`)
- `syncNow` (function, `browser_sync_extension/background.js:94`)
- `armAlarm` (function, `browser_sync_extension/background.js:123`)
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
- `BofMarketplaceCommandSet` (class, `cli/commands/bof_registry.py:44`) `class BofMarketplaceCommandSet(LazyOwnCommandSet)` - BOF marketplace: search, install, stage, deploy and run BOFs on beacons.
- `_ensure_staging_dir` (method, `cli/commands/bof_registry.py:51`) `def _ensure_staging_dir()` - Create and return the BOF staging directory path.
- `_stage_bof` (method, `cli/commands/bof_registry.py:56`) `def _stage_bof(self, bof_name)` - Stage a compiled BOF via the delivery service.
- `do_bof_search` (method, `cli/commands/bof_registry.py:87`) `def do_bof_search(self, line)` - Search the BOF catalog by keyword.
- `do_bof_info` (method, `cli/commands/bof_registry.py:108`) `def do_bof_info(self, line)` - Show detailed information about a BOF.
- `do_bof_install` (method, `cli/commands/bof_registry.py:143`) `def do_bof_install(self, line)` - Install and stage BOFs for beacon delivery.
- `do_bof_stage` (method, `cli/commands/bof_registry.py:171`) `def do_bof_stage(self, line)` - Stage a BOF artifact through its lazyaddon beacon client.
- `do_bof_run` (method, `cli/commands/bof_registry.py:191`) `def do_bof_run(self, line)` - Execute a BOF on a connected beacon.
- `do_bof_train` (method, `cli/commands/bof_registry.py:248`) `def do_bof_train(self, line)` - Run a sequence of BOFs over one beacon, awaiting each result.
- `do_bof_deploy` (method, `cli/commands/bof_registry.py:310`) `def do_bof_deploy(self, line)` - Deliver a staged beacon client onto a target and await check-in.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 470
- Cross-boundary resolved imports (EXTRACTED): 455

## Connections

- [EXTRACTED] depends_on community 7 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 6 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/integration_autonomous_flow.py` (testing) -> `modules/moe_router.py` (presentation)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `lazyc2/blueprints/api_v1.py` (presentation)
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)

## Open Questions

- Why do 14 file(s) lack file-level docs (e.g. `browser_sync_extension/background.js`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.49?

## Sources

- `browser_sync_extension/background.js`
- `cli/commands/automation.py`
- `cli/commands/bof_registry.py`
- `cli/commands/enum.py`
- `contrib/legacy/lazydeepseekcli.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyopenssh77enum2.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazysearch_bot.py`
- `contrib/legacy/lazyseo.py`
- `contrib/legacy/lazysmbrelay.py`
- `contrib/legacy/lazyssh.py`
- `core/executor.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `core/session_secrets.py`
- `lazyc2.py`
- *... and 153 more*
