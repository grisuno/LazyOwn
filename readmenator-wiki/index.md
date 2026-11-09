# Second Brain

*Last synthesized: 2026-11-09 | 1526 files | 31 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `_context.py`, `logging.py`, `lazy_loop.py`. Architecturally it is 6 layers, dominant utility (937 files) across 31 import-based communities. Recorded risk surface: 0 security findings and 118 dependency cycles.

Surprising tissue lives between skills/mcp_tools, cli/commands, modules: lazyc2: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (91% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 1526 |
| Symbols | 24470 |
| Resolved imports | 6016 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 31 |
| Doc coverage | 91% (1388/1526 files) |
| Security findings | 0 |
| Estimated read cost | ~941213 tokens (chars/4, offline so $0) |
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

- [skills/mcp_tools (222 files, cohesion 0.61)](./community_0_skills_mcp_tools.md)
- [cli/commands (166 files, cohesion 0.48)](./community_1_cli_commands.md)
- [modules: lazyc2 (141 files, cohesion 0.48)](./community_2_modules_lazyc2.md)
- [cli (114 files, cohesion 0.55)](./community_3_cli.md)
- [modules: lazy_loop (110 files, cohesion 0.46)](./community_4_modules_lazy_loop.md)
- [modules: lazyown (109 files, cohesion 0.35)](./community_5_modules_lazyown.md)
- [modules: chain_runner (90 files, cohesion 0.60)](./community_6_modules_chain_runner.md)
- [modules: atomic_exploit_bridge (73 files, cohesion 0.45)](./community_7_modules_atomic_exploit_bridge.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_8_lazygui_panels.md)
- [static/js (49 files, cohesion 0.47)](./community_9_static_js.md)
- [modules: llm_budget (37 files, cohesion 0.43)](./community_10_modules_llm_budget.md)
- [modules/guardrails (22 files, cohesion 0.40)](./community_11_modules_guardrails.md)
- [modules: dashboard_engine (17 files, cohesion 0.44)](./community_12_modules_dashboard_engine.md)
- [skills/claude_md_orchestrator (14 files, cohesion 0.68)](./community_13_skills_claude_md_orchestrator.md)
- [modules: defense_eval (8 files, cohesion 0.64)](./community_14_modules_defense_eval.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_15_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_16_modules_saas_attacks.md)
- [modules: network_opsec (6 files, cohesion 0.71)](./community_17_modules_network_opsec.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_18_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_19_contrib_legacy.md)
- [tests (4 files, cohesion 1.00)](./community_20_tests.md)
- [modules: memory_store (3 files, cohesion 1.00)](./community_21_modules_memory_store.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_22_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_23_modules_backdoor.md)
- [modules: lazy_netattack (2 files, cohesion 1.00)](./community_24_modules_lazy_netattack.md)
- [modules: lazy_triage (2 files, cohesion 1.00)](./community_25_modules_lazy_triage.md)
- [poc_tui (2 files, cohesion 1.00)](./community_26_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_27_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_28_scripts_migrate_lazyown.md)
- [tools (2 files, cohesion 1.00)](./community_29_tools.md)
- [orphans (245 files, cohesion 0.00)](./community_30_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `skills/mcp_tools/_context.py` | 352.1 |
| `core/logging.py` | 319.2 |
| `modules/lazy_loop.py` | 299.8 (large, maybe generated) |
| `utils.py` | 262.6 |
| `modules/__init__.py` | 260.0 |

## Strongest Connections

- 3 -> 5: depends_on (strength 0.9, EXTRACTED)
- 6 -> 4: depends_on (strength 0.9, EXTRACTED)
- 6 -> 0: depends_on (strength 0.9, EXTRACTED)
- 6 -> 1: depends_on (strength 0.9, EXTRACTED)
- 6 -> 11: depends_on (strength 0.9, EXTRACTED)
- 5 -> 2: depends_on (strength 0.9, EXTRACTED)
- 5 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 10: depends_on (strength 0.9, EXTRACTED)
- 3 -> 2: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
