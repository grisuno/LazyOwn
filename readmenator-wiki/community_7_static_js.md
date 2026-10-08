# static/js

*Community 7 | 22 files | cohesion 0.54*

## Definition

This community groups 22 file(s) rooted at `static/js` with dominant language js (cohesion 0.54). Central symbols: `A`, `As`, `B`, `BackgroundSize`, `BezierCurve`, `Bk`, `Bounds`, `Break`. Core file: `static/js/html2pdf.bundle.min.js` (695 symbols). Documented purpose: Pretty-print the live payload for the operator.  Tier 2.5 replaces ``do_show``'s unordered, unaligned dump with a stable, deterministic rendering. Output is pla.

## Files

### `static/js` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/bootstrap-4.5.2.min.js` | js | infrastructure | 7 | yes |
| `static/js/bootstrap-5.3.0.bundle.min.js` | js | infrastructure | 28 | yes |
| `static/js/chart.min.js` | js | utility | 88 | yes |
| `static/js/html2pdf.bundle.min.js` | js | utility | 695 | no |
| `static/js/jquery-3.5.1.slim.min.js` | js | utility | 6 | yes |
| `static/js/particles.js` | js | utility | 10 | yes |
| `static/js/quill-2.0.3.js` | js | utility | 124 | yes |
| `static/js/tippy-6.js` | js | utility | 3 | no |
| `static/js/vis-network-9.1.2.min.js` | js | utility | 135 | no |

### `contrib/legacy` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazybinenc.py` | py | utility | 2 | no |
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |
| `contrib/legacy/lazyproxy.py` | py | utility | 9 | no |
| `contrib/legacy/lazyseo.py` | py | utility | 9 | no |

### `.` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `key.py` | py | utility | 1 | no |

### `cli` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/show.py` | py | utility | 1 | yes |

### `core` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/prompt.py` | py | utility | 8 | yes |

### `lazyc2` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyc2/state.py` | py | utility | 0 | yes |

### `lazyown-docker` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `lazyown-docker/init.sh` | sh | utility | 0 | no |

### `modules` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/colors.py` | py | utility | 3 | no |

*... and 2 more files in this community.*


## Key Symbols

- `format_payload` (function, `cli/show.py:14`) `def format_payload(params)` - Render ``params`` as a sorted, aligned ``key = value`` block.
- `generate_key_iv` (function, `contrib/legacy/lazybinenc.py:12`) `def generate_key_iv(sessions_path)`
- `main` (function, `contrib/legacy/lazybinenc.py:54`) `def main()`
- `signal_handler` (function, `contrib/legacy/lazygptcli.py:66`) `def signal_handler(sig, frame)`
- `show_help` (function, `contrib/legacy/lazygptcli.py:73`) `def show_help(message)`
- `check_api_key` (function, `contrib/legacy/lazygptcli.py:77`) `def check_api_key()`
- `configure_logging` (function, `contrib/legacy/lazygptcli.py:83`) `def configure_logging(debug)`
- `parse_args` (function, `contrib/legacy/lazygptcli.py:87`) `def parse_args()`
- `create_complex_prompt` (function, `contrib/legacy/lazygptcli.py:94`) `def create_complex_prompt(base_prompt, history, knowledge_base, error_message)`
- `execute_command` (function, `contrib/legacy/lazygptcli.py:108`) `def execute_command(command)`
- `load_knowledge_base` (function, `contrib/legacy/lazygptcli.py:118`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazygptcli.py:124`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazygptcli.py:128`) `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function, `contrib/legacy/lazygptcli.py:133`) `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function, `contrib/legacy/lazygptcli.py:141`) `def transform_knowledge_base(client)`
- `cleanup_temp_files` (function, `contrib/legacy/lazygptcli.py:164`) `def cleanup_temp_files()`
- `main` (function, `contrib/legacy/lazygptcli.py:177`) `def main()`
- `_ret_model` (function, `contrib/legacy/lazygptcli_unified.py:45`) `def _ret_model()`
- `truncate_message` (function, `contrib/legacy/lazygptcli_unified.py:53`) `def truncate_message(message, max_chars)`
- `_configure_logging` (function, `contrib/legacy/lazygptcli_unified.py:57`) `def _configure_logging(debug)`
- `_load_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:62`) `def _load_knowledge_base(file_path)`
- `_save_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:70`) `def _save_knowledge_base(knowledge_base, file_path)`
- `_add_to_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:76`) `def _add_to_knowledge_base(prompt, response, file_path)`
- `_get_relevant_knowledge` (function, `contrib/legacy/lazygptcli_unified.py:82`) `def _get_relevant_knowledge(prompt, file_path)`
- `_transform_knowledge_base` (function, `contrib/legacy/lazygptcli_unified.py:95`) `def _transform_knowledge_base(client, kb_file, improved_file)`
- `_groq_chat` (function, `contrib/legacy/lazygptcli_unified.py:115`) `def _groq_chat(client, messages, model, max_tokens)`
- `_load_payload_kv` (function, `contrib/legacy/lazygptcli_unified.py:129`) `def _load_payload_kv()`
- `_load_event_config` (function, `contrib/legacy/lazygptcli_unified.py:147`) `def _load_event_config()`
- `_prompt_oneliner` (function, `contrib/legacy/lazygptcli_unified.py:159`) `def _prompt_oneliner(base_prompt, history, knowledge_base)`
- `_prompt_script` (function, `contrib/legacy/lazygptcli_unified.py:175`) `def _prompt_script(base_prompt, history, knowledge_base)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 88
- Cross-boundary resolved imports (EXTRACTED): 102

## Connections

- [EXTRACTED] depends_on community 1 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/misc_migrated.py imports cli/show.py.

## Risks

- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:153` `handle_request` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:184` `start_proxy` `proxy_socket`: Result of allocator stored in `proxy_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyseo.py:50` `results` `content`: Result of allocator stored in `content` is never checked against NULL.

## Open Questions

- Why do 11 file(s) lack file-level docs (e.g. `contrib/legacy/lazybinenc.py`)? What purpose do they serve?
- What would break if the most connected file in static/js changed?
- Should static/js be split, given cohesion 0.54?

## Sources

- `cli/show.py`
- `contrib/legacy/lazybinenc.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazyseo.py`
- `core/prompt.py`
- `key.py`
- `lazyc2/state.py`
- `lazyown-docker/init.sh`
- `modules/colors.py`
- `static/js/bootstrap-4.5.2.min.js`
- `static/js/bootstrap-5.3.0.bundle.min.js`
- `static/js/chart.min.js`
- `static/js/html2pdf.bundle.min.js`
- `static/js/jquery-3.5.1.slim.min.js`
- `static/js/particles.js`
- `static/js/quill-2.0.3.js`
- `static/js/tippy-6.js`
- `static/js/vis-network-9.1.2.min.js`
- *... and 2 more*
