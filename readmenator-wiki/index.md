# Second Brain

*Last synthesized: 2026-10-29 | 1227 files | 24 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (720 files) across 24 import-based communities. Recorded risk surface: 0 security findings and 113 dependency cycles.

Surprising tissue lives between modules: lazyown_mcp, cli/commands, modules: lazy_loop: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1227 |
| Symbols | 22940 |
| Resolved imports | 5282 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 24 |
| Doc coverage | 90% (1101/1227 files) |
| Security findings | 0 |
| Estimated read cost | ~875853 tokens (chars/4, offline so $0) |
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

- [modules: lazyown_mcp (156 files, cohesion 0.54)](./community_0_modules_lazyown_mcp.md)
- [cli/commands (151 files, cohesion 0.51)](./community_1_cli_commands.md)
- [modules: lazy_loop (127 files, cohesion 0.55)](./community_2_modules_lazy_loop.md)
- [modules: world_model (113 files, cohesion 0.46)](./community_3_modules_world_model.md)
- [cli (93 files, cohesion 0.50)](./community_4_cli.md)
- [modules: html2pdf.bundle.min (74 files, cohesion 0.42)](./community_5_modules_html2pdf_bundle_min.md)
- [lazyc2/security (59 files, cohesion 0.47)](./community_6_lazyc2_security.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_7_lazygui_panels.md)
- [modules: llm_budget (44 files, cohesion 0.44)](./community_8_modules_llm_budget.md)
- [modules: chain_runner (41 files, cohesion 0.55)](./community_9_modules_chain_runner.md)
- [skills/claude_md_orchestrator (23 files, cohesion 0.73)](./community_10_skills_claude_md_orchestrator.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_11_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_12_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_13_skills_hermes_lazyown.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_14_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_15_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_16_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_17_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_18_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_19_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_20_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_21_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_22_tools.md)
- [orphans (243 files, cohesion 0.00)](./community_23_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 317.2 |
| `utils.py` | 248.6 |
| `modules/lazy_loop.py` | 236.7 (large, maybe generated) |
| `cli/commands/_base.py` | 204.7 |
| `skills/lazyown_mcp.py` | 203.5 (large, maybe generated) |

## Strongest Connections

- 4 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 5: depends_on (strength 0.9, EXTRACTED)
- 9 -> 2: depends_on (strength 0.9, EXTRACTED)
- 9 -> 0: depends_on (strength 0.9, EXTRACTED)
- 9 -> 8: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 8: depends_on (strength 0.9, EXTRACTED)
- 1 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
