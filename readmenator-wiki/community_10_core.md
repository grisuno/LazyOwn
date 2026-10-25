# core

*Community 10 | 22 files | cohesion 0.43*

## Definition

This community groups 22 file(s) rooted at `core` with dominant language py (cohesion 0.43). Central symbols: `AiCommandSet`, `AuthError`, `BudgetConfig`, `BudgetExceeded`, `BudgetGuard`, `BudgetLedger`, `BudgetedBackend`, `Config`. Core file: `core/llm_budget.py` (45 symbols). Documented purpose: Artificial Intelligence command set.  Covers the ``do_ask``, ``do_groq``, ``do_ai_playbook`` and ``do_ai_toggle`` commands. ``ask`` answers through the configur.

## Files

### `core` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/__init__.py` | py | utility | 0 | yes |
| `core/dependencies.py` | py | utility | 23 | yes |
| `core/errors.py` | py | utility | 23 | yes |
| `core/http.py` | py | presentation | 10 | yes |
| `core/llm_budget.py` | py | utility | 45 | yes |
| `core/network.py` | py | utility | 8 | yes |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_dependencies.py` | py | testing | 35 | yes |
| `tests/test_llm_adapter_parity.py` | py | testing | 41 | yes |
| `tests/test_llm_budget.py` | py | testing | 27 | yes |
| `tests/test_llm_prompts.py` | py | testing | 27 | yes |

### `.` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `discord_c2.py` | py | utility | 21 | no |
| `slack_c2_bot.py` | py | utility | 16 | yes |
| `telegram_c2.py` | py | utility | 18 | no |
| `telegram_hermes.py` | py | utility | 29 | yes |

### `modules` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/llm_adapter.py` | py | infrastructure | 15 | yes |
| `modules/llm_prompts.py` | py | utility | 28 | yes |
| `modules/sidequestion.py` | py | utility | 9 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 8 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyphishingai.py` | py | presentation | 12 | yes |

*... and 2 more files in this community.*


## Key Symbols

- `AiCommandSet` (class, `cli/commands/ai.py:71`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:78`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:166`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_poolcheck` (method, `cli/commands/ai.py:197`) `def do_poolcheck(self, line)` - Prove the LLM failover pool order with one live prompt.
- `_serve` (function, `cli/commands/ai.py:220`) `def _serve(member_id, backend_name, text)`
- `do_ai_playbook` (method, `cli/commands/ai.py:254`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:361`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:378`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `clean_think` (function, `contrib/legacy/lazyphishingai.py:28`) `def clean_think(texto)`
- `clean_yaml` (function, `contrib/legacy/lazyphishingai.py:31`) `def clean_yaml(texto)`
- `truncate_message` (function, `contrib/legacy/lazyphishingai.py:37`) `def truncate_message(message, max_chars)`
- `configure_logging` (function, `contrib/legacy/lazyphishingai.py:42`) `def configure_logging(debug)`
- `create_complex_prompt` (function, `contrib/legacy/lazyphishingai.py:46`) `def create_complex_prompt(base_prompt, history, knowledge_base)`
- `load_knowledge_base` (function, `contrib/legacy/lazyphishingai.py:101`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazyphishingai.py:110`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazyphishingai.py:117`) `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function, `contrib/legacy/lazyphishingai.py:122`) `def get_relevant_knowledge(prompt)`
- `process_prompt_local_yaml` (function, `contrib/legacy/lazyphishingai.py:132`) `def process_prompt_local_yaml(prompt, debug, mode, output_file)`
- `generate` (function, `contrib/legacy/lazyphishingai.py:155`) `def generate()`
- `parse_args` (function, `contrib/legacy/lazyphishingai.py:192`) `def parse_args()`
- `MissingDependencyError` (class, `core/dependencies.py:37`) `class MissingDependencyError(ImportError)` - Raised when an optional dependency is used but is not installed.
- `__init__` (method, `core/dependencies.py:45`) `def __init__(self, import_name, pip_package, feature)` - Build a remediation-oriented error message.
- `DependencySpec` (class, `core/dependencies.py:66`) `class DependencySpec` - Declarative metadata for a single optional Python dependency.
- `_DeferredImport` (class, `core/dependencies.py:101`) `class _DeferredImport` - Stand-in for a missing optional dependency.
- `__init__` (method, `core/dependencies.py:115`) `def __init__(self, spec)` - Store the dependency spec used to build remediation errors.
- `_raise` (method, `core/dependencies.py:123`) `def _raise(self)` - Raise a :class:`MissingDependencyError` for the proxied dependency.
- `__getattr__` (method, `core/dependencies.py:132`) `def __getattr__(self, _name)` - Reject attribute access on a missing dependency.
- `__call__` (method, `core/dependencies.py:136`) `def __call__(self)` - Reject calling a missing dependency.
- `__getitem__` (method, `core/dependencies.py:140`) `def __getitem__(self, _key)` - Reject subscription of a missing dependency.
- `__iter__` (method, `core/dependencies.py:144`) `def __iter__(self)` - Reject iteration over a missing dependency.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 47
- Cross-boundary resolved imports (EXTRACTED): 41

## Connections

- [EXTRACTED] depends_on community 1 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.
- [EXTRACTED] depends_on community 10 <-> 0 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/llm_factory.py.
- [EXTRACTED] depends_on community 10 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `core/dependencies.py` via `subprocess` (5 hops)

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `discord_c2.py`)? What purpose do they serve?
- What would break if the most connected file in core changed?
- Should core be split, given cohesion 0.43?

## Sources

- `cli/commands/ai.py`
- `contrib/legacy/lazyphishingai.py`
- `core/__init__.py`
- `core/dependencies.py`
- `core/errors.py`
- `core/http.py`
- `core/llm_budget.py`
- `core/network.py`
- `core/parsers.py`
- `discord_c2.py`
- `modules/llm_adapter.py`
- `modules/llm_prompts.py`
- `modules/sidequestion.py`
- `slack_c2_bot.py`
- `telegram_c2.py`
- `telegram_hermes.py`
- `tests/test_ai_commands_llm.py`
- `tests/test_dependencies.py`
- `tests/test_llm_adapter_parity.py`
- `tests/test_llm_budget.py`
- *... and 2 more*
