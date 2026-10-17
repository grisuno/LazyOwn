# Second Brain

*Last synthesized: 2026-10-17 | 1078 files | 23 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazyown_mcp.py`. Architecturally it is 6 layers, dominant utility (647 files) across 23 import-based communities. Recorded risk surface: 0 security findings and 72 dependency cycles.

Surprising tissue lives between cli/commands, modules: lazyc2, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (88% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1078 |
| Symbols | 20469 |
| Resolved imports | 4517 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 23 |
| Doc coverage | 88% (949/1078 files) |
| Security findings | 0 |
| Estimated read cost | ~792585 tokens (chars/4, offline so $0) |
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

- [cli/commands (159 files, cohesion 0.54)](./community_0_cli_commands.md)
- [modules: lazyc2 (135 files, cohesion 0.52)](./community_1_modules_lazyc2.md)
- [modules: lazy_loop (115 files, cohesion 0.58)](./community_2_modules_lazy_loop.md)
- [cli (112 files, cohesion 0.54)](./community_3_cli.md)
- [modules: autonomous_daemon (109 files, cohesion 0.50)](./community_4_modules_autonomous_daemon.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [modules: llm_budget (35 files, cohesion 0.43)](./community_6_modules_llm_budget.md)
- [static/js (25 files, cohesion 0.49)](./community_7_static_js.md)
- [skills/claude_md_orchestrator (19 files, cohesion 0.75)](./community_8_skills_claude_md_orchestrator.md)
- [skills/hermes-lazyown (16 files, cohesion 0.57)](./community_9_skills_hermes_lazyown.md)
- [modules: surface_graph (15 files, cohesion 0.50)](./community_10_modules_surface_graph.md)
- [modules: opsec_scorer (12 files, cohesion 0.46)](./community_11_modules_opsec_scorer.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_12_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_13_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_16_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_17_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_18_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_19_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_20_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_21_tools.md)
- [orphans (234 files, cohesion 0.00)](./community_22_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 279.2 |
| `utils.py` | 216.4 |
| `skills/lazyown_mcp.py` | 194.2 (large, maybe generated) |
| `cli/commands/_base.py` | 184.7 |
| `modules/lazy_loop.py` | 182.0 (large, maybe generated) |

## Strongest Connections

- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 6: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 6: depends_on (strength 0.9, EXTRACTED)
- 0 -> 2: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 12 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 3: depends_on (strength 0.9, EXTRACTED)
- 6 -> 4: depends_on (strength 0.9, EXTRACTED)
- 1 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
