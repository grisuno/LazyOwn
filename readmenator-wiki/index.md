# Second Brain

*Last synthesized: 2026-10-03 | 891 files | 27 concept pages | offline, zero tokens*

> Raw sources -> readmenator wiki -> links (Karpathy LLM Wiki Pattern, deterministic).
> Start here, then open one community page. Prefer grep over full reads.

## Vault Overview

The codebase centres on `logging.py`, `utils.py`, `_base.py`. Architecturally it is 6 layers, dominant utility (480 files) across 27 import-based communities. Recorded risk surface: 0 security findings and 26 dependency cycles.

Surprising tissue lives between cli/commands (community 0), tests (community 1), static/js: 20 extracted cross-community imports and 0 inferred bridges. Follow `connections.json` sorted by strength before refactoring.

Open work clusters around documentation (85% file coverage), 0 security findings, 20 taint paths, and 5 suggested exploration questions in `queries.md`.

## Stats

| Metric | Value |
|--------|-------|
| Files | 891 |
| Symbols | 17030 |
| Resolved imports | 3220 |
| Languages | asm, c, cpp, cs, h, js, lua, php, py, sh |
| Communities | 27 |
| Doc coverage | 85% (761/891 files) |
| Security findings | 0 |
| Estimated read cost | ~527796 tokens (chars/4, offline so $0) |
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

- [cli/commands (community 0) (176 files, cohesion 0.58)](./community_0_cli_commands.md)
- [tests (community 1) (122 files, cohesion 0.50)](./community_1_tests.md)
- [static/js (18 files, cohesion 0.54)](./community_2_static_js.md)
- [tests (community 3) (111 files, cohesion 0.54)](./community_3_tests.md)
- [cli (20 files, cohesion 0.45)](./community_4_cli.md)
- [cli/commands (community 5) (5 files, cohesion 0.31)](./community_5_cli_commands.md)
- [modules (community 6) (7 files, cohesion 0.88)](./community_6_modules.md)
- [modules (community 7) (7 files, cohesion 0.86)](./community_7_modules.md)
- [modules (community 8) (46 files, cohesion 0.47)](./community_8_modules.md)
- [modules (community 9) (6 files, cohesion 0.83)](./community_9_modules.md)
- [contrib/legacy (5 files, cohesion 0.80)](./community_10_contrib_legacy.md)
- [modules (community 11) (72 files, cohesion 0.45)](./community_11_modules.md)
- [tests (community 12) (2 files, cohesion 0.50)](./community_12_tests.md)
- [tests (community 13) (4 files, cohesion 0.75)](./community_13_tests.md)
- [lazygui/panels (36 files, cohesion 0.77)](./community_14_lazygui_panels.md)
- [lazygui/theme/palettes (7 files, cohesion 0.55)](./community_15_lazygui_theme_palettes.md)
- [modules/backdoor (2 files, cohesion 1.00)](./community_16_modules_backdoor.md)
- [poc_tui (community 17) (4 files, cohesion 0.60)](./community_17_poc_tui.md)
- [poc_tui (community 18) (2 files, cohesion 1.00)](./community_18_poc_tui.md)
- [scripts (community 19) (2 files, cohesion 1.00)](./community_19_scripts.md)
- [scripts (community 20) (3 files, cohesion 1.00)](./community_20_scripts.md)
- [scripts (community 21) (2 files, cohesion 1.00)](./community_21_scripts.md)
- [skills/claude_md_orchestrator (13 files, cohesion 0.85)](./community_22_skills_claude_md_orchestrator.md)
- [skills/hermes-lazyown (7 files, cohesion 0.85)](./community_23_skills_hermes_lazyown.md)
- [test (2 files, cohesion 1.00)](./community_24_test.md)
- [tools (2 files, cohesion 1.00)](./community_25_tools.md)
- [orphans (208 files, cohesion 0.00)](./community_26_orphans.md)

## God Nodes

| File | Score |
|------|-------|
| `core/logging.py` | 247.2 |
| `utils.py` | 190.1 |
| `cli/commands/_base.py` | 170.7 |
| `skills/lazyown_mcp.py` | 146.1 (large, maybe generated) |
| `lazyown.py` | 122.3 |

## Strongest Connections

- 1 -> 0: depends_on (strength 0.9, EXTRACTED)
- 2 -> 1: depends_on (strength 0.9, EXTRACTED)
- 3 -> 11: depends_on (strength 0.9, EXTRACTED)
- 3 -> 0: depends_on (strength 0.9, EXTRACTED)
- 3 -> 1: depends_on (strength 0.9, EXTRACTED)
- 0 -> 11: depends_on (strength 0.9, EXTRACTED)
- 4 -> 1: depends_on (strength 0.9, EXTRACTED)
- 6 -> 0: depends_on (strength 0.9, EXTRACTED)
- 0 -> 8: depends_on (strength 0.9, EXTRACTED)
- 7 -> 0: depends_on (strength 0.9, EXTRACTED)

## Navigation Tips

- Obsidian Graph View works: every community page links back here.
- `connections.json` is machine-readable for GraphRAG pipelines.
- `REPORT.md` states what was extracted vs inferred and current limits.
- Regenerate offline: `readmenator . --rebuild` (no network, no tokens).
