# modules: chain_runner

modules: chain_runner groups 40 files (py) around ChainStep, identifier, Chain, resolve, _render. Parsing, printing and replanning support for the ``apt_chain`` CLI.

```mermaid
graph LR
    cli["cli"]
    modules["modules"]
    tests["tests"]
    cli -- "calls into" --> modules
    modules -- "calls into" --> tests
    tests -- "calls into" --> cli
    tests -- "calls into" --> modules
```

## cli (8.1)

cli groups 4 files (py) around select_agent_flavour, CommandAndControlMigratedCommandSet, do_msf, do_c2, do_listener. Parsing, printing and replanning support for the ``apt_chain`` CLI.

## modules (8.2)

modules groups 20 files (py) around ChainStep, identifier, Chain, resolve, _render. APT Playbook Engine — map public APT reports to executable Atomic Red Team chains.

## tests (8.3)

tests groups 16 files (py) around _make_shell, _Set, _Shell, __init__, _write_chain. apt_chain admin & run options BDD contract.

**Files**:

- cli/apt_chain_support.py
- cli/commands/command_and_control_migrated.py
- cli/commands/retry_ops.py
- cli/retry_support.py
- modules/apt_playbooks.py
- modules/atomic_cli.py
- modules/atomic_resolver.py
- modules/chain_distill.py
- modules/chain_facts.py
- modules/chain_registry.py
- modules/chain_runner.py
- modules/chain_state.py
- modules/chain_synth.py
- modules/emulation_runner.py
- modules/guardrails/__init__.py
- modules/guardrails/advisories.py
- modules/guardrails/budget.py
- modules/guardrails/checkpoints.py
- modules/guardrails/contracts.py
- modules/guardrails/harness.py
- modules/gym_matrix_runner.py
- modules/listener_manager.py
- modules/retry_session.py
- modules/verb_manifest.py
- tests/test_apt_chain_admin.py
- tests/test_apt_chain_integration.py
- tests/test_atomic_loop.py
- tests/test_atomic_resolver.py
- tests/test_chain_distill.py
- tests/test_chain_parallel_fallback.py
- tests/test_chain_registry.py
- tests/test_chain_runner.py
- tests/test_chain_synth.py
- tests/test_chain_v24_core.py
- tests/test_codeql_alert_fixes.py
- tests/test_command_control_agent.py
- tests/test_emulation_runner.py
- tests/test_f4_hardening.py
- tests/test_retry_session.py
- tests/test_verb_manifest.py
