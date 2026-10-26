# modules: world_model

*Community 5 | 63 files | cohesion 0.40*

## Definition

This community groups 63 file(s) rooted at `modules` with dominant language py (cohesion 0.40). Central symbols: `ADCSCertipyWrapper`, `C2Builder`, `C2Profile`, `C2Server`, `C2SessionCommandSet`, `CertificateTemplate`, `ChainResult`, `Completed`. Core file: `modules/world_model.py` (70 symbols). Documented purpose: C2 session CommandSet — headless server, agent deploy, exec, loot.  Every command is non-interactive and loop-routable: explicit arguments, JSON-able results on.

## Files

### `modules` (24 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/adcs_attacks.py` | py | utility | 14 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 37 | yes |
| `modules/attack_surface3d.py` | py | utility | 11 | yes |
| `modules/beacon_recon.py` | py | utility | 6 | yes |

### `tests` (21 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_attack_surface3d.py` | py | testing | 8 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |
| `tests/test_beacon_recon_sink.py` | py | testing | 18 | yes |
| `tests/test_c2_surfaces.py` | py | testing | 12 | yes |

### `modules/sinks` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |
| `modules/sinks/intel_graph.py` | py | utility | 1 | yes |
| `modules/sinks/killchain.py` | py | utility | 1 | yes |

### `cli/commands` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/c2_session.py` | py | utility | 10 | yes |
| `cli/commands/database.py` | py | data_access | 16 | yes |
| `cli/commands/exploit_migrated.py` | py | utility | 52 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/surface_graph.py` | py | utility | 33 | yes |
| `cli/surface_tui.py` | py | utility | 19 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/autonomous.py` | py | utility | 3 | yes |
| `core/session_secrets.py` | py | utility | 4 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

*... and 43 more files in this community.*


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
- `DatabaseCommandSet` (class, `cli/commands/database.py:26`) `class DatabaseCommandSet(LazyOwnCommandSet)` - Database commands for campaign state management.
- `_get_db` (method, `cli/commands/database.py:32`) `def _get_db(self)`
- `_active_workspace` (method, `cli/commands/database.py:40`) `def _active_workspace(self)`
- `do_db_init` (method, `cli/commands/database.py:57`) `def do_db_init(self, line)` - Initialize the database (creates schema if not exists).
- `do_db_workspace` (method, `cli/commands/database.py:75`) `def do_db_workspace(self, line)` - Manage workspaces (list, create, switch, delete).
- `do_db_hosts` (method, `cli/commands/database.py:124`) `def do_db_hosts(self, line)` - List or add hosts in the active workspace.
- `do_db_services` (method, `cli/commands/database.py:185`) `def do_db_services(self, line)` - List all services in the active workspace.
- `do_db_vulns` (method, `cli/commands/database.py:213`) `def do_db_vulns(self, line)` - List or add vulnerabilities.
- `do_retest` (method, `cli/commands/database.py:267`) `def do_retest(self, line)` - Re-verify a finding in an isolated session (LAZY retester).
- `do_db_creds` (method, `cli/commands/database.py:349`) `def do_db_creds(self, line)` - List or add credentials.
- `do_db_loot` (method, `cli/commands/database.py:393`) `def do_db_loot(self, line)` - List or add loot items.
- `do_db_notes` (method, `cli/commands/database.py:433`) `def do_db_notes(self, line)` - List or add notes.
- `do_db_import` (method, `cli/commands/database.py:471`) `def do_db_import(self, line)` - Import scan results into the database.
- `do_db_export` (method, `cli/commands/database.py:509`) `def do_db_export(self, line)` - Export database table to CSV.
- `do_db_status` (method, `cli/commands/database.py:543`) `def do_db_status(self, line)` - Show entity counts for the active workspace.
- `shlex_split` (function, `cli/commands/database.py:560`) `def shlex_split(text)` - Split text like shlex.split but handle empty strings gracefully.
- `ExploitMigratedCommandSet` (class, `cli/commands/exploit_migrated.py:38`) `class ExploitMigratedCommandSet(LazyOwnCommandSet)`
- `do_cp` (method, `cli/commands/exploit_migrated.py:43`) `def do_cp(self, line)` - Copies a file from the ExploitDB directory to the sessions directory.
- `do_createcookie` (method, `cli/commands/exploit_migrated.py:84`) `def do_createcookie(self, line)` - Creates a `cookie.txt` file in the `sessions` directory with the specified cookie value.
- `do_py3ttyup` (method, `cli/commands/exploit_migrated.py:128`) `def do_py3ttyup(self, line)` - Copies a Python reverse shell command to the clipboard.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 161
- Cross-boundary resolved imports (EXTRACTED): 297

## Connections

- [EXTRACTED] depends_on community 5 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 7 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports modules/c2_builder.py.
- [EXTRACTED] depends_on community 5 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports modules/db.py.
- [EXTRACTED] depends_on community 5 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports skills/autonomous_daemon.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:204` `validate_client_id` `ct`: Result of allocator stored in `ct` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:256` `validate_client_id` `data`: Result of allocator stored in `data` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `modules/c2_agent.py:303` `validate_client_id` `_dn`: Result of allocator stored in `_dn` is never checked against NULL.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `tests/test_gym_ms2_cli.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/chain_mediator.py` -> `modules/lazy_loop.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: world_model changed?
- Should modules: world_model be split, given cohesion 0.40?

## Sources

- `cli/commands/c2_session.py`
- `cli/commands/database.py`
- `cli/commands/exploit_migrated.py`
- `cli/commands/lab.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/surface.py`
- `cli/surface_graph.py`
- `cli/surface_tui.py`
- `contrib/legacy/lazydeepseekcli.py`
- `core/autonomous.py`
- `core/session_secrets.py`
- `modules/adcs_attacks.py`
- `modules/atomic_exploit_bridge.py`
- `modules/attack_surface3d.py`
- `modules/beacon_recon.py`
- `modules/c2_agent.py`
- `modules/c2_builder.py`
- `modules/c2_surfaces.py`
- `modules/ctf_capture.py`
- `modules/estorides_fusion.py`
- *... and 43 more*
