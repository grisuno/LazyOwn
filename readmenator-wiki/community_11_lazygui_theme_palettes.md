# lazygui/theme/palettes

*Community 11 | 7 files | cohesion 0.55*

## Definition

This community groups 7 file(s) rooted at `lazygui/theme/palettes` with dominant language py (cohesion 0.55). Central symbols: `ThemeTokens`. Core file: `lazygui/theme/tokens.py` (1 symbols). Documented purpose: Catppuccin Mocha palette - warm pastel dark theme..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazygui/theme/palettes/catppuccin_mocha.py` | py | presentation | 0 | yes |
| `lazygui/theme/palettes/cobalt_clone.py` | py | presentation | 0 | yes |
| `lazygui/theme/palettes/gruvbox_dark.py` | py | presentation | 0 | yes |
| `lazygui/theme/palettes/solarized_light.py` | py | presentation | 0 | yes |
| `lazygui/theme/palettes/tactical_green.py` | py | presentation | 0 | yes |
| `lazygui/theme/palettes/tokyo_night.py` | py | presentation | 0 | yes |
| `lazygui/theme/tokens.py` | py | presentation | 1 | yes |

## Key Symbols

- `ThemeTokens` (class, `lazygui/theme/tokens.py:14`) `class ThemeTokens` - Atomic design tokens for one theme variant.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 6
- Cross-boundary resolved imports (EXTRACTED): 5

## Connections

- [EXTRACTED] depends_on community 4 <-> 11 (strength 0.9): Extracted import edge crosses communities: lazygui/theme/__init__.py imports lazygui/theme/tokens.py.
- [EXTRACTED] depends_on community 10 <-> 11 (strength 0.9): Extracted import edge crosses communities: lazygui/windows/main_window.py imports lazygui/theme/tokens.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in lazygui/theme/palettes changed?
- Should lazygui/theme/palettes be split, given cohesion 0.55?

## Sources

- `lazygui/theme/palettes/catppuccin_mocha.py`
- `lazygui/theme/palettes/cobalt_clone.py`
- `lazygui/theme/palettes/gruvbox_dark.py`
- `lazygui/theme/palettes/solarized_light.py`
- `lazygui/theme/palettes/tactical_green.py`
- `lazygui/theme/palettes/tokyo_night.py`
- `lazygui/theme/tokens.py`
