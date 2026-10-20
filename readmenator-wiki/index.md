# Second Brain

*Last synthesized: 2026-10-20 | 1124 files | 24 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (668 files) across 24 import-based communities. Recorded risk surface: 0 security findings and 77 dependency cycles.

Surprising tissue lives between cli/commands, modules: autonomous_daemon, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (89% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1124 |
| Symbols | 21004 |
| Resolved imports | 4758 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 24 |
| Doc coverage | 89% (995/1124 files) |
| Security findings | 0 |
| Estimated read cost | ~815053 tokens (chars/4, offline so $0) |
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

- [cli/commands (167 files, cohesion 0.54)](./community_0_cli_commands.md)
- [modules: autonomous_daemon (165 files, cohesion 0.56)](./community_1_modules_autonomous_daemon.md)
- [cli (113 files, cohesion 0.55)](./community_2_cli.md)
- [modules: lazy_loop (110 files, cohesion 0.58)](./community_3_modules_lazy_loop.md)
- [modules: lazyc2 (98 files, cohesion 0.50)](./community_4_modules_lazyc2.md)
- [static/js (56 files, cohesion 0.48)](./community_5_static_js.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_6_lazygui_panels.md)
- [modules: lazyown_facts (29 files, cohesion 0.52)](./community_7_modules_lazyown_facts.md)
- [modules: surface_graph (16 files, cohesion 0.50)](./community_8_modules_surface_graph.md)
- [modules: dashboard_engine (13 files, cohesion 0.39)](./community_9_modules_dashboard_engine.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.78)](./community_10_skills_claude_md_orchestrator.md)
- [skills/hermes-lazyown (12 files, cohesion 0.57)](./community_11_skills_hermes_lazyown.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_12_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_13_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_16_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_17_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_18_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_19_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_20_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_21_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_22_tools.md)
- [orphans (236 files, cohesion 0.00)](./community_23_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 289.2 |
| `utils.py` | 224.5 |
| `modules/lazy_loop.py` | 209.3 (large, maybe generated) |
| `skills/lazyown_mcp.py` | 200.6 (large, maybe generated) |
| `cli/commands/_base.py` | 188.7 |

## Strongest Connections

- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 1: depends_on (strength 0.9, EXTRACTED)
- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 5: depends_on (strength 0.9, EXTRACTED)
- 2 -> 3: depends_on (strength 0.9, EXTRACTED)
- 12 -> 0: depends_on (strength 0.9, EXTRACTED)
- 5 -> 1: depends_on (strength 0.9, EXTRACTED)
- 5 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
