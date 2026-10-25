# Subsystem: tools

## tools/contract_check.py
- Doc: Contract conformance checker for single-file LAZY port modules.
- Layer: utility
- Language: py
- Symbols:
  - `check_file` (function, line 19) `def check_file(path)`
  - `main` (function, line 46) `def main(argv)`

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

## tools/generate_metasploitable_gym.py
- Doc: Generate the Metasploitable 2 gym catalogue.
- Layer: utility
- Language: py
- Symbols:
  - `exploit_document` (function, line 919) `def exploit_document(item)`
  - `chain_document` (function, line 942) `def chain_document(item)`
  - `base_chain_document` (function, line 961) `def base_chain_document()`
  - `index_document` (function, line 1034) `def index_document()`
  - `_normalize_dvwa` (function, line 1061) `def _normalize_dvwa()`
  - `write` (function, line 1074) `def write()`

## tools/set_lazyaddon_updates.py
- Doc: Set or check the ``update`` flag on every lazyaddon YAML.
- Layer: utility
- Language: py
- Symbols:
  - `set_flag` (function, line 22) `def set_flag(path, value)`
  - `read_flag` (function, line 45) `def read_flag(path)`
  - `main` (function, line 55) `def main()`
