# modules

*Community 4 | 180 files | cohesion 0.70*

## Definition

This community groups 180 file(s) rooted at `modules` with dominant language py (cohesion 0.70). Central symbols: `ACIEngine`, `ACIGoal`, `ACIPlan`, `ACIPlanner`, `ACIReflector`, `AIModel`, `AIResult`, `ASTToolExtractor`. Core file: `lazyc2.py` (263 symbols). Documented purpose: Automation command set — credential reuse, conditional hooks, operator profiles.  Provides CLI commands for managing the credential reuse engine, conditional ho.

## Files

### `modules` (67 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 35 | yes |
| `modules/agent_tool.py` | py | utility | 4 | no |

### `tests` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_aci_planner.py` | py | testing | 95 | yes |

### `skills` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/aci_planner.py` | py | utility | 42 | yes |
| `skills/autonomous_daemon.py` | py | presentation | 132 | yes |

### `modules/legacy` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |
| `modules/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `lazyc2/blueprints` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/__init__.py` | py | utility | 0 | yes |

### `skills/tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_autonomous_daemon.py` | py | testing | 88 | yes |

### `core` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/executor.py` | py | utility | 6 | yes |

### `lazyc2/extensions` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |

### `modules/integrations` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |

### `.` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazy_sentinel4.py` | py | utility | 47 | no |

### `lazyc2/security` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/csrf.py` | py | utility | 11 | yes |

### `lazygui/theme` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/theme/__init__.py` | py | presentation | 0 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/automation.py` | py | utility | 13 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |

### `lazygui/theme/palettes` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/theme/palettes/__init__.py` | py | presentation | 1 | yes |

*... and 160 more files in this community.*


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
- `_build_auto_populate_parser` (function, `cli/commands/mcp_bridge.py:50`) `def _build_auto_populate_parser()` - Return the argparse parser used by ``auto_populate``.
- `_build_facts_show_parser` (function, `cli/commands/mcp_bridge.py:67`) `def _build_facts_show_parser()` - Return the argparse parser used by ``facts_show``.
- `_build_rag_query_parser` (function, `cli/commands/mcp_bridge.py:84`) `def _build_rag_query_parser()` - Return the argparse parser used by ``rag_query``.
- `_build_parquet_query_parser` (function, `cli/commands/mcp_bridge.py:92`) `def _build_parquet_query_parser()` - Return the argparse parser used by ``parquet_query``.
- `_build_threat_model_parser` (function, `cli/commands/mcp_bridge.py:111`) `def _build_threat_model_parser()` - Return the argparse parser used by ``threat_model``.
- `_build_playbook_run_parser` (function, `cli/commands/mcp_bridge.py:124`) `def _build_playbook_run_parser()` - Return the argparse parser used by ``playbook_run``.
- `McpBridgeCommandSet` (class, `cli/commands/mcp_bridge.py:138`) `class McpBridgeCommandSet(LazyOwnCommandSet)` - CLI shims exposing the documented MCP verbs to human operators.
- `do_auto_populate` (method, `cli/commands/mcp_bridge.py:146`) `def do_auto_populate(self, args)` - Parse the latest nmap XML scan and auto-populate payload context.
- `do_facts_show` (method, `cli/commands/mcp_bridge.py:253`) `def do_facts_show(self, args)` - Show structured facts extracted from nmap scans and tool output.
- `do_rag_query` (method, `cli/commands/mcp_bridge.py:278`) `def do_rag_query(self, args)` - Semantic search over session artefacts (scans, logs, notes).
- `do_parquet_query` (method, `cli/commands/mcp_bridge.py:308`) `def do_parquet_query(self, args)` - Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).
- `do_threat_model` (method, `cli/commands/mcp_bridge.py:370`) `def do_threat_model(self, args)` - Build or inspect the threat model derived from session events.
- `do_playbook_run` (method, `cli/commands/mcp_bridge.py:423`) `def do_playbook_run(self, args)` - Execute a generated YAML playbook step by step through the shell.
- `_executor` (method, `cli/commands/mcp_bridge.py:467`) `def _executor(command, host)`
- `do_auto_loop` (method, `cli/commands/mcp_bridge.py:481`) `def do_auto_loop(self, line)` - Run a goal through the autonomous daemon orchestrator backend.
- `do_session_state` (method, `cli/commands/mcp_bridge.py:499`) `def do_session_state(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state).
- `do_campaign_sitrep` (method, `cli/commands/mcp_bridge.py:504`) `def do_campaign_sitrep(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep).

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 923
- Cross-boundary resolved imports (EXTRACTED): 271

## Connections

- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports core/logging.py.
- [EXTRACTED] depends_on community 0 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_adapter.py.
- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: lazyc2/app_factory.py imports lazyc2/blueprints/__init__.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports lazyc2/security/command_allowlist.py.
- [EXTRACTED] depends_on community 4 <-> 9 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports lazyc2/security/cors.py.
- [EXTRACTED] depends_on community 4 <-> 6 (strength 0.9): Extracted import edge crosses communities: lazyc2.py imports modules/live_surface.py.
- [EXTRACTED] depends_on community 10 <-> 4 (strength 0.9): Extracted import edge crosses communities: lazygui/app.py imports core/logging.py.
- [EXTRACTED] depends_on community 4 <-> 11 (strength 0.9): Extracted import edge crosses communities: lazygui/theme/__init__.py imports lazygui/theme/tokens.py.
- [EXTRACTED] depends_on community 4 <-> 19 (strength 0.9): Extracted import edge crosses communities: pwntomate.py imports skills/claude_md_orchestrator/parser.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [cycle] `lazyc2/blueprints/__init__.py` -> `lazyc2/blueprints/auth.py` -> `lazyc2.py` -> `lazyc2/blueprints/__init__.py`
- [cycle] `modules/detection_oracle.py` -> `modules/detection_feed.py` -> `modules/detection_oracle.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/lazyown_llm.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`

## Open Questions

- Why do 14 file(s) lack file-level docs (e.g. `lazy_sentinel4.py`)? What purpose do they serve?
- Can the cycle `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` be broken with an interface?
- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.70?

## Sources

- `cli/commands/automation.py`
- `cli/commands/mcp_bridge.py`
- `core/executor.py`
- `core/llm_budget.py`
- `core/logging.py`
- `core/scheduler.py`
- `core/security.py`
- `lazy_sentinel4.py`
- `lazyc2.py`
- `lazyc2/addon_creator.py`
- `lazyc2/blueprints/__init__.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/api.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/beacon.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/phishing.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/short_urls.py`
- *... and 160 more*
