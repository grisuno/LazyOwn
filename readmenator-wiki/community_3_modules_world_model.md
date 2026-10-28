# modules: world_model

*Community 3 | 110 files | cohesion 0.45*

## Definition

This community groups 110 file(s) rooted at `tests` with dominant language py (cohesion 0.45). Central symbols: `ADCSCertipyWrapper`, `AIExploitChainer`, `AddonCatalog`, `AddonEntry`, `AdvancePhaseSingleWriterSpec`, `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: C2 session CommandSet — headless server, agent deploy, exec, loot.  Every command is non-interactive and loop-routable: explicit arguments, JSON-able results on.

## Files

### `tests` (37 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_atomic_exploit_bridge.py` | py | testing | 36 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |

### `modules` (35 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |
| `modules/apt_playbooks.py` | py | utility | 15 | yes |

### `cli` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/dashboard_layout.py` | py | presentation | 3 | yes |
| `cli/dashboard_tui.py` | py | utility | 64 | yes |

### `modules/sinks` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/beacon_dispatch.py` | py | utility | 3 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/c2_session.py` | py | utility | 10 | yes |
| `cli/commands/estorides.py` | py | utility | 9 | yes |

### `contrib/legacy` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |
| `contrib/legacy/lazypwn.py` | py | utility | 15 | no |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |
| `core/safe_exec.py` | py | utility | 12 | yes |

### `lazygui` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/__init__.py` | py | utility | 0 | yes |
| `lazygui/version.py` | py | utility | 0 | yes |

### `modules/integrations` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/nuclei_bridge.py` | py | utility | 29 | yes |
| `modules/integrations/nuclei_parser.py` | py | utility | 17 | yes |

*... and 90 more files in this community.*


## Key Symbols

