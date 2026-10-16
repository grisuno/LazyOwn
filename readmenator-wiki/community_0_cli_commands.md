# cli/commands

*Community 0 | 157 files | cohesion 0.55*

## Definition

This community groups 157 file(s) rooted at `cli/commands` with dominant language py (cohesion 0.55). Central symbols: `AddonHotReloader`, `AddonInfo`, `AddonRegistry`, `AliasResolver`, `AntiForensicsCommandSet`, `AppLockerBypassCommandSet`, `AuditCommandSet`, `BackendAdapterSpec`. Core file: `tests/test_improvements_spec.py` (160 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Este archivo contiene la.

## Files

### `cli/commands` (56 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/__init__.py` | py | utility | 0 | yes |
| `cli/commands/_base.py` | py | utility | 7 | yes |
| `cli/commands/_dormancy.py` | py | utility | 2 | yes |
| `cli/commands/anti_forensics.py` | py | utility | 7 | yes |

### `tests` (45 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_aes_key_propagation.py` | py | testing | 12 | yes |
| `tests/test_api_key_resolution.py` | py | testing | 9 | yes |
| `tests/test_backdoor_random.py` | py | testing | 5 | yes |

### `modules` (30 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_purple.py` | py | utility | 40 | yes |
| `modules/beacon_config_builder.py` | py | infrastructure | 14 | yes |
| `modules/bitm_engine.py` | py | utility | 18 | yes |

### `cli` (14 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/aliases.py` | py | utility | 7 | yes |
| `cli/banner_config.py` | py | infrastructure | 120 | yes |
| `cli/cli_enhancements.py` | py | utility | 69 | yes |

### `core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/config.py` | py | infrastructure | 18 | yes |
| `core/defaults.py` | py | utility | 8 | yes |
| `core/hardening.py` | py | utility | 34 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `banner.py` | py | utility | 3 | yes |
| `utils.py` | py | utility | 124 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazysmbrelay.py` | py | utility | 7 | no |

### `scripts/devtools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `scripts/devtools/core_smoke.py` | py | utility | 4 | yes |

*... and 137 more files in this community.*


## Key Symbols

- `image_to_bash` (function, `banner.py:26`) `def image_to_bash(image_path, image_res)`
- `list_png_files` (function, `banner.py:50`) `def list_png_files()`
- `main` (function, `banner.py:60`) `def main()`
- `_SafeFormatDict` (class, `cli/aliases.py:29`) `class _SafeFormatDict(dict)` - ``str.format_map`` source that returns ``""`` for missing/None values.
- `__missing__` (method, `cli/aliases.py:32`) `def __missing__(self, key)`
- `__getitem__` (method, `cli/aliases.py:35`) `def __getitem__(self, key)`
- `_substitute` (function, `cli/aliases.py:42`) `def _substitute(template, payload)` - Render ``template`` against ``payload`` placeholders.
- `template_placeholders` (function, `cli/aliases.py:56`) `def template_placeholders(template)` - Return the ``{name}`` placeholders referenced by ``template``.
- `empty_placeholders` (function, `cli/aliases.py:72`) `def empty_placeholders(template, context)` - Return placeholders whose rendered value against ``context`` is empty.
- `load_aliases` (function, `cli/aliases.py:77`) `def load_aliases(payload, path, lazy)` - Return the cmd2 alias map.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 537
- Cross-boundary resolved imports (EXTRACTED): 452

## Connections

- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/__init__.py imports cli/aliases.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/auto_crypto.py imports modules/cli_auth.py.
- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 0 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/safe_exec.py.
- [EXTRACTED] depends_on community 12 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/active_directory.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 1 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/automation.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 13 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/cloud_attacks.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 11 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/database.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 0 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/defaults.py imports cli/assign.py.

## Risks

- [taint high] `cli/banner_config.py` -> `cli/banner_config.py` via `subprocess` (0 hops)
- [taint high] `cli/banner_config.py` -> `cli/engagement_hooks.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/cli_auth.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/safe_exec.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `cli/palette.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/config.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `modules/lazy_rbac.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/logging.py` via `subprocess` (2 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/enum.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `cli/commands/_base.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `utils.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/validators.py` via `subprocess` (4 hops)

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `contrib/legacy/lazysmbrelay.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- Is the dangerous import `subprocess` in `cli/banner_config.py` still required, or can it be isolated?
- What would break if the most connected file in cli/commands changed?
- Should cli/commands be split, given cohesion 0.55?

## Sources

- `banner.py`
- `cli/aliases.py`
- `cli/banner_config.py`
- `cli/cli_enhancements.py`
- `cli/commands/__init__.py`
- `cli/commands/_base.py`
- `cli/commands/_dormancy.py`
- `cli/commands/anti_forensics.py`
- `cli/commands/applocker_bypass.py`
- `cli/commands/audit.py`
- `cli/commands/bitm.py`
- `cli/commands/bof_registry.py`
- `cli/commands/c2_profile.py`
- `cli/commands/campaign.py`
- `cli/commands/catalog.py`
- `cli/commands/cicd.py`
- `cli/commands/cli_auth.py`
- `cli/commands/cloud.py`
- `cli/commands/command_and_control.py`
- `cli/commands/cred.py`
- *... and 137 more*
