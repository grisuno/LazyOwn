# modules: lazyc2

*Community 2 | 142 files | cohesion 0.48*

## Definition

This community groups 142 file(s) rooted at `modules` with dominant language py (cohesion 0.48). Central symbols: `AESKeyManager`, `ActionCategory`, `AddonUpdateResult`, `AdvancePhaseSingleWriterSpec`, `ApprovalDecision`, `ApprovalGate`, `ApprovalOutcome`, `ApprovalRequest`. Core file: `lazyc2.py` (314 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `modules` (41 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/addon_updater.py` | py | utility | 10 | yes |
| `modules/auto_purple.py` | py | utility | 40 | yes |

### `tests` (37 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_addon_creator.py` | py | testing | 86 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |
| `lazyc2/security/cli_credentials.py` | py | utility | 3 | yes |

### `contrib/legacy` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |

### `lazyc2/blueprints` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |

### `skills/mcp_tools` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/campaign.py` | py | utility | 2 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |

### `skills` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `lazyc2` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |

### `modules/sinks` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/campaign_db.py` | py | utility | 1 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 314 | no |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/purple_tui.py` | py | utility | 15 | yes |

*... and 122 more files in this community.*


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
- `_build_exec_parser` (function, `cli/commands/purple_team.py:29`) `def _build_exec_parser()`
- `_build_test_parser` (function, `cli/commands/purple_team.py:67`) `def _build_test_parser()`
- `_build_config_parser` (function, `cli/commands/purple_team.py:92`) `def _build_config_parser()`
- `_build_history_parser` (function, `cli/commands/purple_team.py:106`) `def _build_history_parser()`
- `PurpleTeamCommandSet` (class, `cli/commands/purple_team.py:124`) `class PurpleTeamCommandSet(LazyOwnCommandSet)` - Purple team orchestration commands for the LazyOwn shell.
- `_get_loop` (method, `cli/commands/purple_team.py:130`) `def _get_loop(self)` - Build a PurpleTeamLoop from payload.json config.
- `do_purple_exec` (method, `cli/commands/purple_team.py:144`) `def do_purple_exec(self, line)` - Execute a red action and measure if LazyOwnBT detects it.
- `do_purple_test` (method, `cli/commands/purple_team.py:203`) `def do_purple_test(self, args)` - Test if LazyOwnBT would detect a command (no execution).
- `do_purple_score` (method, `cli/commands/purple_team.py:223`) `def do_purple_score(self, line)` - Show current engagement detection score.
- `do_purple_report` (method, `cli/commands/purple_team.py:271`) `def do_purple_report(self, line)` - Generate full engagement report with datasets.
- `do_purple_methods` (method, `cli/commands/purple_team.py:285`) `def do_purple_methods(self, line)` - List available LazyOwnBT detection methods.
- `do_purple_config` (method, `cli/commands/purple_team.py:297`) `def do_purple_config(self, args)` - Show or update purple team configuration (payload.json).
- `do_purple_dashboard` (method, `cli/commands/purple_team.py:350`) `def do_purple_dashboard(self, line)` - Launch the Purple Team TUI dashboard.
- `do_purple_history` (method, `cli/commands/purple_team.py:367`) `def do_purple_history(self, args)` - Show recent purple team action results.
- `_load_score` (function, `cli/purple_tui.py:33`) `def _load_score()`
- `_load_recent_results` (function, `cli/purple_tui.py:42`) `def _load_recent_results(n)`
- `_dataset_stats` (function, `cli/purple_tui.py:56`) `def _dataset_stats()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 427
- Cross-boundary resolved imports (EXTRACTED): 380

## Connections

- [EXTRACTED] depends_on community 5 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/swan_agent.py` -> `skills/hive_mind.py`
- [cycle] `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `skills/swan_agent.py` -> `skills/lazyown_groq_agents.py`
- [cycle] `modules/detection_oracle.py` -> `modules/detection_feed.py` -> `modules/detection_oracle.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/integration_autonomous_flow.py` (testing) -> `modules/moe_router.py` (presentation)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `lazyc2/blueprints/api_v1.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)

## Open Questions

- Why do 12 file(s) lack file-level docs (e.g. `contrib/legacy/lazyproxy.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.48?

## Sources

- `cli/commands/automation.py`
- `cli/commands/purple_team.py`
- `cli/purple_tui.py`
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
- `lazyc2/__init__.py`
- `lazyc2/blueprints/__init__.py`
- *... and 122 more*
