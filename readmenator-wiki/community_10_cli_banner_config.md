# cli: banner_config

*Community 10 | 19 files | cohesion 0.41*

## Definition

This community groups 19 file(s) rooted at `tests` with dominant language py (cohesion 0.41). Central symbols: `BannerConfig`, `BannerConfigurator`, `BannerRenderer`, `BannerSettings`, `BatteryLoadSegment`, `CliAuthCommandSet`, `ColorPalette`, `ColorRegistry`. Core file: `cli/banner_config.py` (120 symbols). Documented purpose: Configurable Neon Box banner for the LazyOwn interactive shell.  The module exposes a single, self-contained banner subsystem with three extension axes the oper.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/banner_config.py` | py | infrastructure | 120 | yes |
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |
| `cli/commands/redteam_gym.py` | py | utility | 8 | yes |
| `cli/commands/ux.py` | py | utility | 9 | yes |
| `cli/config_history.py` | py | infrastructure | 9 | yes |
| `cli/engagement_hooks.py` | py | utility | 32 | yes |
| `cli/fuzzy_match.py` | py | utility | 3 | yes |
| `cli/fuzzy_picker.py` | py | utility | 41 | yes |
| `cli/session_hud.py` | py | utility | 9 | yes |
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/redteam_gym.py` | py | utility | 18 | yes |
| `tests/test_banner_config.py` | py | testing | 45 | yes |
| `tests/test_cli_auth_remember.py` | py | testing | 7 | yes |
| `tests/test_engagement_and_ping.py` | py | testing | 40 | yes |
| `tests/test_engagement_command_gate.py` | py | testing | 18 | yes |
| `tests/test_engagement_elo_and_methodology.py` | py | testing | 43 | yes |
| `tests/test_fuzzy_picker.py` | py | testing | 25 | yes |
| `tests/test_prompt_readline_markers.py` | py | testing | 8 | yes |
| `tests/test_prompt_refresh.py` | py | testing | 9 | yes |

## Key Symbols

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
- `_bracketed` (method, `cli/banner_config.py:293`) `def _bracketed(label, value, bullet, value_color, ctx, glyphs)` - Render one bracketed top-row segment with the chosen value color.
- `_middle` (method, `cli/banner_config.py:307`) `def _middle(label, value, value_color, ctx, glyphs)` - Render one middle-row segment with the chosen value color.
- `SegmentRenderer` (class, `cli/banner_config.py:314`) `class SegmentRenderer(ABC)` - Contract for a single prompt segment.
- `spec` (method, `cli/banner_config.py:319`) `def spec(self)`
- `render` (method, `cli/banner_config.py:322`) `def render(self, ctx, cfg, color, glyphs)`
- `UserHostSegment` (class, `cli/banner_config.py:325`) `class UserHostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:336`) `def render(self, ctx, cfg, color, glyphs)`
- `IfaceSegment` (class, `cli/banner_config.py:340`) `class IfaceSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:351`) `def render(self, ctx, cfg, color, glyphs)`
- `LhostSegment` (class, `cli/banner_config.py:359`) `class LhostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:370`) `def render(self, ctx, cfg, color, glyphs)`
- `RhostSegment` (class, `cli/banner_config.py:376`) `class RhostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:387`) `def render(self, ctx, cfg, color, glyphs)`
- `DomainSegment` (class, `cli/banner_config.py:393`) `class DomainSegment(SegmentRenderer)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 106
- Cross-boundary resolved imports (EXTRACTED): 50

## Connections

- [EXTRACTED] depends_on community 2 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 10 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cli_auth.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)

## Open Questions

- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli: banner_config changed?
- Should cli: banner_config be split, given cohesion 0.41?

## Sources

- `cli/banner_config.py`
- `cli/commands/cli_auth.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/ux.py`
- `cli/config_history.py`
- `cli/engagement_hooks.py`
- `cli/fuzzy_match.py`
- `cli/fuzzy_picker.py`
- `cli/session_hud.py`
- `modules/cli_auth.py`
- `modules/redteam_gym.py`
- `tests/test_banner_config.py`
- `tests/test_cli_auth_remember.py`
- `tests/test_engagement_and_ping.py`
- `tests/test_engagement_command_gate.py`
- `tests/test_engagement_elo_and_methodology.py`
- `tests/test_fuzzy_picker.py`
- `tests/test_prompt_readline_markers.py`
- `tests/test_prompt_refresh.py`
