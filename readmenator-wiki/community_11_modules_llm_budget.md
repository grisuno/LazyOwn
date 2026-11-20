# modules: llm_budget

*Community 11 | 43 files | cohesion 0.42*

## Definition

This community groups 43 file(s) rooted at `modules` with dominant language py (cohesion 0.42). Central symbols: `AIModel`, `AIResult`, `ASTToolExtractor`, `AgentRunner`, `AgentTool`, `AiCommandSet`, `AnthropicModel`, `BudgetConfig`. Core file: `tests/test_llm_orchestrator.py` (89 symbols). Documented purpose: Artificial Intelligence command set.  Covers the ``do_ask``, ``do_groq``, ``do_ai_playbook`` and ``do_ai_toggle`` commands. ``ask`` answers through the configur.

## Files

### `modules` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/agent_runner.py` | py | utility | 39 | yes |
| `modules/ai_fallback.py` | py | utility | 12 | yes |
| `modules/ai_model.py` | py | business_logic | 44 | yes |
| `modules/forensic_cleaner.py` | py | utility | 8 | yes |
| `modules/lazy_agent.py` | py | utility | 32 | yes |
| `modules/lazyllmchat.py` | py | utility | 30 | yes |

### `tests` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 15 | yes |
| `tests/test_ai_commands_llm.py` | py | testing | 18 | yes |
| `tests/test_lazy_streaming.py` | py | testing | 17 | yes |
| `tests/test_llm_adapter_parity.py` | py | testing | 42 | yes |
| `tests/test_llm_budget.py` | py | testing | 27 | yes |
| `tests/test_llm_key_pool.py` | py | testing | 9 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |
| `contrib/legacy/lazyllmchat.py` | py | utility | 30 | no |
| `contrib/legacy/lazyphishingai.py` | py | presentation | 12 | yes |

### `cli/commands` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/ai.py` | py | utility | 8 | yes |
| `cli/commands/opsec_cleanup.py` | py | utility | 9 | yes |

### `core` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `core/llm_budget.py` | py | utility | 45 | yes |
| `core/llm_key_pool.py` | py | utility | 17 | yes |

### `skills/mcp_tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/get_llm_budget.py` | py | utility | 1 | yes |

*... and 23 more files in this community.*


## Key Symbols

- `AiCommandSet` (class, `cli/commands/ai.py:71`) `class AiCommandSet(LazyOwnCommandSet)` - Pending phase module for the Artificial Intelligence commands.
- `do_ask` (method, `cli/commands/ai.py:78`) `def do_ask(self, line)` - Ask the AI a question with current session context pre-loaded.
- `do_groq` (method, `cli/commands/ai.py:166`) `def do_groq(self, line)` - Generate a single-line command through the Groq backend.
- `do_poolcheck` (method, `cli/commands/ai.py:197`) `def do_poolcheck(self, line)` - Prove the LLM failover pool order with one live prompt.
- `_serve` (function, `cli/commands/ai.py:220`) `def _serve(member_id, backend_name, text)`
- `do_ai_playbook` (method, `cli/commands/ai.py:254`) `def do_ai_playbook(self, line)` - Generate an offensive playbook from Nmap CSV + KB + Ollama.
- `do_ai_toggle` (method, `cli/commands/ai.py:361`) `def do_ai_toggle(self, _arg)` - Toggle the in-process AI assistant on or off.
- `do_llm_budget` (method, `cli/commands/ai.py:378`) `def do_llm_budget(self, line)` - Show the LLM daily cost budget, per call token cap, and current spend.
- `OpsecCleanupCommandSet` (class, `cli/commands/opsec_cleanup.py:19`) `class OpsecCleanupCommandSet(LazyOwnCommandSet)` - OPSEC scoring, log tampering, forensic cleaning, timestomping, memory/network OPSEC.
- `do_opsec_score` (method, `cli/commands/opsec_cleanup.py:25`) `def do_opsec_score(self, line)` - Real-time OPSEC risk assessment with contextual action gating (v2).
- `do_log_tamper` (method, `cli/commands/opsec_cleanup.py:97`) `def do_log_tamper(self, line)` - Cross-platform log clearing commands.
- `do_forensic_clean` (method, `cli/commands/opsec_cleanup.py:162`) `def do_forensic_clean(self, line)` - Clean forensic artifacts — Prefetch, Shimcache, Amcache, Jump Lists, etc.
- `do_timestomp` (method, `cli/commands/opsec_cleanup.py:219`) `def do_timestomp(self, line)` - Manipulate file MACB timestamps to evade forensic timeline analysis.
- `do_memory_clean` (method, `cli/commands/opsec_cleanup.py:288`) `def do_memory_clean(self, line)` - Clean memory artifacts — Kerberos tickets, clipboard, env vars, credentials.
- `do_network_opsec` (method, `cli/commands/opsec_cleanup.py:342`) `def do_network_opsec(self, line)` - Network OPSEC — proxy chains, DoH, canary detection, traffic analysis.
- `do_auditd_disable` (method, `cli/commands/opsec_cleanup.py:445`) `def do_auditd_disable(self, line)` - Generate commands to disable Linux auditd.
- `do_sysmon_disable` (method, `cli/commands/opsec_cleanup.py:468`) `def do_sysmon_disable(self, line)` - Generate commands to disable Windows Sysmon.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 133
- Cross-boundary resolved imports (EXTRACTED): 180

## Connections

- [EXTRACTED] depends_on community 11 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports cli/commands/_base.py.
- [EXTRACTED] depends_on community 11 <-> 7 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/killchain.py.
- [EXTRACTED] depends_on community 11 <-> 2 (strength 0.9): Extracted import edge crosses communities: cli/commands/ai.py imports modules/sidequestion.py.

## Risks

- [taint high] `cli/banner_config.py` -> `modules/llm_factory.py` via `subprocess` (4 hops)
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `modules/loop/target_os.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py` -> `core/config.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `contrib/legacy/lazyllmchat.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules: llm_budget changed?
- Should modules: llm_budget be split, given cohesion 0.42?

## Sources

- `cli/commands/ai.py`
- `cli/commands/opsec_cleanup.py`
- `contrib/legacy/lazyaddon_creator.py`
- `contrib/legacy/lazyllmchat.py`
- `contrib/legacy/lazyphishingai.py`
- `core/llm_budget.py`
- `core/llm_key_pool.py`
- `modules/agent_runner.py`
- `modules/ai_fallback.py`
- `modules/ai_model.py`
- `modules/forensic_cleaner.py`
- `modules/lazy_agent.py`
- `modules/lazyllmchat.py`
- `modules/llm_adapter.py`
- `modules/llm_client.py`
- `modules/llm_factory.py`
- `modules/llm_orchestrator.py`
- `modules/llm_pool.py`
- `modules/llm_prompts.py`
- `modules/log_tamper.py`
- *... and 23 more*
