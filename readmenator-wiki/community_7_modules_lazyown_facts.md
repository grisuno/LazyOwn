# modules: lazyown_facts

*Community 7 | 63 files | cohesion 0.54*

## Definition

This community groups 63 file(s) rooted at `tests` with dominant language py (cohesion 0.54). Central symbols: `AccessFact`, `AdaptiveFallbackArbiter`, `Alternative`, `AptPlaybook`, `AptPlaybookEngine`, `AtomicResolver`, `AtomicTest`, `AtomicTestRef`. Core file: `skills/lazyown_facts.py` (79 symbols). Documented purpose: Parsing, printing and replanning support for the ``apt_chain`` CLI.  Keeps ``cli.commands.command_and_control_migrated`` thin: argument parsing, step selection,.

## Files

### `tests` (32 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_apt_chain_admin.py` | py | testing | 30 | yes |
| `tests/test_apt_chain_integration.py` | py | testing | 6 | yes |
| `tests/test_atomic_loop.py` | py | testing | 17 | yes |
| `tests/test_atomic_resolver.py` | py | testing | 9 | yes |
| `tests/test_chain_approval_c2.py` | py | testing | 27 | yes |
| `tests/test_chain_approval_cli_wiring.py` | py | testing | 2 | yes |
| `tests/test_chain_distill.py` | py | testing | 15 | yes |

### `modules` (24 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/apt_playbooks.py` | py | utility | 17 | yes |
| `modules/atomic_cli.py` | py | utility | 11 | yes |
| `modules/atomic_resolver.py` | py | utility | 27 | yes |
| `modules/chain_approval.py` | py | utility | 18 | yes |
| `modules/chain_distill.py` | py | utility | 23 | yes |
| `modules/chain_facts.py` | py | utility | 3 | yes |

### `cli` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/apt_chain_support.py` | py | utility | 29 | yes |
| `cli/retry_support.py` | py | utility | 10 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/command_and_control_migrated.py` | py | utility | 33 | yes |
| `cli/commands/lazy_adaptive.py` | py | utility | 4 | yes |

### `skills` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/lazyown_facts.py` | py | utility | 79 | yes |

### `skills/mcp_tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/ttp_chain.py` | py | utility | 1 | yes |

### `skills/tests` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_facts.py` | py | testing | 37 | yes |

*... and 43 more files in this community.*


## Key Symbols

