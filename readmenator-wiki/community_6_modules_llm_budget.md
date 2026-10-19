# modules: llm_budget

*Community 6 | 35 files | cohesion 0.43*

## Definition

This community groups 35 file(s) rooted at `modules` with dominant language py (cohesion 0.43). Central symbols: `AIModel`, `ASTToolExtractor`, `AgentRunner`, `AgentTool`, `AiCommandSet`, `AnthropicModel`, `AuthError`, `BudgetConfig`. Core file: `tests/test_payload_schema.py` (53 symbols). Documented purpose: Artificial Intelligence command set.  Covers the ``do_ask``, ``do_groq``, ``do_ai_playbook`` and ``do_ai_toggle`` commands. ``ask`` answers through the configur.

## Files

### `modules` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 38 | yes |
| `modules/ai_model.py` | py | business_logic | 39 | yes |
| `modules/llm_adapter.py` | py | infrastructure | 15 | yes |
| `modules/llm_client.py` | py | infrastructure | 12 | yes |

### `tests` (9 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_core_config.py` | py | testing | 19 | yes |
| `tests/test_dependencies.py` | py | testing | 35 | yes |
| `tests/test_lazy_streaming.py` | py | testing | 17 | yes |

### `core` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/dependencies.py` | py | utility | 23 | yes |
| `core/errors.py` | py | utility | 23 | yes |
| `core/http.py` | py | presentation | 10 | yes |

### `.` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `discord_c2.py` | py | utility | 21 | no |
| `slack_c2_bot.py` | py | utility | 16 | yes |
| `telegram_c2.py` | py | utility | 18 | no |
| `telegram_hermes.py` | py | utility | 29 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |
| `contrib/legacy/lazyphishingai.py` | py | presentation | 12 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 8 | yes |

*... and 15 more files in this community.*


## Key Symbols

- `AiCommandSet` (class, `cli/commands/ai.py:71`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:78`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:166`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_poolcheck` (method, `cli/commands/ai.py:197`) `def do_poolcheck(self, line)` - Prove the LLM failover pool order with one live prompt.
- `_serve` (function, `cli/commands/ai.py:220`) `def _serve(member_id, backend_name, text)`
- `do_ai_playbook` (method, `cli/commands/ai.py:254`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:361`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:378`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `parse_github_url` (function, `contrib/legacy/lazyaddon_creator.py:49`) `def parse_github_url(url)` - Extrae (owner, repo) de una URL de GitHub.
- `github_api_get` (function, `contrib/legacy/lazyaddon_creator.py:58`) `def github_api_get(owner, repo, endpoint)` - GET a la API pública de GitHub (sin auth, rate-limit 60/hr).
- `fetch_repo_metadata` (function, `contrib/legacy/lazyaddon_creator.py:68`) `def fetch_repo_metadata(owner, repo)` - Devuelve metadata básica del repo.
- `fetch_readme` (function, `contrib/legacy/lazyaddon_creator.py:73`) `def fetch_readme(owner, repo)` - Descarga y decodifica el README.
- `fetch_root_files` (function, `contrib/legacy/lazyaddon_creator.py:85`) `def fetch_root_files(owner, repo)` - Lista nombres de archivos en el directorio raíz.
- `build_llm_prompt` (function, `contrib/legacy/lazyaddon_creator.py:98`) `def build_llm_prompt(meta, readme, root_files)` - Construye el prompt para el LLM.
- `extract_json_from_response` (function, `contrib/legacy/lazyaddon_creator.py:164`) `def extract_json_from_response(text)` - Extrae el primer bloque JSON de una respuesta de LLM.
- `heuristic_install_command` (function, `contrib/legacy/lazyaddon_creator.py:192`) `def heuristic_install_command(root_files, language)` - Infiere un install_command básico a partir de los archivos raíz.
- `heuristic_execute_command` (function, `contrib/legacy/lazyaddon_creator.py:211`) `def heuristic_execute_command(name, root_files, language)` - Infiere un execute_command básico.
- `heuristic_params` (function, `contrib/legacy/lazyaddon_creator.py:245`) `def heuristic_params(name, readme, root_files)` - Infiere parámetros comunes basándose en el nombre y README.
- `fallback_yaml_data` (function, `contrib/legacy/lazyaddon_creator.py:276`) `def fallback_yaml_data(meta, readme, root_files)` - Genera datos de addon usando solo heurísticas locales (sin LLM).
- `build_yaml` (function, `contrib/legacy/lazyaddon_creator.py:300`) `def build_yaml(data, repo_url)` - Construye la estructura de dict que representa el addon YAML.
- `save_yaml` (function, `contrib/legacy/lazyaddon_creator.py:336`) `def save_yaml(addon, output_dir)` - Guarda el dict como archivo YAML en output_dir.
- `main` (function, `contrib/legacy/lazyaddon_creator.py:357`) `def main()`
- `LazyOwnShellBridge` (class, `contrib/legacy/lazyllmchat.py:22`) `class LazyOwnShellBridge`
- `__init__` (method, `contrib/legacy/lazyllmchat.py:25`) `def __init__(self, script_path)`
- `_load_shell` (method, `contrib/legacy/lazyllmchat.py:31`) `def _load_shell(self)`
- `no_history_init` (function, `contrib/legacy/lazyllmchat.py:38`) `def no_history_init(self_)`
- `execute` (method, `contrib/legacy/lazyllmchat.py:65`) `def execute(self, command)`
- `target` (function, `contrib/legacy/lazyllmchat.py:70`) `def target()`
- `SessionContextProvider` (class, `contrib/legacy/lazyllmchat.py:104`) `class SessionContextProvider`
- `__init__` (method, `contrib/legacy/lazyllmchat.py:105`) `def __init__(self, session_path)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 89
- Cross-boundary resolved imports (EXTRACTED): 104

## Connections

- [EXTRACTED] depends_on community 7 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/assign.py imports core/payload_schema.py.
- [EXTRACTED] depends_on community 0 <-> 6 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 6 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 6 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_pool.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/payload_schema.py` via `subprocess` (3 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [taint high] `cli/banner_config.py` -> `core/dependencies.py` via `subprocess` (5 hops)
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/ai_model.py` -> `modules/llm_factory.py`

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- Can the cycle `modules/llm_factory.py` -> `modules/ai_model.py` be broken with an interface?
- What would break if the most connected file in modules: llm_budget changed?
- Should modules: llm_budget be split, given cohesion 0.43?

## Sources

- `cli/commands/ai.py`
- `contrib/legacy/lazyaddon_creator.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyphishingai.py`
- `core/__init__.py`
- `core/dependencies.py`
- `core/errors.py`
- `core/http.py`
- `core/llm_budget.py`
- `core/network.py`
- `core/parsers.py`
- `core/payload_schema.py`
- `discord_c2.py`
- `modules/agent_runner.py`
- `modules/ai_model.py`
- `modules/llm_adapter.py`
- `modules/llm_client.py`
- `modules/llm_factory.py`
- `modules/llm_prompts.py`
- `modules/sidequestion.py`
- *... and 15 more*
