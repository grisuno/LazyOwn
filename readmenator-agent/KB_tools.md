# Subsystem: tools

## tools/extract_cluster.py
- Layer: utility
- Doc: Extract a named cluster of do_* methods from a CommandSet module.  Usage: python3 tools/extract_cluster.py <source.py> <
- Language: py
- Symbols:
  - `fragment_name` (function, line 29) `def fragment_name(fragment)`
  - `collect_methods` (function, line 41) `def collect_methods(source_text, wanted)`
  - `build_module` (function, line 66) `def build_module(target_class, phase, category, title, methods, extra_imports)`
  - `main` (function, line 143) `def main()`

## tools/gen_demo_gifs.py
- Layer: utility
- Doc: Generate LazyOwn demo GIFs without external services.
- Language: py
- Symbols:
  - `font` (function, line 12) `def font(size)`
  - `render` (function, line 20) `def render(lines, path, hold)`
  - `main` (function, line 68) `def main()`
- Imported by: `tools/gen_demo_gifs_extra.py`

## tools/gen_demo_gifs_extra.py
- Layer: utility
- Doc: Additional LazyOwn demo GIFs. Every command verified against source.
- Language: py
- Symbols:
  - `main` (function, line 47) `def main()`
- Depends on: `tools/gen_demo_gifs.py`
