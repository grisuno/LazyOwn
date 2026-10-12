# cli: banner_config

*Community 6 | 40 files | cohesion 0.51*

## Definition

This community groups 40 file(s) rooted at `tests` with dominant language py (cohesion 0.51). Central symbols: `AddonCreatorConfig`, `AddonDraft`, `AddonStore`, `AddonValidationError`, `AddonValidator`, `AddonYamlRenderer`, `BannerConfig`, `BannerConfigurator`. Core file: `cli/banner_config.py` (120 symbols). Documented purpose: Configurable Neon Box banner for the LazyOwn interactive shell.  The module exposes a single, self-contained banner subsystem with three extension axes the oper.

## Files

### `tests` (13 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_addon_creator.py` | py | testing | 86 | yes |
| `tests/test_banner_config.py` | py | testing | 45 | yes |
| `tests/test_cli_auth_remember.py` | py | testing | 7 | yes |

### `cli` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/banner_config.py` | py | infrastructure | 120 | yes |
| `cli/config_history.py` | py | infrastructure | 9 | yes |
| `cli/engagement_hooks.py` | py | utility | 32 | yes |

### `cli/commands` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/cli_auth.py` | py | utility | 5 | yes |
| `cli/commands/exploitgym.py` | py | utility | 10 | yes |
| `cli/commands/redteam_gym.py` | py | utility | 8 | yes |

### `lazyc2/blueprints` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/blueprints/addons.py` | py | presentation | 14 | yes |
| `lazyc2/blueprints/auth.py` | py | presentation | 19 | yes |

### `modules` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/cli_auth.py` | py | utility | 18 | yes |
| `modules/exploitgym_gym.py` | py | utility | 20 | yes |

### `lazyc2` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/__init__.py` | py | utility | 0 | no |
| `lazyc2/addon_creator.py` | py | utility | 38 | yes |

### `lazyc2/extensions` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/extensions/decoy.py` | py | presentation | 1 | yes |
| `lazyc2/extensions/storage.py` | py | data_access | 12 | yes |

### `static/js` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/socket.io-4.0.0.min.js` | js | utility | 32 | yes |
| `static/js/socket.io-4.3.2.min.js` | js | utility | 15 | yes |

### `lazyc2/security` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/security/csrf.py` | py | utility | 11 | yes |

*... and 20 more files in this community.*


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
- `RhostSegment` (class, `cli/banner_config.py:376`) `class RhostSegment(SegmentRenderer)`
- `render` (method, `cli/banner_config.py:387`) `def render(self, ctx, cfg, color, glyphs)`
- `DomainSegment` (class, `cli/banner_config.py:393`) `class DomainSegment(SegmentRenderer)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 168
- Cross-boundary resolved imports (EXTRACTED): 69

## Connections

- [EXTRACTED] depends_on community 0 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 6 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/cli_auth.py imports cli/commands/_base.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `lazyc2/__init__.py`)? What purpose do they serve?
- Can the cycle `cli/engagement_hooks.py` -> `modules/cli_auth.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli: banner_config changed?
- Should cli: banner_config be split, given cohesion 0.51?

## Sources

- `cli/banner_config.py`
- `cli/commands/cli_auth.py`
- `cli/commands/exploitgym.py`
- `cli/commands/redteam_gym.py`
- `cli/commands/ux.py`
- `cli/config_history.py`
- `cli/engagement_hooks.py`
- `cli/fuzzy_match.py`
- `cli/fuzzy_picker.py`
- `cli/session_hud.py`
- `lazyc2/__init__.py`
- `lazyc2/addon_creator.py`
- `lazyc2/blueprints/addons.py`
- `lazyc2/blueprints/auth.py`
- `lazyc2/blueprints/operations.py`
- `lazyc2/blueprints/session_auth.py`
- `lazyc2/extensions/decoy.py`
- `lazyc2/extensions/storage.py`
- `lazyc2/extensions/users.py`
- `lazyc2/models.py`
- *... and 20 more*
