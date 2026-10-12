# Second Brain

*Last synthesized: 2026-10-12 | 1000 files | 24 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (609 files) across 24 import-based communities. Recorded risk surface: 0 security findings and 29 dependency cycles.

Surprising tissue lives between modules: lazyc2, cli/commands, modules: autonomous_daemon: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (87% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1000 |
| Symbols | 19405 |
| Resolved imports | 4073 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 24 |
| Doc coverage | 87% (873/1000 files) |
| Security findings | 0 |
| Estimated read cost | ~752838 tokens (chars/4, offline so $0) |
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

- [modules: lazyc2 (146 files, cohesion 0.52)](./community_0_modules_lazyc2.md)
- [cli/commands (137 files, cohesion 0.57)](./community_1_cli_commands.md)
- [modules: autonomous_daemon (116 files, cohesion 0.53)](./community_2_modules_autonomous_daemon.md)
- [cli: status_bar (101 files, cohesion 0.53)](./community_3_cli_status_bar.md)
- [modules: lazy_loop (79 files, cohesion 0.58)](./community_4_modules_lazy_loop.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [cli: banner_config (40 files, cohesion 0.51)](./community_6_cli_banner_config.md)
- [static/js (26 files, cohesion 0.52)](./community_7_static_js.md)
- [skills/claude_md_orchestrator (17 files, cohesion 0.80)](./community_8_skills_claude_md_orchestrator.md)
- [modules: surface_graph (15 files, cohesion 0.53)](./community_9_modules_surface_graph.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_10_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_11_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_12_skills_hermes_lazyown.md)
- [modules: network_opsec (6 files, cohesion 0.71)](./community_13_modules_network_opsec.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_16_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_17_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_18_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_19_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_20_scripts_migrate_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_21_test.md)
- [tools (2 files, cohesion 1.00)](./community_22_tools.md)
- [orphans (216 files, cohesion 0.00)](./community_23_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 243.2 |
| `utils.py` | 210.4 |
| `cli/commands/_base.py` | 182.7 |
| `skills/lazyown_mcp.py` | 179.8 (large, maybe generated) |
| `modules/lazy_loop.py` | 152.0 (large, maybe generated) |

## Strongest Connections

- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 7 -> 4: depends_on (strength 0.9, EXTRACTED)
- 0 -> 3: depends_on (strength 0.9, EXTRACTED)
- 0 -> 6: depends_on (strength 0.9, EXTRACTED)
- 10 -> 1: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: depends_on (strength 0.9, EXTRACTED)
- 2 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
