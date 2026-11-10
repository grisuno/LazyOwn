# modules: chain_runner

*Community 7 | 64 files | cohesion 0.54*

## Definition

This community groups 64 file(s) rooted at `tests` with dominant language py (cohesion 0.54). Central symbols: `AdaptiveFallbackArbiter`, `Alternative`, `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`, `AtomicTest`, `AtomicTestRef`, `BackendSelection`. Core file: `modules/chain_runner.py` (46 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (31 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 28 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |
| `tests/test_chain_approval_c2.py` | py | testing | 27 | yes |
| `tests/test_chain_approval_cli_wiring.py` | py | testing | 2 | yes |

### `modules` (25 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ad_gym.py` | py | utility | 10 | yes |
| `modules/apt_playbooks.py` | py | utility | 17 | yes |
| `modules/atomic_exploit_bridge.py` | py | utility | 39 | yes |
| `modules/atomic_resolver.py` | py | utility | 27 | yes |
| `modules/chain_approval.py` | py | utility | 18 | yes |
| `modules/chain_distill.py` | py | utility | 23 | yes |

### `skills/mcp_tools` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/apt_chain.py` | py | utility | 1 | yes |
| `skills/mcp_tools/atomic_clean.py` | py | utility | 1 | yes |
| `skills/mcp_tools/atomic_shell.py` | py | utility | 1 | yes |
| `skills/mcp_tools/ttp_chain.py` | py | utility | 1 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 25 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/command_and_control_migrated.py` | py | utility | 34 | yes |
| `cli/commands/lazy_adaptive.py` | py | utility | 4 | yes |

*... and 44 more files in this community.*


## Key Symbols

- `_parse_admin_flags` (function, `cli/apt_chain_support.py:46`) `def _parse_admin_flags(args, tokens)` - Split admin tokens into positionals, valued flags and plain flags.
- `_token_name_ok` (function, `cli/apt_chain_support.py:77`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:83`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:109`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:177`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `_synth_from_playbook` (function, `cli/apt_chain_support.py:205`) `def _synth_from_playbook(playbook, target)` - Lower one named APT playbook into a written chain; admin payload.
- `resolve_admin` (function, `cli/apt_chain_support.py:234`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:356`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:388`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:396`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `build_cli_approver` (function, `cli/apt_chain_support.py:437`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:445`) `def approve(step_id, command)`
- `_step_from_alternative` (function, `cli/apt_chain_support.py:459`) `def _step_from_alternative(alternative, outcome, target)` - Build one safe replan step from an adaptive fallback alternative.
- `_observed_conditions` (function, `cli/apt_chain_support.py:476`) `def _observed_conditions(target)` - Read observed services and credential evidence for one host.
- `build_adaptive_replanner` (function, `cli/apt_chain_support.py:497`) `def build_adaptive_replanner()` - Return a replanner driven by ``modules.lazy_fallback``.
- `replan` (function, `cli/apt_chain_support.py:510`) `def replan(context)`
- `compose_replanners` (function, `cli/apt_chain_support.py:535`) `def compose_replanners(replanners)` - Return one replanner running every non-None replanner in order.
- `composed` (function, `cli/apt_chain_support.py:548`) `def composed(context)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:555`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:558`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:580`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:589`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:611`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:639`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:713`) `def _platform()` - Guess the loop platform from the payload configuration.
- `select_agent_flavour` (function, `cli/commands/command_and_control_migrated.py:43`) `def select_agent_flavour(run_tests, platform)` - Pick the agent script extension from the tests of the current run.
- `CommandAndControlMigratedCommandSet` (class, `cli/commands/command_and_control_migrated.py:66`) `class CommandAndControlMigratedCommandSet(LazyOwnCommandSet)`
- `do_msf` (method, `cli/commands/command_and_control_migrated.py:71`) `def do_msf(self, line)` - Automates various Metasploit tasks including scanning for vulnerabilities, setting up reverse shells
- `do_c2` (method, `cli/commands/command_and_control_migrated.py:421`) `def do_c2(self, line)` - Handle C2 server setup and agent compilation.
- `do_listener` (method, `cli/commands/command_and_control_migrated.py:543`) `def do_listener(self, line)` - Manage C2 listeners: list, add, start, stop, remove.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 208
- Cross-boundary resolved imports (EXTRACTED): 182

## Connections

- [EXTRACTED] depends_on community 7 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.
- [EXTRACTED] depends_on community 7 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports skills/lazyown_facts.py.
- [EXTRACTED] depends_on community 7 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 7 <-> 12 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 7 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/chain_synth.py.
- [EXTRACTED] depends_on community 7 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `core/config.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` be broken with an interface?
- What would break if the most connected file in modules: chain_runner changed?
- Should modules: chain_runner be split, given cohesion 0.54?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/lazy_adaptive.py`
- `cli/retry_support.py`
- `modules/ad_gym.py`
- `modules/apt_playbooks.py`
- `modules/atomic_exploit_bridge.py`
- `modules/atomic_resolver.py`
- `modules/chain_approval.py`
- `modules/chain_distill.py`
- `modules/chain_facts.py`
- `modules/chain_loop.py`
- `modules/chain_registry.py`
- `modules/chain_runner.py`
- `modules/chain_state.py`
- `modules/chain_tokens.py`
- `modules/ctf_capture.py`
- `modules/emulation_runner.py`
- `modules/failure_verdict.py`
- `modules/gym_matrix_runner.py`
- *... and 44 more*
