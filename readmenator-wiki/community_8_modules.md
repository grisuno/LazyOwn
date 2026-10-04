# modules

*Community 8 | 46 files | cohesion 0.47*

## Definition

This community groups 46 file(s) rooted at `modules` with dominant language py (cohesion 0.47). Central symbols: `AIResult`, `AVBlockedMatcher`, `AbstractReader`, `AbstractSelector`, `AbstractSignalMatcher`, `AccessFact`, `AutoMapper`, `BridgeDispatcher`. Core file: `skills/hive_mind.py` (107 symbols). Documented purpose: MCP verb bridge — one command language for operators and agents.  The MCP server (``skills/lazyown_mcp.py``) exposes workflow verbs that the operator documentat.

## Files

### `modules` (18 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ai_fallback.py` | py | utility | 8 | yes |
| `modules/atomic_enricher.py` | py | utility | 9 | yes |
| `modules/cve_matcher.py` | py | utility | 12 | yes |
| `modules/event_engine.py` | py | infrastructure | 10 | yes |

### `skills` (12 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/heartbeat.py` | py | utility | 5 | yes |
| `skills/hive_mind.py` | py | utility | 107 | yes |
| `skills/lazyown_automapper.py` | py | data_access | 23 | yes |
| `skills/lazyown_daemon.py` | py | utility | 24 | yes |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/integration_autonomous_flow.py` | py | testing | 1 | no |
| `tests/test_bridge_catalog_filtered.py` | py | testing | 20 | yes |
| `tests/test_core_modules.py` | py | presentation | 94 | yes |
| `tests/test_mcp_improvements.py` | py | testing | 34 | yes |

### `skills/tests` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/tests/test_facts.py` | py | testing | 37 | yes |
| `skills/tests/test_hive_mind.py` | py | testing | 95 | yes |
| `skills/tests/test_mcp_smoke.py` | py | testing | 5 | yes |

### `modules/integrations` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/integrations/__init__.py` | py | utility | 0 | yes |
| `modules/integrations/misp_export.py` | py | utility | 38 | yes |
| `modules/integrations/searchsploit.py` | py | utility | 27 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/mcp_bridge.py` | py | utility | 20 | yes |

### `contrib/legacy` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazyaddon_creator.py` | py | utility | 14 | yes |

*... and 26 more files in this community.*


## Key Symbols