- `_apply_limit` (function, `cli/apt_chain_support.py:46`) `def _apply_limit(args, value)` - Parse one ``--limit`` integer into the args, erroring loudly.
- `_parse_admin_flags` (function, `cli/apt_chain_support.py:54`) `def _parse_admin_flags(args, tokens)` - Split admin tokens into positionals, valued flags and plain flags.
- `_token_name_ok` (function, `cli/apt_chain_support.py:82`) `def _token_name_ok(name)` - True when a name matches the chain token grammar.
- `ChainArgs` (class, `cli/apt_chain_support.py:88`) `class ChainArgs` - Parsed ``apt_chain`` invocation.
- `parse_chain_args` (function, `cli/apt_chain_support.py:114`) `def parse_chain_args(line)` - Parse one ``apt_chain`` command line into structured args.
- `_set_value` (function, `cli/apt_chain_support.py:180`) `def _set_value(args, flag, value)` - Assign one valued option onto the args struct.
- `_synth_from_playbook` (function, `cli/apt_chain_support.py:205`) `def _synth_from_playbook(playbook, target)` - Lower one named APT playbook into a written chain; admin payload.
- `resolve_invocation` (function, `cli/apt_chain_support.py:234`) `def resolve_invocation(positionals, target_seed, preset_target, playbook_engine,` - Classify positional tokens into chain, target and playbook override.
- `chain_file_exists` (function, `cli/apt_chain_support.py:275`) `def chain_file_exists(name)` - True when chains/<name>.yaml exists, even if disabled.
- `resolve_admin` (function, `cli/apt_chain_support.py:322`) `def resolve_admin(args)` - Execute an admin action against the registry and checkpoint store.
- `select_step_ids` (function, `cli/apt_chain_support.py:457`) `def select_step_ids(chain, args)` - Resolve --step/--from-step/--to-step into one id set.
- `adversarial_continue` (function, `cli/apt_chain_support.py:489`) `def adversarial_continue(chain)` - Return a copy of the chain where every step continues on error.
- `render_result` (function, `cli/apt_chain_support.py:497`) `def render_result(result)` - Render one chain result as operator lines (JSON mode prints dict).
- `render_admin` (function, `cli/apt_chain_support.py:538`) `def render_admin(payload, action)` - Render an ``apt_chain`` admin payload as severity-tagged operator lines.
- `build_cli_approver` (function, `cli/apt_chain_support.py:616`) `def build_cli_approver(printer, input_fn)` - Return an approver baked for interactive operators.
- `approve` (function, `cli/apt_chain_support.py:624`) `def approve(step_id, command)`
- `_step_from_alternative` (function, `cli/apt_chain_support.py:638`) `def _step_from_alternative(alternative, outcome, target)` - Build one safe replan step from an adaptive fallback alternative.
- `_observed_conditions` (function, `cli/apt_chain_support.py:655`) `def _observed_conditions(target)` - Read observed services and credential evidence for one host.
- `build_adaptive_replanner` (function, `cli/apt_chain_support.py:676`) `def build_adaptive_replanner()` - Return a replanner driven by ``modules.lazy_fallback``.
- `replan` (function, `cli/apt_chain_support.py:689`) `def replan(context)`
- `compose_replanners` (function, `cli/apt_chain_support.py:714`) `def compose_replanners(replanners)` - Return one replanner running every non-None replanner in order.
- `composed` (function, `cli/apt_chain_support.py:727`) `def composed(context)`
- `build_reactive_replanner` (function, `cli/apt_chain_support.py:734`) `def build_reactive_replanner()` - Return a replanner driven by ``modules.reactive_engine``.
- `replan` (function, `cli/apt_chain_support.py:737`) `def replan(context)`
- `_decision_command` (function, `cli/apt_chain_support.py:759`) `def _decision_command(decision)` - Extract one actionable command from a reactive decision.
- `_step_from_decision` (function, `cli/apt_chain_support.py:768`) `def _step_from_decision(command, outcome, executed_count)` - Build one safe replan step from a suggested command.
- `_recent_changes_block` (function, `cli/apt_chain_support.py:790`) `def _recent_changes_block(target)` - Recent world changes on the target for one LLM recovery prompt.
- `build_llm_recovery_chain` (function, `cli/apt_chain_support.py:818`) `def build_llm_recovery_chain(result, target, task_id)` - Ask the LLM pool for a temporary recovery chain after a failed run.
- `_platform` (function, `cli/apt_chain_support.py:892`) `def _platform()` - Guess the loop platform from the payload configuration.
- `select_agent_flavour` (function, `cli/commands/command_and_control_migrated.py:43`) `def select_agent_flavour(run_tests, platform)` - Pick the agent script extension from the tests of the current run.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 200
- Cross-boundary resolved imports (EXTRACTED): 165

## Connections

- [EXTRACTED] depends_on community 7 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/auto_registry.py.
- [EXTRACTED] depends_on community 7 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/reactive_engine.py.
- [EXTRACTED] depends_on community 7 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/__init__.py.
- [EXTRACTED] depends_on community 7 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/guardrails/__init__.py.
- [EXTRACTED] depends_on community 7 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports cli/assign.py.
- [EXTRACTED] depends_on community 7 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/command_and_control_migrated.py imports core/config.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `core/config.py`
- [cycle] `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `cli/apt_chain_support.py` -> `modules/chain_family.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `cli/apt_chain_support.py` -> `modules/chain_family.py` -> `modules/lazy_loop.py`
- [cycle] `modules/lazy_loop.py` -> `modules/chain_loop.py` -> `cli/apt_chain_support.py` -> `modules/chain_family.py` -> `modules/lazy_loop.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`
- [cycle] `modules/atomic_exploit_bridge.py` -> `modules/emulation_runner.py` -> `modules/atomic_exploit_bridge.py`

## Open Questions

- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/chain_loop.py` be broken with an interface?
- What would break if the most connected file in modules: lazyown_facts changed?
- Should modules: lazyown_facts be split, given cohesion 0.54?

## Sources

- `cli/apt_chain_support.py`
- `cli/commands/command_and_control_migrated.py`
- `cli/commands/lazy_adaptive.py`
- `cli/retry_support.py`
- `modules/apt_playbooks.py`
- `modules/atomic_cli.py`
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
- `modules/emulation_runner.py`
- `modules/failure_verdict.py`
- `modules/gym_matrix_runner.py`
- `modules/lazy_deviations.py`
- *... and 43 more*
