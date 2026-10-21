# Second Brain

*Last synthesized: 2026-10-20 | 1134 files | 25 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (671 files) across 25 import-based communities. Recorded risk surface: 0 security findings and 56 dependency cycles.

Surprising tissue lives between modules: autonomous_daemon, cli/commands: utils, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (89% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1134 |
| Symbols | 21312 |
| Resolved imports | 4773 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 25 |
| Doc coverage | 89% (1005/1134 files) |
| Security findings | 0 |
| Estimated read cost | ~820775 tokens (chars/4, offline so $0) |
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

- [modules: autonomous_daemon (164 files, cohesion 0.58)](./community_0_modules_autonomous_daemon.md)
- [cli/commands: utils (146 files, cohesion 0.53)](./community_1_cli_commands_utils.md)
- [modules: lazy_loop (115 files, cohesion 0.58)](./community_2_modules_lazy_loop.md)
- [cli (109 files, cohesion 0.56)](./community_3_cli.md)
- [modules: lazyc2 (96 files, cohesion 0.50)](./community_4_modules_lazyc2.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [static/js (39 files, cohesion 0.40)](./community_6_static_js.md)
- [modules: lazyown_facts (32 files, cohesion 0.53)](./community_7_modules_lazyown_facts.md)
- [cli/commands: c2_profile_engine (26 files, cohesion 0.41)](./community_8_cli_commands_c2_profile_engine.md)
- [core (22 files, cohesion 0.43)](./community_9_core.md)
- [skills/claude_md_orchestrator (19 files, cohesion 0.75)](./community_10_skills_claude_md_orchestrator.md)
- [modules: surface_graph (16 files, cohesion 0.50)](./community_11_modules_surface_graph.md)
- [skills/hermes-lazyown (13 files, cohesion 0.44)](./community_12_skills_hermes_lazyown.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_13_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_14_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_15_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_16_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_17_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_18_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_19_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_20_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_21_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_22_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_23_tools.md)
- [orphans (241 files, cohesion 0.00)](./community_24_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 289.2 |
| `utils.py` | 224.5 |
| `modules/lazy_loop.py` | 213.6 (large, maybe generated) |
| `skills/lazyown_mcp.py` | 200.6 (large, maybe generated) |
| `cli/commands/_base.py` | 188.7 |

## Strongest Connections

- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 2: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)
- 7 -> 2: depends_on (strength 0.9, EXTRACTED)
- 6 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 3: depends_on (strength 0.9, EXTRACTED)
- 1 -> 9: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 13 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
