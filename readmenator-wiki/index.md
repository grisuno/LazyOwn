# Second Brain

*Last synthesized: 2026-10-27 | 1202 files | 26 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (708 files) across 26 import-based communities. Recorded risk surface: 0 security findings and 113 dependency cycles.

Surprising tissue lives between modules: lazyown_mcp, cli/commands, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (90% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1202 |
| Symbols | 22632 |
| Resolved imports | 5228 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 26 |
| Doc coverage | 90% (1076/1202 files) |
| Security findings | 0 |
| Estimated read cost | ~866803 tokens (chars/4, offline so $0) |
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

- [modules: lazyown_mcp (137 files, cohesion 0.52)](./community_0_modules_lazyown_mcp.md)
- [cli/commands (128 files, cohesion 0.50)](./community_1_cli_commands.md)
- [cli (111 files, cohesion 0.53)](./community_2_cli.md)
- [modules: lazy_loop (108 files, cohesion 0.58)](./community_3_modules_lazy_loop.md)
- [modules: lazyown_facts (75 files, cohesion 0.49)](./community_4_modules_lazyown_facts.md)
- [modules: lazyc2 (75 files, cohesion 0.49)](./community_5_modules_lazyc2.md)
- [modules: html2pdf.bundle.min (73 files, cohesion 0.40)](./community_6_modules_html2pdf_bundle_min.md)
- [modules: world_model (60 files, cohesion 0.38)](./community_7_modules_world_model.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_8_lazygui_panels.md)
- [modules: llm_budget (36 files, cohesion 0.46)](./community_9_modules_llm_budget.md)
- [modules/guardrails (32 files, cohesion 0.46)](./community_10_modules_guardrails.md)
- [skills/claude_md_orchestrator (19 files, cohesion 0.75)](./community_11_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_12_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_13_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_14_modules_saas_attacks.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_15_skills_hermes_lazyown.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_17_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_18_tests.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_19_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_20_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_21_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_22_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_23_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_24_tools.md)
- [orphans (237 files, cohesion 0.00)](./community_25_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 317.2 |
| `utils.py` | 240.6 |
| `modules/lazy_loop.py` | 234.6 (large, maybe generated) |
| `skills/lazyown_mcp.py` | 203.5 (large, maybe generated) |
| `cli/commands/_base.py` | 196.7 |

## Strongest Connections

- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 6: depends_on (strength 0.9, EXTRACTED)
- 4 -> 3: depends_on (strength 0.9, EXTRACTED)
- 4 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 10: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 2 -> 9: depends_on (strength 0.9, EXTRACTED)
- 2 -> 4: depends_on (strength 0.9, EXTRACTED)
- 7 -> 2: depends_on (strength 0.9, EXTRACTED)
- 13 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
