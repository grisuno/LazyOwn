# modules: lazyown_facts

modules: lazyown_facts groups 29 files (py) around CommandInjectionError, UrlValidationError, needs_shell, safe_system, safe_run_argv. Parsing, printing and replanning support for the ``apt_chain`` CLI.

```mermaid
graph LR
    cli["cli"]
    core["core"]
    modules["modules"]
    skills["skills"]
    tests["tests"]
    cli -- "calls into" --> modules
    modules -- "depends on" --> core
    modules -- "calls into" --> skills
    modules -- "calls into" --> tests
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "calls into" --> modules
    tests -- "calls into" --> skills
```

## cli (8.1)

cli groups 2 files (py) around CommandAndControlMigratedCommandSet, do_msf, do_c2, do_listener, _api. Parsing, printing and replanning support for the ``apt_chain`` CLI.

## core (8.2)

core groups 1 files (py) around CommandInjectionError, UrlValidationError, needs_shell, safe_system, safe_run_argv. Centralized safe command execution for the LazyOwn framework.

## modules (8.3)

modules groups 11 files (py) around ChainStep, identifier, Chain, resolve, _render. APT Playbook Engine — map public APT reports to executable Atomic Red Team chains.

## skills (8.4)

skills groups 2 files (py) around Config, default, ServiceFact, CredentialFact, ShareFact. LazyOwn FactStore

## tests (8.5)

tests groups 13 files (py) around _make_shell, _Set, _Shell, __init__, _write_chain. apt_chain admin & run options BDD contract.

**Files**:

- cli/apt_chain_support.py
- cli/commands/command_and_control_migrated.py
- core/safe_exec.py
- modules/apt_playbooks.py
- modules/atomic_cli.py
- modules/atomic_resolver.py
- modules/chain_registry.py
- modules/chain_runner.py
- modules/chain_state.py
- modules/chain_synth.py
- modules/chain_tokens.py
- modules/command_executor.py
- modules/emulation_runner.py
- modules/metasploitable_migrations.py
- skills/lazyown_facts.py
- skills/tests/test_facts.py
- tests/test_apt_chain_admin.py
- tests/test_apt_chain_integration.py
- tests/test_atomic_exploit_bridge.py
- tests/test_atomic_loop.py
- tests/test_atomic_resolver.py
- tests/test_chain_registry.py
- tests/test_chain_runner.py
- tests/test_chain_synth.py
- tests/test_chain_v24_core.py
- tests/test_emulation_runner.py
- tests/test_executor_kernel.py
- tests/test_metasploitable_migrations.py
- tests/test_security_hardening_v4.py
