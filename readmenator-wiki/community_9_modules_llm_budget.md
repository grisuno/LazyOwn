# modules: llm_budget

*Community 9 | 33 files | cohesion 0.41*

## Definition

This community groups 33 file(s) rooted at `modules` with dominant language py (cohesion 0.41). Central symbols: `AIModel`, `ASTToolExtractor`, `AgentRunner`, `AgentTool`, `AnthropicModel`, `BudgetConfig`, `BudgetExceeded`, `BudgetGuard`. Core file: `core/llm_budget.py` (45 symbols). Documented purpose: Unified Ollama/DeepSeek client for LazyOwn — merges lazydeepseekcli_local + lazydeepseekcli_localreport.  Provides streaming SSE responses via Flask for both re.

## Files

### `modules` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 38 | yes |
| `modules/ai_model.py` | py | business_logic | 39 | yes |
| `modules/colors.py` | py | utility | 3 | no |
| `modules/llm_adapter.py` | py | infrastructure | 16 | yes |
| `modules/llm_client.py` | py | infrastructure | 12 | yes |

### `contrib/legacy` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |
| `contrib/legacy/lazydeepseekcli.py` | py | presentation | 16 | yes |
| `contrib/legacy/lazygptcli.py` | py | utility | 14 | yes |
| `contrib/legacy/lazygptcli_unified.py` | py | utility | 29 | yes |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |

### `tests` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_c2_surfaces.py` | py | testing | 12 | yes |
| `tests/test_lazy_streaming.py` | py | testing | 17 | yes |
| `tests/test_llm_adapter_parity.py` | py | testing | 42 | yes |

### `.` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `discord_c2.py` | py | utility | 21 | no |
| `slack_c2_bot.py` | py | utility | 16 | yes |
| `telegram_c2.py` | py | utility | 19 | no |
| `telegram_hermes.py` | py | utility | 31 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/llm_budget.py` | py | utility | 45 | yes |
| `core/parsers.py` | py | utility | 1 | yes |

*... and 13 more files in this community.*


## Key Symbols

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
- `truncate_message` (function, `contrib/legacy/lazydeepseekcli.py:41`) `def truncate_message(message, max_chars)`
- `configure_logging` (function, `contrib/legacy/lazydeepseekcli.py:45`) `def configure_logging(debug)`
- `_load_payload_kv` (function, `contrib/legacy/lazydeepseekcli.py:50`) `def _load_payload_kv()`
- `_load_report_context` (function, `contrib/legacy/lazydeepseekcli.py:68`) `def _load_report_context()`
- `_prompt_redteam` (function, `contrib/legacy/lazydeepseekcli.py:79`) `def _prompt_redteam(base_prompt, history, knowledge_base)`
- `_prompt_report` (function, `contrib/legacy/lazydeepseekcli.py:118`) `def _prompt_report(base_prompt, history, knowledge_base)`
- `load_knowledge_base` (function, `contrib/legacy/lazydeepseekcli.py:167`) `def load_knowledge_base(file_path)`
- `save_knowledge_base` (function, `contrib/legacy/lazydeepseekcli.py:174`) `def save_knowledge_base(knowledge_base, file_path)`
- `add_to_knowledge_base` (function, `contrib/legacy/lazydeepseekcli.py:179`) `def add_to_knowledge_base(prompt, command, file_path)`
- `get_relevant_knowledge` (function, `contrib/legacy/lazydeepseekcli.py:185`) `def get_relevant_knowledge(prompt)`
- `transform_knowledge_base` (function, `contrib/legacy/lazydeepseekcli.py:193`) `def transform_knowledge_base(prompt_builder)`
- `_ollama_stream` (function, `contrib/legacy/lazydeepseekcli.py:223`) `def _ollama_stream(prompt_text, mode, timeout)`
- `generate` (function, `contrib/legacy/lazydeepseekcli.py:232`) `def generate()`
- `process_prompt_local` (function, `contrib/legacy/lazydeepseekcli.py:261`) `def process_prompt_local(prompt, debug, mode)`
- `process_prompt_localreport` (function, `contrib/legacy/lazydeepseekcli.py:269`) `def process_prompt_localreport(prompt, debug, mode)`
- `parse_args` (function, `contrib/legacy/lazydeepseekcli.py:277`) `def parse_args()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 84
- Cross-boundary resolved imports (EXTRACTED): 97

## Connections

- [EXTRACTED] depends_on community 1 <-> 9 (strength 0.9): Extracted import edge crosses communities: cli/banner_config.py imports core/parsers.py.

## Risks

- [taint high] `cli/banner_config.py` -> `core/parsers.py` via `subprocess` (1 hops)
- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_factory.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/config.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/param_registry.py` -> `core/payload_schema.py`
- [cycle] `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/mcp_agent_bridge.py` -> `modules/llm_factory.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`

## Open Questions

- Why do 6 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules: llm_budget changed?
- Should modules: llm_budget be split, given cohesion 0.41?

## Sources

- `contrib/legacy/lazyaddon_creator.py`
- `contrib/legacy/lazydeepseekcli.py`
- `contrib/legacy/lazygptcli.py`
- `contrib/legacy/lazygptcli_unified.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyphishingai.py`
- `contrib/legacy/lazyproxy.py`
- `contrib/legacy/lazyseo.py`
- `core/llm_budget.py`
- `core/parsers.py`
- `discord_c2.py`
- `modules/agent_runner.py`
- `modules/ai_model.py`
- `modules/colors.py`
- `modules/llm_adapter.py`
- `modules/llm_client.py`
- `modules/llm_factory.py`
- `modules/llm_prompts.py`
- `modules/privesc_predictor.py`
- `modules/vuln_bot_cli.py`
- *... and 13 more*
