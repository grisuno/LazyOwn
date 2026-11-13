# Second Brain

*Last synthesized: 2026-11-13 | 1622 files | 28 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `_context.py`, `lazy_loop.py`, `logging.py`. Architecturally it is 6 layers, dominant utility (981 files) across 28 import-based communities. Recorded risk surface: 0 security findings and 154 dependency cycles.

Surprising tissue lives between skills/mcp_tools, cli/commands, modules: lazyc2: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (91% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1622 |
| Symbols | 25639 |
| Resolved imports | 6386 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 28 |
| Doc coverage | 91% (1481/1622 files) |
| Security findings | 0 |
| Estimated read cost | ~994062 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 8: `lazyc2.py`, `lazy_loop.py`, `mcp_generated_tools.py`, `3d-force-graph-1.73.4.min.js`, `html2pdf.bundle.min.js` (+3 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [skills/mcp_tools (222 files, cohesion 0.60)](./community_0_skills_mcp_tools.md)
- [cli/commands (148 files, cohesion 0.46)](./community_1_cli_commands.md)
- [modules: lazyc2 (142 files, cohesion 0.47)](./community_2_modules_lazyc2.md)
- [modules: lazy_loop (138 files, cohesion 0.50)](./community_3_modules_lazy_loop.md)
- [cli (129 files, cohesion 0.56)](./community_4_cli.md)
- [modules: lazyown (104 files, cohesion 0.36)](./community_5_modules_lazyown.md)
- [modules: lazyown_facts (101 files, cohesion 0.61)](./community_6_modules_lazyown_facts.md)
- [modules: autonomous_exploit_engine (93 files, cohesion 0.45)](./community_7_modules_autonomous_exploit_engine.md)
- [modules: world_model (65 files, cohesion 0.39)](./community_8_modules_world_model.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_9_lazygui_panels.md)
- [modules: bof_registry (48 files, cohesion 0.47)](./community_10_modules_bof_registry.md)
- [modules: llm_budget (46 files, cohesion 0.44)](./community_11_modules_llm_budget.md)
- [skills/claude_md_orchestrator (30 files, cohesion 0.68)](./community_12_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_13_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_14_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_15_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_16_modules_polymorphic_engine.md)
- [tests (4 files, cohesion 1.00)](./community_17_tests.md)
- [modules: memory_store (3 files, cohesion 1.00)](./community_18_modules_memory_store.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_19_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_20_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_21_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_22_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_23_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_24_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_25_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_26_tools.md)
- [orphans (250 files, cohesion 0.00)](./community_27_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `skills/mcp_tools/_context.py` | 380.1 |
| `modules/lazy_loop.py` | 347.8 (large, maybe generated) |
| `core/logging.py` | 335.2 |
| `modules/__init__.py` | 296.0 |
| `utils.py` | 268.6 |

## Strongest Connections

- 4 -> 5: depends_on (strength 0.9, EXTRACTED)
- 6 -> 10: depends_on (strength 0.9, EXTRACTED)
- 6 -> 3: depends_on (strength 0.9, EXTRACTED)
- 6 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 1: depends_on (strength 0.9, EXTRACTED)
- 5 -> 2: depends_on (strength 0.9, EXTRACTED)
- 1 -> 11: depends_on (strength 0.9, EXTRACTED)
- 1 -> 7: depends_on (strength 0.9, EXTRACTED)
- 1 -> 5: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
