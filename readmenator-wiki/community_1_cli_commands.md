# cli/commands

*Community 1 | 137 files | cohesion 0.50*

## Definition

This community groups 137 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.50). Central symbols: `AddonUpdateResult`, `AiCommandSet`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `AutoFireCommandSet`, `BannerConfig`, `BannerConfigurator`, `BannerRenderer`. Core file: `utils.py` (126 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: AGPL v3  Descripción: Este archivo contiene l.

## Files

### `cli/commands` (72 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/ai.py` | py | utility | 8 | yes |
| `cli/commands/anti_forensics.py` | py | utility | 7 | yes |
| `cli/commands/applocker_bypass.py` | py | utility | 9 | yes |

### `tests` (25 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_updater.py` | py | testing | 13 | yes |
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_banner_config.py` | py | testing | 45 | yes |
| `tests/test_bdd_infra_range_report.py` | py | testing | 5 | yes |

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/addon_updater.py` | py | utility | 10 | yes |
| `modules/beacon_config_builder.py` | py | infrastructure | 14 | yes |
| `modules/bitm_engine.py` | py | utility | 18 | yes |

### `cli` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/banner_config.py` | py | infrastructure | 120 | yes |
| `cli/config_history.py` | py | infrastructure | 9 | yes |
| `cli/confirm.py` | py | utility | 2 | yes |

### `core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/defaults.py` | py | utility | 8 | yes |
| `core/safe_import.py` | py | utility | 4 | yes |
| `core/validators.py` | py | utility | 8 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 126 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazysmbrelay.py` | py | utility | 7 | no |

*... and 117 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:26`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:50`) `def list_png_files()`
- `main` (function, `banner.py:60`) `def main()`
- `BannerConfig` (class, `cli/banner_config.py:59`) `class BannerConfig` - Centralised constants for the banner renderer and configurator.
- `ColorRegistry` (class, `cli/banner_config.py:143`) `class ColorRegistry` - Named ANSI colors operators can assign to any segment.
- `names` (method, `cli/banner_config.py:170`) `def names(self)`
- `has` (method, `cli/banner_config.py:173`) `def has(self, name)`
- `resolve` (method, `cli/banner_config.py:176`) `def resolve(self, name)`
- `cycle` (method, `cli/banner_config.py:179`) `def cycle(self, current, direction)`
- `default_name` (method, `cli/banner_config.py:187`) `def default_name(self)`
- `GlyphRegistry` (class, `cli/banner_config.py:191`) `class GlyphRegistry` - Glyph slots used by the Neon Box renderer with cyclable choices.
- `slots` (method, `cli/banner_config.py:212`) `def slots(self)`
- `choices` (method, `cli/banner_config.py:215`) `def choices(self, slot)`
- `has` (method, `cli/banner_config.py:218`) `def has(self, slot)`
- `default` (method, `cli/banner_config.py:221`) `def default(self, slot)`
- `cycle` (method, `cli/banner_config.py:225`) `def cycle(self, slot, current, direction)`
- `SegmentSpec` (class, `cli/banner_config.py:237`) `class SegmentSpec` - Metadata describing a prompt segment available for toggling.
- `ColorPalette` (class, `cli/banner_config.py:250`) `class ColorPalette` - ANSI escape codes for the box chrome itself.
- `RenderContext` (class, `cli/banner_config.py:268`) `class RenderContext` - Pre-resolved data delivered to every :class:`SegmentRenderer`.
- `_bracketed` (function, `cli/banner_config.py:293`) `def _bracketed(label, value, bullet, value_color, ctx, glyphs)` - Render one bracketed top-row segment with the chosen value color.
- `_middle` (function, `cli/banner_config.py:307`) `def _middle(label, value, value_color, ctx, glyphs)` - Render one middle-row segment with the chosen value color.
- `SegmentRenderer` (class, `cli/banner_config.py:314`) `class SegmentRenderer(ABC)` - Contract for a single prompt segment.
- `spec` (method, `cli/banner_config.py:319`) `def spec(self)`
- `render` (method, `cli/banner_config.py:322`) `def render(self, ctx, cfg, color, glyphs)`
- `UserHostSegment` (class, `cli/banner_config.py:325`) `class UserHostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:336`) `def render(self, ctx, cfg, color, glyphs)`
- `IfaceSegment` (class, `cli/banner_config.py:340`) `class IfaceSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:351`) `def render(self, ctx, cfg, color, glyphs)`
- `LhostSegment` (class, `cli/banner_config.py:359`) `class LhostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:370`) `def render(self, ctx, cfg, color, glyphs)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 329
- Cross-boundary resolved imports (EXTRACTED): 323

## Connections

- [EXTRACTED] depends_on community 1 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 1 <-> 5 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports cli/engagement_hooks.py.
- [EXTRACTED] depends_on community 3 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/command_form.py imports cli/commands/containers.py.
- [EXTRACTED] depends_on community 15 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/sidequestion.py.
- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/c2_session.py imports modules/c2_agent.py.
- [EXTRACTED] depends_on community 16 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/param_registry.py` via `subprocess` (4 hops)

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `contrib/legacy/lazysmbrelay.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.50?

## Sources

- `banner.py`
- `cli/banner_config.py`
- `cli/commands/_base.py`
- `cli/commands/ai.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/bitm.py`
- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/c2_session.py`
- `cli/commands/caldera.py`
- `cli/commands/campaign.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cli_auth.py`
- `cli/commands/cloud.py`
- `cli/commands/collaboration.py`
- `cli/commands/command_and_control.py`
- `cli/commands/containers.py`
- `cli/commands/cred.py`
- *... and 117 more*
