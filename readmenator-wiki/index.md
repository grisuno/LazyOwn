# Second Brain

*Last synthesized: 2026-10-30 | 1266 files | 29 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `lazy_loop.py`, `utils.py`. Architecturally it is 6 layers, dominant utility (732 files) across 29 import-based communities. Recorded risk surface: 0 security findings and 120 dependency cycles.

Surprising tissue lives between modules: autonomous_daemon, cli/commands, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1266 |
| Symbols | 23416 |
| Resolved imports | 5418 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 29 |
| Doc coverage | 90% (1140/1266 files) |
| Security findings | 0 |
| Estimated read cost | ~896814 tokens (chars/4, offline so $0) |
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

- [modules: autonomous_daemon (158 files, cohesion 0.53)](./community_0_modules_autonomous_daemon.md)
- [cli/commands (135 files, cohesion 0.49)](./community_1_cli_commands.md)
- [cli (115 files, cohesion 0.54)](./community_2_cli.md)
- [modules: world_model (113 files, cohesion 0.45)](./community_3_modules_world_model.md)
- [modules: lazy_loop (109 files, cohesion 0.52)](./community_4_modules_lazy_loop.md)
- [modules: lazyc2 (76 files, cohesion 0.48)](./community_5_modules_lazyc2.md)
- [static/js (64 files, cohesion 0.40)](./community_6_static_js.md)
- [modules: lazyown_facts (59 files, cohesion 0.51)](./community_7_modules_lazyown_facts.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_8_lazygui_panels.md)
- [modules/guardrails (32 files, cohesion 0.46)](./community_9_modules_guardrails.md)
- [core (22 files, cohesion 0.40)](./community_10_core.md)
- [skills/claude_md_orchestrator (19 files, cohesion 0.75)](./community_11_skills_claude_md_orchestrator.md)
- [modules: exploit_migrated (8 files, cohesion 0.33)](./community_12_modules_exploit_migrated.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_13_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_14_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_15_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_16_skills_hermes_lazyown.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_17_modules_polymorphic_engine.md)
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
| `modules/lazy_loop.py` | 271.8 (large, maybe generated) |
| `utils.py` | 250.6 |
| `cli/commands/_base.py` | 206.7 |
| `skills/lazyown_mcp.py` | 177.1 (large, maybe generated) |

## Strongest Connections

- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 6: depends_on (strength 0.9, EXTRACTED)
- 7 -> 4: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 3: depends_on (strength 0.9, EXTRACTED)
- 7 -> 9: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 10: depends_on (strength 0.9, EXTRACTED)
- 1 -> 7: depends_on (strength 0.9, EXTRACTED)
- 2 -> 3: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
