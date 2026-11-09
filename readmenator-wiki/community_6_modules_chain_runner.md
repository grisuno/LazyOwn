# modules: chain_runner

*Community 6 | 73 files | cohesion 0.53*

## Definition

This community groups 73 file(s) rooted at `tests` with dominant language py (cohesion 0.53). Central symbols: `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`, `AtomicTest`, `AtomicTestRef`, `BackendSelection`, `Broken`, `C2Approver`. Core file: `tests/test_security_hardening_v4.py` (67 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (38 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 28 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_atomic_exploit_bridge.py` | py | testing | 38 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |
| `tests/test_chain_approval_c2.py` | py | testing | 27 | yes |
| `tests/test_chain_approval_cli_wiring.py` | py | testing | 2 | yes |
| `tests/test_chain_distill.py` | py | testing | 15 | yes |

### `modules` (30 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ad_gym.py` | py | utility | 10 | yes |
| `modules/apt_playbooks.py` | py | utility | 17 | yes |
| `modules/atomic_cli.py` | py | utility | 11 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 39 | yes |
| `modules/atomic_resolver.py` | py | utility | 27 | yes |
| `modules/chain_approval.py` | py | utility | 18 | yes |
| `modules/chain_distill.py` | py | utility | 23 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 19 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/safe_exec.py` | py | utility | 14 | yes |
| `core/safe_subprocess.py` | py | utility | 7 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/command_and_control_migrated.py` | py | utility | 34 | yes |

*... and 53 more files in this community.*


## Key Symbols

- `_parse_admin_flags` (function, `cli/apt_chain_support.py:46`) `def _parse_admin_flags(args, tokens)` - Split admin tokens into positionals, valued flags and plain flags.
- `_token_name_ok` (function, `cli/apt_chain_support.py:77`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:83`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:108`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:174`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `_synth_from_playbook` (function, `cli/apt_chain_support.py:202`) `def _synth_from_playbook(playbook, target)` - Lower one named APT playbook into a written chain; admin payload.
- `resolve_admin` (function, `cli/apt_chain_support.py:231`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:353`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:385`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:393`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `build_cli_approver` (function, `cli/apt_chain_support.py:426`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:434`) `def approve(step_id, command)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:448`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:451`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:473`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:482`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:504`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:532`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:606`) `def _platform()` - Guess the loop platform from the payload configuration.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 270
- Cross-boundary resolved imports (EXTRACTED): 192

## Connections

- [EXTRACTED] depends_on community 6 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 6 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 6 <-> 18 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 6 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 6 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports core/config.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `core/config.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [cycle] `modules/auto_registry.py` -> `modules/command_executor.py` -> `modules/auto_registry.py`
- [dataflow UNCHECKED_ALLOC] `modules/command_executor.py:224` `run_tee` `handle`: Result of allocator stored in `handle` is never checked against NULL.

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: chain_runner changed?
- Should modules: chain_runner be split, given cohesion 0.53?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/retry_support.py`
- `core/safe_exec.py`
- `core/safe_subprocess.py`
- `modules/ad_gym.py`
- `modules/apt_playbooks.py`
- `modules/atomic_cli.py`
- `modules/atomic_exploit_bridge.py`
- `modules/atomic_resolver.py`
- `modules/chain_approval.py`
- `modules/chain_distill.py`
- `modules/chain_facts.py`
- `modules/chain_loop.py`
- `modules/chain_registry.py`
- `modules/chain_runner.py`
- `modules/chain_state.py`
- `modules/chain_synth.py`
- `modules/chain_tokens.py`
- `modules/command_executor.py`
- *... and 53 more*