- `_lab_auth` (function, `cli/commands/c2_session.py:24`) `def _lab_auth()` - Return (user, password, https_port, http_port) for the lab C2.
- `_fresh_lab_creds` (function, `cli/commands/c2_session.py:54`) `def _fresh_lab_creds()` - Generate fully random lab operator credentials (no fixed affixes).
- `_server` (function, `cli/commands/c2_session.py:65`) `def _server(user, password, port)` - Build a C2Server bound to lab auth (generates lab creds when needed).
- `_issue` (function, `cli/commands/c2_session.py:83`) `def _issue(client_id, command, auth, https_port)` - POST one command to the C2 issue endpoint (no prompts, ever).
- `C2SessionCommandSet` (class, `cli/commands/c2_session.py:108`) `class C2SessionCommandSet(LazyOwnCommandSet)` - Headless C2 lifecycle + session ops: server, deploy, exec, loot.
- `do_c2_server` (method, `cli/commands/c2_session.py:115`) `def do_c2_server(self, line)` - Manage the headless C2 server (lab use).
- `do_c2_reboot` (method, `cli/commands/c2_session.py:168`) `def do_c2_reboot(self, line)` - Restart the headless C2 server with ROTATED operator credentials.
- `do_c2_deploy` (method, `cli/commands/c2_session.py:249`) `def do_c2_deploy(self, line)` - Deploy the malleable agent to a lab target (needs root shell primitive).
- `do_c2_exec` (method, `cli/commands/c2_session.py:299`) `def do_c2_exec(self, line)` - Run one command on a live C2 session and print its answer.
- `do_c2_loot` (method, `cli/commands/c2_session.py:346`) `def do_c2_loot(self, line)` - Exfiltrate a remote file through a live C2 session into sessions/loot/.
- `_yellow` (function, `cli/commands/estorides.py:43`) `def _yellow(text)`
- `_green` (function, `cli/commands/estorides.py:47`) `def _green(text)`
- `EstoridesCommandSet` (class, `cli/commands/estorides.py:51`) `class EstoridesCommandSet(LazyOwnCommandSet)` - Bidirectional Estorides <-> LazyOwn integration commands.
- `_check_estorides` (method, `cli/commands/estorides.py:57`) `def _check_estorides(self)` - Check that estorides is cloned and available.
- `do_estorides_seed` (method, `cli/commands/estorides.py:73`) `def do_estorides_seed(self, line)` - Feed LazyOwn hosts/domains into Estorides for passive OSINT discovery.
- `do_estorides_import` (method, `cli/commands/estorides.py:189`) `def do_estorides_import(self, line)` - Import Estorides-discovered entities into LazyOwn database and scope.
- `_preview_entities` (method, `cli/commands/estorides.py:319`) `def _preview_entities(self, entities)` - Show a preview of entities grouped by type.
- `do_estorides_loop` (method, `cli/commands/estorides.py:337`) `def do_estorides_loop(self, line)` - Run the bidirectional Estorides <-> LazyOwn feedback loop.
- `do_estorides_surface` (method, `cli/commands/estorides.py:441`) `def do_estorides_surface(self, line)` - Show the combined active + passive attack surface.
- `ExploitMigratedCommandSet` (class, `cli/commands/exploit_migrated.py:38`) `class ExploitMigratedCommandSet(LazyOwnCommandSet)`
- `do_cp` (method, `cli/commands/exploit_migrated.py:43`) `def do_cp(self, line)` - Copies a file from the ExploitDB directory to the sessions directory.
- `do_createcookie` (method, `cli/commands/exploit_migrated.py:84`) `def do_createcookie(self, line)` - Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `do_py3ttyup` (method, `cli/commands/exploit_migrated.py:128`) `def do_py3ttyup(self, line)` - Copies a Python reverse shell command to the clipboard.
- `do_pyautomate` (method, `cli/commands/exploit_migrated.py:164`) `def do_pyautomate(self, line)` - Automates the execution of pwntomate tools on XML configuration files.
- `do_winbase64payload` (method, `cli/commands/exploit_migrated.py:215`) `def do_winbase64payload(self, line)` - Creates a base64 encoded payload specifically for Windows to execute a PowerShell command or downloa
- `do_createdll` (method, `cli/commands/exploit_migrated.py:344`) `def do_createdll(self, line)` - Create a Windows DLL file using MinGW-w64 or a Blazor DLL for Linux.
- `do_seo` (method, `cli/commands/exploit_migrated.py:402`) `def do_seo(self, line)` - Performs a web seo fingerprinting scan using `lazyseo.py`.
- `do_padbuster` (method, `cli/commands/exploit_migrated.py:437`) `def do_padbuster(self, line)` - Execute the PadBuster command for padding oracle attacks.
- `do_cacti_exploit` (method, `cli/commands/exploit_migrated.py:483`) `def do_cacti_exploit(self, line)` - Automates the exploitation of the Cacti version 1.2.26 vulnerability
- `setup_handler` (function, `cli/commands/exploit_migrated.py:513`) `def setup_handler(config_file, lhost, lport)` - Sets up a Metasploit multi/handler exploit configuration in the provided config file.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 362
- Cross-boundary resolved imports (EXTRACTED): 407

## Connections

- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/command_chain.py imports cli/exploration.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 9 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/atomic_exploit_bridge.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/unified_dashboard.py` -> `skills/hive_mind.py`
- [cycle] `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [layer strict] `tests/test_exploration_and_addons.py` (testing) -> `cli/exploration_view.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `cli/commands/recon.py:603` `_run_single_search` `_s`: Result of allocator stored in `_s` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `cli/lazynmap_post.py:243` `_emit_event` `fd`: Result of allocator stored in `fd` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/auto_pivot.py:222` `health_check` `sock`: Result of allocator stored in `sock` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:204` `validate_client_id` `ct`: Result of allocator stored in `ct` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.45?

## Sources

- `cli/commands/c2_session.py`
- `cli/commands/estorides.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/pwn.py`
- `cli/commands/recon.py`
- `cli/commands/surface.py`
- `cli/dashboard_layout.py`
- `cli/dashboard_tui.py`
- `cli/exploit_advisor.py`
- `cli/exploration.py`
- `cli/exploration_view.py`
- `cli/graph_advisor.py`
- `cli/killchain.py`
- `cli/lazynmap_post.py`
- `cli/ops_commands.py`
- `cli/recommendation.py`
- `cli/recommendation_signals.py`
- `cli/recon_plan.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- *... and 90 more*
