# Subsystem: tools

## tools/extract_cluster.py
- Doc: Extract a named cluster of do_* methods from a CommandSet module.
- Layer: utility
- Language: py
- Symbols:
  - `fragment_name` (function, line 29) `def fragment_name(fragment)`
  - `collect_methods` (function, line 41) `def collect_methods(source_text, wanted)`
  - `build_module` (function, line 66) `def build_module(target_class, phase, category, title, methods, extra_imports)`
  - `main` (function, line 141) `def main()`

## tools/gen_demo_gifs.py
- Doc: Generate LazyOwn demo GIFs without external services.
- Layer: utility
- Language: py
- Symbols:
  - `font` (function, line 14) `def font(size)`
  - `render` (function, line 22) `def render(lines, path, hold)`
  - `main` (function, line 70) `def main()`
- Imported by: `tools/gen_demo_gifs_extra.py`

## tools/gen_demo_gifs_extra.py
- Doc: Additional LazyOwn demo GIFs.
- Layer: utility
- Language: py
- Symbols:
  - `main` (function, line 49) `def main()`
- Depends on: `tools/gen_demo_gifs.py`
