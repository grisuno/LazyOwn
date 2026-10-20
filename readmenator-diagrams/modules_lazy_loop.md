# modules: lazy_loop

modules: lazy_loop groups 111 files (py) around plausible_command, _sudo_unavailable, _is_ip_literal, _valid_nmap_port_spec, repair_worker_command. Container and Kubernetes attack command set.

```mermaid
graph LR
    cli["cli"]
    core["core"]
    lazyc2["lazyc2"]
    modules["modules"]
    tests["tests"]
    cli -- "calls into" --> core
    cli -- "calls into" --> modules
    core -- "calls into" --> modules
    lazyc2 -- "calls into" --> modules
    modules -- "calls into" --> cli
    modules -- "calls into" --> core
    modules -- "calls into" --> tests
    tests -- "calls into" --> cli
    tests -- "calls into" --> core
    tests -- "depends on" --> lazyc2
    tests -- "calls into" --> modules
```

## cli (4.1)

cli groups 10 files (py) around ContainerCommandSet, do_docker_enum, do_k8s_enum, do_container_escape, do_k8s_pods. Container and Kubernetes attack command set.

## core (4.2)

core groups 2 files (py) around is_autonomous, autonomous_mode, _guarded_input, _tty_fd, emit_restore_sequences. Autonomous-run mode for the loop engine.

## lazyc2 (4.3)

lazyc2 groups 1 files (py) around _error, _namespaced_path, _world_snapshot, _status_payload, status. Orchestrator REST + web panel for the LazyOwn C2 dashboard.

## modules (4.4)

modules groups 50 files (py) around plausible_command, _sudo_unavailable, _is_ip_literal, _valid_nmap_port_spec, repair_worker_command. Active Directory Certificate Services (AD CS) attack module.

## tests (4.5)

tests groups 48 files (py) around gate_env, test_gate_exact_and_fuzzy_match, test_gate_cidr_match, test_gate_task_allow_is_closed_whitelist, test_gate_blocks_asset_insert. Asset gate + un-nerfed outputs + IntelGraph CSP regression tests.

**Files**:

- cli/commands/containers.py
- cli/commands/exploit_migrated.py
- cli/commands/lazyloop.py
- cli/commands/lazyops.py
- cli/commands/redteam_gym.py
- cli/lazy_monitor.py
- cli/lazy_orchestrator.py
- cli/orchestrator_assets_tabs.py
- cli/session_brief.py
- cli/tui_forms.py
- core/autonomous.py
- core/terminal_guard.py
- lazyc2/blueprints/orchestrator.py
- modules/__init__.py
- modules/adcs_attacks.py
- modules/atomic_exploit_bridge.py
- modules/auto_registry.py
- modules/custom_tools.py
- modules/exploit_chain.py
- modules/gym_registry.py
- modules/jsonl_tail.py
- modules/kill_chain_viz.py
- modules/killchain.py
- modules/lazy_bridge.py
- modules/lazy_cli_bridge.py
- modules/lazy_engine.py
- modules/lazy_installer.py
- modules/lazy_intel.py
- modules/lazy_loop.py
- modules/lazy_mentions.py
- modules/lazy_orchestrator_feedback.py
- modules/lazy_proxy.py
- modules/lazy_roles.py
- modules/lazy_runner.py
- modules/lazy_sandbox.py
- modules/lazy_skill_mirror.py
- modules/lazy_skills.py
- modules/lazyk8s.py
- modules/loop_progress.py
- modules/loop_triggers.py
- modules/metasploitable_gym.py
- modules/notify.py
- modules/orchestrator_config.py
- modules/outcome_bus.py
- modules/playbook_admin.py
- modules/reaction_bridge.py
- modules/redteam_gym.py
- modules/selfupdate.py
- modules/sinks/attack_graph.py
- modules/sinks/c2_surfaces.py
- modules/sinks/intel_graph.py
- modules/sinks/killchain.py
- modules/sinks/objectives.py
- modules/sinks/routing.py
- modules/sinks/world_model.py
- modules/tools/__init__.py
- modules/tools/loop_smoke.py
- modules/tools/monitor_smoke.py
- modules/traffic_recorder.py
- modules/trigger_policy.py
- modules/verb_catalog.py
- modules/workspace.py
- modules/world_model.py
- tests/test_asset_gate.py
- tests/test_auto_registry.py
- tests/test_chain_list_command.py
- tests/test_gym_cli.py
- tests/test_gym_ms2_cli.py
- tests/test_gym_registry.py
- tests/test_killchain_snapshot.py
- tests/test_killchain_unified_v2.py
- tests/test_lazy_agent.py
- tests/test_lazy_bridge_traffic.py
- tests/test_lazy_engine.py
- tests/test_lazy_evidence.py
- tests/test_lazy_loop.py
- tests/test_lazy_orchestrator.py
- tests/test_lazy_proxy.py
- tests/test_lazy_runner.py
- tests/test_lazy_worker_safety.py
- tests/test_loop_auto_orchestrator.py
- tests/test_loop_broadcast.py
- tests/test_loop_budget.py
- tests/test_loop_cli_catalog.py
- tests/test_loop_cold_overview.py
- tests/test_loop_force_graph.py
- tests/test_loop_guard_audit.py
- tests/test_loop_intent_delete.py
- tests/test_loop_mentions.py
- tests/test_loop_nmap_guard.py
- tests/test_loop_progress.py
- tests/test_loop_scope_traffic_evidence.py
- tests/test_loop_spawn_side.py
- tests/test_loop_store_race.py
- tests/test_loop_supervision.py
- tests/test_loop_worker_traces.py
- tests/test_metasploitable_gym.py
- tests/test_orchestrator_api.py
- tests/test_orchestrator_triggers.py
- tests/test_orchestrator_yaml.py
- tests/test_outcome_bus.py
- tests/test_pi_leg.py
- tests/test_playbook_admin.py
- tests/test_reaction_bridge.py
- tests/test_security_codeql_batch.py
- tests/test_session_brief.py
- tests/test_trigger_policy.py
- tests/test_ttpscope_bridge.py
- tests/test_unified_bridge_delegate.py
- tests/test_verb_catalog.py
- tests/test_world_model_extended.py
