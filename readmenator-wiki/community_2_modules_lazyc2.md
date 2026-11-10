# modules: lazyc2

*Community 2 | 138 files | cohesion 0.47*

## Definition

This community groups 138 file(s) rooted at `modules` with dominant language py (cohesion 0.47). Central symbols: `AESKeyManager`, `AddonUpdateResult`, `AdvancePhaseSingleWriterSpec`, `AutoRecommender`, `AutomationCommandSet`, `AutonomousAgent`, `BeaconHistoryConfig`, `BindAddressResolver`. Core file: `lazyc2.py` (313 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `modules` (40 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/addon_updater.py` | py | utility | 10 | yes |
| `modules/beacon_history.py` | py | utility | 7 | yes |

### `tests` (31 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_addon_updater.py` | py | testing | 13 | yes |

### `contrib/legacy` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygalazy.py` | py | utility | 7 | no |
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |

### `lazyc2/security` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/__init__.py` | py | utility | 0 | no |

### `lazyc2/blueprints` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |

### `skills/hermes-lazyown` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/hermes-lazyown/claudemd_rules.py` | py | business_logic | 14 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |

### `modules/integrations` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `skills/mcp_tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/campaign.py` | py | utility | 2 | yes |

### `skills` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/daemon_health.py` | py | utility | 16 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2.py` | py | presentation | 313 | no |

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

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `modules/backdoor` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/backdoor/server.c` | c | utility | 1 | no |

*... and 118 more files in this community.*


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
- `SamsungKnoxExploitServer` (class, `contrib/legacy/lazygalazy.py:8`) `class SamsungKnoxExploitServer(BaseHTTPRequestHandler)`
- `do_GET` (method, `contrib/legacy/lazygalazy.py:11`) `def do_GET(self)`
- `apk_bytes` (method, `contrib/legacy/lazygalazy.py:33`) `def apk_bytes(self)`
- `launch_html` (method, `contrib/legacy/lazygalazy.py:36`) `def launch_html(self)`
- `exploit_js` (method, `contrib/legacy/lazygalazy.py:49`) `def exploit_js(self)`
- `rand_word` (method, `contrib/legacy/lazygalazy.py:93`) `def rand_word(self)`
- `main` (function, `contrib/legacy/lazygalazy.py:97`) `def main()`
- `signal_handler` (function, `contrib/legacy/lazygptcli.py:66`) `def signal_handler(sig, frame)`
- `show_help` (function, `contrib/legacy/lazygptcli.py:73`) `def show_help(message)`
- `check_api_key` (function, `contrib/legacy/lazygptcli.py:77`) `def check_api_key()`
- `configure_logging` (function, `contrib/legacy/lazygptcli.py:83`) `def configure_logging(debug)`
- `parse_args` (function, `contrib/legacy/lazygptcli.py:87`) `def parse_args()`
- `create_complex_prompt` (function, `contrib/legacy/lazygptcli.py:94`) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function, `contrib/legacy/lazygptcli.py:108`) `def execute_command(command)`
- `load_knowledge_base` (function, `contrib/legacy/lazygptcli.py:118`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazygptcli.py:124`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazygptcli.py:128`) `def add_to_knowledge_base(prompt, command, file_path)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 351
- Cross-boundary resolved imports (EXTRACTED): 345

## Connections

- [EXTRACTED] depends_on community 5 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/chain_mode.py imports core/logging.py.
- [EXTRACTED] depends_on community 2 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [layer strict] `lazyc2/blueprints/operations.py` (presentation) -> `lazyc2/extensions/storage.py` (data_access)
- [layer strict] `tests/test_addon_creator.py` (testing) -> `lazyc2/blueprints/addons.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `core/api_authz.py` (presentation)
- [layer strict] `tests/test_api_v1.py` (testing) -> `lazyc2/blueprints/api_v1.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)
- [layer strict] `tests/test_collab_and_onboarding.py` (testing) -> `modules/collab_bp.py` (presentation)

## Open Questions

- Why do 14 file(s) lack file-level docs (e.g. `contrib/legacy/lazygalazy.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: lazyc2 changed?
- Should modules: lazyc2 be split, given cohesion 0.47?

## Sources

- `cli/commands/automation.py`
- `contrib/legacy/lazygalazy.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyhoneypot.py`
- `contrib/legacy/lazyhttpreverseshell.py`
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
- *... and 118 more*
