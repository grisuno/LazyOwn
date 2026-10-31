# Second Brain

*Last synthesized: 2026-10-31 | 1309 files | 29 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `lazy_loop.py`, `utils.py`. Architecturally it is 6 layers, dominant utility (756 files) across 29 import-based communities. Recorded risk surface: 0 security findings and 125 dependency cycles.

Surprising tissue lives between modules: lazy_loop, cli/commands, modules: lazyown_mcp: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1309 |
| Symbols | 23889 |
| Resolved imports | 5610 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 29 |
| Doc coverage | 90% (1183/1309 files) |
| Security findings | 0 |
| Estimated read cost | ~916125 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 9: `lazyc2.py`, `lazy_loop.py`, `lazyown_mcp.py`, `mcp_generated_tools.py`, `3d-force-graph-1.73.4.min.js` (+4 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [modules: lazy_loop (184 files, cohesion 0.57)](./community_0_modules_lazy_loop.md)
- [cli/commands (158 files, cohesion 0.52)](./community_1_cli_commands.md)
- [modules: lazyown_mcp (158 files, cohesion 0.51)](./community_2_modules_lazyown_mcp.md)
- [cli (138 files, cohesion 0.58)](./community_3_cli.md)
- [modules: chain_runner (81 files, cohesion 0.50)](./community_4_modules_chain_runner.md)
- [lazyc2/security (55 files, cohesion 0.45)](./community_5_lazyc2_security.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_6_lazygui_panels.md)
- [static/js (49 files, cohesion 0.36)](./community_7_static_js.md)
- [modules: autonomous_daemon (42 files, cohesion 0.49)](./community_8_modules_autonomous_daemon.md)
- [modules: llm_budget (41 files, cohesion 0.43)](./community_9_modules_llm_budget.md)
- [skills/claude_md_orchestrator (23 files, cohesion 0.73)](./community_10_skills_claude_md_orchestrator.md)
- [modules: exploit_migrated (18 files, cohesion 0.39)](./community_11_modules_exploit_migrated.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_12_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_13_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_14_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_15_skills_hermes_lazyown.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [modules/guardrails (6 files, cohesion 0.62)](./community_17_modules_guardrails.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_18_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_19_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_20_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_21_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_22_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_23_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_24_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_25_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_26_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_27_tools.md)
- [orphans (241 files, cohesion 0.00)](./community_28_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 319.2 |
| `modules/lazy_loop.py` | 286.9 (large, maybe generated) |
| `utils.py` | 260.6 |
| `cli/commands/_base.py` | 216.7 |
| `modules/__init__.py` | 204.0 |

## Strongest Connections

- 3 -> 7: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)
- 4 -> 17: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 9: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 13 -> 1: depends_on (strength 0.9, EXTRACTED)
- 9 -> 3: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
