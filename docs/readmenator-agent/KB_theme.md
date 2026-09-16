# Subsystem: theme

## lazygui/theme/__init__.py
- Layer: presentation
- Language: py
- Depends on: `lazygui/theme/manager.py`, `lazygui/theme/qss_builder.py`, `lazygui/theme/tokens.py`

## lazygui/theme/manager.py
- Layer: presentation
- Language: py
- Symbols:
  - `ThemeManager` (class, line 26) `class ThemeManager(QObject)`
  - `__init__` (method, line 31) `def __init__(self, constants, settings, application, palettes, parent)`
  - `active_tokens` (method, line 57) `def active_tokens(self)`
  - `active_id` (method, line 64) `def active_id(self)`
  - `available` (method, line 68) `def available(self)`
  - `apply_initial` (method, line 72) `def apply_initial(self)`
  - `apply` (method, line 80) `def apply(self, identifier)`
  - `cycle` (method, line 93) `def cycle(self)`
  - `_apply_to_application` (method, line 103) `def _apply_to_application(self, tokens)`
  - `_build_qpalette` (method, line 109) `def _build_qpalette(tokens)`
- Depends on: `core/logging.py`, `lazygui/config/constants.py`, `lazygui/config/settings.py`, `lazygui/theme/palettes/__init__.py`, `lazygui/theme/qss_builder.py`, `lazygui/theme/tokens.py`
- Imported by: `lazygui/app.py`, `lazygui/theme/__init__.py`, `lazygui/windows/main_window.py`

## lazygui/theme/qss_builder.py
- Layer: presentation
- Language: py
- Symbols:
  - `QssBuilder` (class, line 16) `class QssBuilder`
  - `build` (method, line 21) `def build(self, tokens)`
  - `_font_stack` (method, line 39) `def _font_stack(stack)`
- Depends on: `lazygui/config/constants.py`, `lazygui/theme/tokens.py`
- Imported by: `lazygui/theme/__init__.py`, `lazygui/theme/manager.py`

## lazygui/theme/tokens.py
- Layer: presentation
- Language: py
- Symbols:
  - `ThemeTokens` (class, line 14) `class ThemeTokens`
- Imported by: `lazygui/theme/__init__.py`, `lazygui/theme/manager.py`, `lazygui/theme/palettes/__init__.py`, `lazygui/theme/palettes/catppuccin_mocha.py`, `lazygui/theme/palettes/cobalt_clone.py`, `lazygui/theme/palettes/gruvbox_dark.py`, `lazygui/theme/palettes/solarized_light.py`, `lazygui/theme/palettes/tactical_green.py`, `lazygui/theme/palettes/tokyo_night.py`, `lazygui/theme/qss_builder.py`, `lazygui/windows/main_window.py`
