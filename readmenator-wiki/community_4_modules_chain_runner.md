# modules: chain_runner

*Community 4 | 81 files | cohesion 0.50*

## Definition

This community groups 81 file(s) rooted at `tests` with dominant language py (cohesion 0.50). Central symbols: `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`, `AtomicTest`, `AtomicTestRef`, `BackendSelection`, `Broken`, `C2Approver`. Core file: `tests/test_security_hardening_v4.py` (67 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (36 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 22 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_atomic_exploit_bridge.py` | py | testing | 38 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |

### `modules` (32 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ad_gym.py` | py | utility | 10 | yes |
| `modules/apt_playbooks.py` | py | utility | 15 | yes |
| `modules/atomic_cli.py` | py | utility | 11 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 39 | yes |
| `modules/atomic_resolver.py` | py | utility | 27 | yes |

### `modules/sinks` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/sinks/__init__.py` | py | utility | 0 | yes |
| `modules/sinks/attack_graph.py` | py | utility | 1 | yes |
| `modules/sinks/beacon_dispatch.py` | py | utility | 3 | yes |
| `modules/sinks/c2_surfaces.py` | py | utility | 1 | yes |
| `modules/sinks/intel_graph.py` | py | utility | 1 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 17 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/command_and_control_migrated.py` | py | utility | 34 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/safe_exec.py` | py | utility | 14 | yes |

*... and 61 more files in this community.*


## Key Symbols

- `_token_name_ok` (function, `cli/apt_chain_support.py:45`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:51`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:75`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:144`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `resolve_admin` (function, `cli/apt_chain_support.py:172`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:291`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:323`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:331`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `build_cli_approver` (function, `cli/apt_chain_support.py:364`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:372`) `def approve(step_id, command)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:386`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:389`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:411`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:420`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:442`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:470`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:544`) `def _platform()` - Guess the loop platform from the payload configuration.
- `select_agent_flavour` (function, `cli/commands/command_and_control_migrated.py:43`) `def select_agent_flavour(run_tests, platform)` - Pick the agent script extension from the tests of the current run.
- `CommandAndControlMigratedCommandSet` (class, `cli/commands/command_and_control_migrated.py:66`) `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)`
- `do_msf` (method, `cli/commands/command_and_control_migrated.py:71`) `def do_msf(self, line)` - Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells
- `do_c2` (method, `cli/commands/command_and_control_migrated.py:421`) `def do_c2(self, line)` - Handle C2 server setup and agent compilation.
- `do_listener` (method, `cli/commands/command_and_control_migrated.py:543`) `def do_listener(self, line)` - Manage C2 listeners: list, add, start, stop, remove.
- `_api` (function, `cli/commands/command_and_control_migrated.py:570`) `def _api(method, endpoint, payload)`
- `do_sandbox` (method, `cli/commands/command_and_control_migrated.py:671`) `def do_sandbox(self, line)` - Toggle or query Docker sandbox mode.
- `do_msfrpc` (method, `cli/commands/command_and_control_migrated.py:713`) `def do_msfrpc(self, line)` - Connects to the msfrpcd daemon and allows remote control of Metasploit.
- `do_sliver_server` (method, `cli/commands/command_and_control_migrated.py:737`) `def do_sliver_server(self, line)` - Starts the Sliver server and generates a client configuration file for connecting clients.
- `do_empire` (method, `cli/commands/command_and_control_migrated.py:854`) `def do_empire(self, line)` - Generates payloads using PowerShell Empire with various options.
- `do_automsf` (method, `cli/commands/command_and_control_migrated.py:904`) `def do_automsf(self, line)` - Try to check if Vulnerable using the module passed by argument of lazyown example automsf exploit/wi
- `do_iis_webdav_upload_asp` (method, `cli/commands/command_and_control_migrated.py:949`) `def do_iis_webdav_upload_asp(self, line)` - (CVE-2017-7269). Vulnerable using the module iis_webdav_upload_asp of metasploit
- `do_duckyspark` (method, `cli/commands/command_and_control_migrated.py:984`) `def do_duckyspark(self, line)` - duckyspark Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucl

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 284
- Cross-boundary resolved imports (EXTRACTED): 225

## Connections

- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 4 <-> 17 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 4 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/aliases.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_ledger.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/sinks/routing.py` -> `modules/lazy_intel.py`
- [cycle] `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [layer strict] `tests/test_c2_surfaces.py` (testing) -> `contrib/legacy/lazydeepseekcli.py` (presentation)
- [dataflow UNCHECKED_ALLOC] `modules/command_executor.py:224` `run_tee` `handle`: Result of allocator stored in `handle` is never checked against NULL.

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop_triggers.py` -> `modules/trigger_policy.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/planner.py` -> `modules/playbook_engine.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: chain_runner changed?
- Should modules: chain_runner be split, given cohesion 0.50?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/retry_support.py`
- `contrib/legacy/lazydeepseekcli.py`
- `core/safe_exec.py`
- `modules/ad_gym.py`
- `modules/apt_playbooks.py`
- `modules/atomic_cli.py`
- `modules/atomic_exploit_bridge.py`
- `modules/atomic_resolver.py`
- `modules/beacon_recon.py`
- `modules/c2_surfaces.py`
- `modules/chain_approval.py`
- `modules/chain_distill.py`
- `modules/chain_facts.py`
- `modules/chain_registry.py`
- `modules/chain_runner.py`
- `modules/chain_state.py`
- `modules/chain_synth.py`
- `modules/chain_tokens.py`
- *... and 61 more*