- `_build_auto_populate_parser` (function, `cli/commands/mcp_bridge.py:50`) `def _build_auto_populate_parser()` - Return the argparse parser used by ``auto_populate``.
- `_build_facts_show_parser` (function, `cli/commands/mcp_bridge.py:67`) `def _build_facts_show_parser()` - Return the argparse parser used by ``facts_show``.
- `_build_rag_query_parser` (function, `cli/commands/mcp_bridge.py:84`) `def _build_rag_query_parser()` - Return the argparse parser used by ``rag_query``.
- `_build_parquet_query_parser` (function, `cli/commands/mcp_bridge.py:92`) `def _build_parquet_query_parser()` - Return the argparse parser used by ``parquet_query``.
- `_build_threat_model_parser` (function, `cli/commands/mcp_bridge.py:111`) `def _build_threat_model_parser()` - Return the argparse parser used by ``threat_model``.
- `_build_playbook_run_parser` (function, `cli/commands/mcp_bridge.py:124`) `def _build_playbook_run_parser()` - Return the argparse parser used by ``playbook_run``.
- `McpBridgeCommandSet` (class, `cli/commands/mcp_bridge.py:138`) `class McpBridgeCommandSet(LazyOwnCommandSet)` - CLI shims exposing the documented MCP verbs to human operators.
- `do_auto_populate` (method, `cli/commands/mcp_bridge.py:146`) `def do_auto_populate(self, args)` - Parse the latest nmap XML scan and auto-populate payload context.
- `do_facts_show` (method, `cli/commands/mcp_bridge.py:253`) `def do_facts_show(self, args)` - Show structured facts extracted from nmap scans and tool output.
- `do_rag_query` (method, `cli/commands/mcp_bridge.py:278`) `def do_rag_query(self, args)` - Semantic search over session artefacts (scans, logs, notes).
- `do_parquet_query` (method, `cli/commands/mcp_bridge.py:308`) `def do_parquet_query(self, args)` - Query the parquet knowledge bases (GTFOBins, LOLBas, ATT&CK, sessions).
- `do_threat_model` (method, `cli/commands/mcp_bridge.py:370`) `def do_threat_model(self, args)` - Build or inspect the threat model derived from session events.
- `do_playbook_run` (method, `cli/commands/mcp_bridge.py:423`) `def do_playbook_run(self, args)` - Execute a generated YAML playbook step by step through the shell.
- `_executor` (method, `cli/commands/mcp_bridge.py:467`) `def _executor(command, host)`
- `do_auto_loop` (method, `cli/commands/mcp_bridge.py:481`) `def do_auto_loop(self, line)` - Run a goal through the autonomous daemon orchestrator backend.
- `do_session_state` (method, `cli/commands/mcp_bridge.py:499`) `def do_session_state(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_session_state).
- `do_campaign_sitrep` (method, `cli/commands/mcp_bridge.py:504`) `def do_campaign_sitrep(self, line)` - Alias of ``sitrep`` kept for MCP verb parity (lazyown_campaign_sitrep).
- `do_timeline` (method, `cli/commands/mcp_bridge.py:509`) `def do_timeline(self, line)` - Alias of ``timeline_browser`` kept for MCP verb parity (lazyown_timeline).
- `_delegate` (method, `cli/commands/mcp_bridge.py:513`) `def _delegate(self, command, line)` - Forward ``line`` to another shell command verbatim.
- `_refresh_aliases` (method, `cli/commands/mcp_bridge.py:521`) `def _refresh_aliases(self)` - Hot-reload declarative aliases after mutating payload context.
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

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 239
- Cross-boundary resolved imports (EXTRACTED): 171

## Connections

- [EXTRACTED] depends_on community 0 <-> 8 (strength 0.9): Extracted import edge crosses communities: cli/commands/caldera.py imports modules/planner.py.
- [EXTRACTED] depends_on community 8 <-> 1 (strength 0.9): Extracted import edge crosses communities: cli/commands/mcp_bridge.py imports core/config.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: cli/commands/mcp_bridge.py imports modules/world_model.py.

## Risks

- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_replay.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `modules/pipeline_engine.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/lazyown_mcp.py` -> `skills/lazyown_llm.py` -> `skills/lazyown_mcp.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`
- [cycle] `skills/autonomous_daemon.py` -> `skills/lazyown_mcp.py` -> `skills/autonomous_daemon.py`

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `tests/integration_autonomous_flow.py`)? What purpose do they serve?
- Can the cycle `skills/lazyown_mcp.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` be broken with an interface?
- What would break if the most connected file in modules changed?
- Should modules be split, given cohesion 0.47?

## Sources

- `cli/commands/mcp_bridge.py`
- `contrib/legacy/lazyaddon_creator.py`
- `modules/ai_fallback.py`
- `modules/atomic_enricher.py`
- `modules/cve_matcher.py`
- `modules/event_engine.py`
- `modules/integrations/__init__.py`
- `modules/integrations/misp_export.py`
- `modules/integrations/searchsploit.py`
- `modules/lazyown_bridge.py`
- `modules/llm_client.py`
- `modules/llm_evaluator.py`
- `modules/memory_store.py`
- `modules/obs_parser.py`
- `modules/planner.py`
- `modules/playbook_engine.py`
- `modules/reactive_engine.py`
- `modules/recommender.py`
- `modules/session_rag.py`
- `modules/session_reader.py`
- *... and 26 more*
