# skills/claude_md_orchestrator

*Community 8 | 19 files | cohesion 0.75*

## Definition

This community groups 19 file(s) rooted at `skills/claude_md_orchestrator` with dominant language py (cohesion 0.75). Central symbols: `AnalyzerResult`, `BddResult`, `CheckResult`, `CicdResult`, `CicleState`, `CicleStateFile`, `Config`, `Contract`. Core file: `static/js/xterm.js` (62 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: 09/06/2024 Licencia: GPL v3  Descripción: Assistente de consola  █.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |
| `contrib/legacy/lazyproxy.py` | py | utility | 9 | no |
| `contrib/legacy/lazyseo.py` | py | utility | 9 | no |
| `modules/colors.py` | py | utility | 3 | no |
| `skills/claude_md_orchestrator/__init__.py` | py | utility | 0 | yes |
| `skills/claude_md_orchestrator/bdd_agent.py` | py | utility | 8 | yes |
| `skills/claude_md_orchestrator/boy_scout.py` | py | utility | 5 | yes |
| `skills/claude_md_orchestrator/cicd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/config.py` | py | infrastructure | 15 | yes |
| `skills/claude_md_orchestrator/documentation_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/models.py` | py | business_logic | 32 | yes |
| `skills/claude_md_orchestrator/orchestrator.py` | py | utility | 21 | yes |
| `skills/claude_md_orchestrator/parser.py` | py | utility | 13 | yes |
| `skills/claude_md_orchestrator/reviewer_agent.py` | py | utility | 10 | yes |
| `skills/claude_md_orchestrator/sdd_agent.py` | py | utility | 6 | yes |
| `skills/claude_md_orchestrator/tdd_agent.py` | py | utility | 7 | yes |
| `skills/claude_md_orchestrator/validators.py` | py | utility | 21 | yes |
| `static/js/xterm.js` | js | utility | 62 | no |

## Key Symbols

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
- `_prompt_adversary` (function, `contrib/legacy/lazygptcli_unified.py:190`) `def _prompt_adversary(base_prompt, history, knowledge_base)`
- `_prompt_general` (function, `contrib/legacy/lazygptcli_unified.py:206`) `def _prompt_general(base_prompt, history, knowledge_base)`
- `_prompt_search` (function, `contrib/legacy/lazygptcli_unified.py:225`) `def _prompt_search(base_prompt, history, knowledge_base)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 41
- Cross-boundary resolved imports (EXTRACTED): 14

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` -> `utils.py`
- [cycle] `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `utils.py`
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:153` `handle_request` `server_socket`: Result of allocator stored in `server_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyproxy.py:184` `start_proxy` `proxy_socket`: Result of allocator stored in `proxy_socket` is never checked against NULL.
- [dataflow UNCHECKED_ALLOC] `contrib/legacy/lazyseo.py:50` `results` `content`: Result of allocator stored in `content` is never checked against NULL.

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `contrib/legacy/lazyproxy.py`)? What purpose do they serve?
- Can the cycle `utils.py` -> `skills/claude_md_orchestrator/parser.py` -> `skills/claude_md_orchestrator/models.py` -> `cli/commands/enum.py` -> `cli/commands/_base.py` be broken with an interface?
- What would break if the most connected file in skills/claude_md_orchestrator changed?
- Should skills/claude_md_orchestrator be split, given cohesion 0.75?

## Sources

- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazyseo.py`
- `modules/colors.py`
- `skills/claude_md_orchestrator/__init__.py`
- `skills/claude_md_orchestrator/bdd_agent.py`
- `skills/claude_md_orchestrator/boy_scout.py`
- `skills/claude_md_orchestrator/cicd_agent.py`
- `skills/claude_md_orchestrator/config.py`
- `skills/claude_md_orchestrator/documentation_agent.py`
- `skills/claude_md_orchestrator/models.py`
- `skills/claude_md_orchestrator/orchestrator.py`
- `skills/claude_md_orchestrator/parser.py`
- `skills/claude_md_orchestrator/reviewer_agent.py`
- `skills/claude_md_orchestrator/sdd_agent.py`
- `skills/claude_md_orchestrator/tdd_agent.py`
- `skills/claude_md_orchestrator/validators.py`
- `static/js/xterm.js`
