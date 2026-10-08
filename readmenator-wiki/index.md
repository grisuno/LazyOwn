# Second Brain

*Last synthesized: 2026-10-08 | 896 files | 23 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (563 files) across 23 import-based communities. Recorded risk surface: 0 security findings and 21 dependency cycles.

Surprising tissue lives between modules: autonomous_daemon, cli/commands, cli: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (85% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 896 |
| Symbols | 17095 |
| Resolved imports | 3202 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 23 |
| Doc coverage | 85% (766/896 files) |
| Security findings | 0 |
| Estimated read cost | ~530241 tokens (chars/4, offline so $0) |
| Large files (>256KB, maybe generated) | 7: `lazyc2.py`, `lazyown_mcp.py`, `mcp_generated_tools.py`, `html2pdf.bundle.min.js`, `vis-network-9.1.2.min.js` (+2 more) |

## Reading Order

1. Skim Stats and God Nodes below for blast radius.
2. Open the largest community page first, then follow Connections.
3. Use `queries.md` for the next question; log the answer there.

```
grep -rn '<keyword>' index.md community_*.md
readmenator query "<question>" --target LazyOwn
```

## Concept Wiki

- [modules: autonomous_daemon (142 files, cohesion 0.65)](./community_0_modules_autonomous_daemon.md)
- [cli/commands (136 files, cohesion 0.59)](./community_1_cli_commands.md)
- [cli (89 files, cohesion 0.56)](./community_2_cli.md)
- [modules: lazyc2 (77 files, cohesion 0.53)](./community_3_modules_lazyc2.md)
- [modules: wizard (54 files, cohesion 0.47)](./community_4_modules_wizard.md)
- [lazygui/panels (54 files, cohesion 0.94)](./community_5_lazygui_panels.md)
- [modules: world_model (37 files, cohesion 0.44)](./community_6_modules_world_model.md)
- [static/js (22 files, cohesion 0.54)](./community_7_static_js.md)
- [skills/hermes-lazyown (17 files, cohesion 0.64)](./community_8_skills_hermes_lazyown.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.85)](./community_9_skills_claude_md_orchestrator.md)
- [modules: metrics (8 files, cohesion 0.36)](./community_10_modules_metrics.md)
- [modules: kerberos_core (7 files, cohesion 0.88)](./community_11_modules_kerberos_core.md)
- [modules: saas_attacks (7 files, cohesion 0.86)](./community_12_modules_saas_attacks.md)
- [modules: polymorphic_engine (6 files, cohesion 0.83)](./community_13_modules_polymorphic_engine.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_14_contrib_legacy.md)
- [scripts: journal (3 files, cohesion 1.00)](./community_15_scripts_journal.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_16_modules_backdoor.md)
- [poc_tui (2 files, cohesion 1.00)](./community_17_poc_tui.md)
- [scripts: check_contract_manifest (2 files, cohesion 1.00)](./community_18_scripts_check_contract_manifest.md)
- [scripts: migrate_lazyown (2 files, cohesion 1.00)](./community_19_scripts_migrate_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_20_test.md)
- [tools (2 files, cohesion 1.00)](./community_21_tools.md)
- [orphans (207 files, cohesion 0.00)](./community_22_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 247.2 |
| `utils.py` | 194.1 |
| `cli/commands/_base.py` | 172.7 |
| `skills/lazyown_mcp.py` | 150.5 (large, maybe generated) |
| `lazyc2.py` | 112.3 (large, maybe generated) |

## Strongest Connections

- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 1 -> 4: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 1 -> 3: depends_on (strength 0.9, EXTRACTED)
- 2 -> 0: depends_on (strength 0.9, EXTRACTED)
- 4 -> 2: depends_on (strength 0.9, EXTRACTED)
- 11 -> 1: depends_on (strength 0.9, EXTRACTED)
- 4 -> 6: depends_on (strength 0.9, EXTRACTED)
- 0 -> 1: depends_on (strength 0.9, EXTRACTED)
- 12 -> 1: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
