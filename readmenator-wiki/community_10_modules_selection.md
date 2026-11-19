# modules/selection

*Community 10 | 40 files | cohesion 0.57*

## Definition

This community groups 40 file(s) rooted at `modules/selection` with dominant language py (cohesion 0.57). Central symbols: `ActionDecision`, `AdversarySelector`, `AtomicSelector`, `AutoVerb`, `BridgeSelector`, `ChainSelector`, `CredentialSpraySelector`, `EDBSelector`. Core file: `modules/auto_registry.py` (46 symbols). Documented purpose: Registry of loop-ready automation verbs (the ``auto_*`` family plus read-only staging verbs such as ``atomic_tests`` / ``atomic_gen``).  Every entry is a LazyOw.

## Files

### `modules/selection` (18 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/selection/__init__.py` | py | utility | 0 | yes |
| `modules/selection/_phase_categories.py` | py | utility | 1 | yes |
| `modules/selection/adversary.py` | py | utility | 6 | yes |
| `modules/selection/atomic.py` | py | utility | 2 | yes |
| `modules/selection/base.py` | py | utility | 4 | yes |
| `modules/selection/bridge.py` | py | utility | 2 | yes |
| `modules/selection/chain.py` | py | utility | 3 | yes |

### `tests` (15 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_auto_registry.py` | py | testing | 20 | yes |
| `tests/test_chain_match_determinism.py` | py | testing | 13 | yes |
| `tests/test_chain_selector.py` | py | testing | 14 | yes |
| `tests/test_intel_selector.py` | py | testing | 16 | yes |
| `tests/test_loop_fire_pending.py` | py | testing | 14 | yes |
| `tests/test_poc_registry.py` | py | testing | 29 | yes |

### `modules` (4 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/auto_registry.py` | py | utility | 46 | yes |
| `modules/campaign_blacklist.py` | py | utility | 4 | yes |
| `modules/chain_match.py` | py | utility | 7 | yes |
| `modules/reverse-shell.c` | c | utility | 2 | no |

### `modules/rootkit` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/rootkit/rootkit.c` | c | utility | 13 | yes |

### `skills/mcp_tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `skills/mcp_tools/lazy_addon.py` | py | utility | 1 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/select2-4.1.0.min.js` | js | utility | 3 | yes |

*... and 20 more files in this community.*


## Key Symbols

- `_looks_like_target` (function, `modules/auto_registry.py:38`) `def _looks_like_target(value)` - Check whether a token is a plausible network target.
- `auto_verb_target` (function, `modules/auto_registry.py:55`) `def auto_verb_target(command)` - Return the target an ``auto <verb> <target>`` line carries, else ''.
- `AutoVerb` (class, `modules/auto_registry.py:95`) `class AutoVerb` - One automation verb the loop may invoke autonomously.
- `_os_default_for_verb` (function, `modules/auto_registry.py:278`) `def _os_default_for_verb(verb)` - Return the target OS for one built-in auto verb.
- `_verb_rows` (function, `modules/auto_registry.py:286`) `def _verb_rows()` - Merged auto-verb rows (built-ins + operator overrides) as objects.
- `_verb_row` (function, `modules/auto_registry.py:331`) `def _verb_row(name)` - Return one merged auto-verb row by name, or None.
- `verb_enabled` (function, `modules/auto_registry.py:340`) `def verb_enabled(name)` - Return whether one auto verb may be proposed or executed.
- `_cli_verb_allowed` (function, `modules/auto_registry.py:427`) `def _cli_verb_allowed(name)` - Return True when the merged view lets the loop route a CLI verb.
- `_repo_base` (function, `modules/auto_registry.py:451`) `def _repo_base()` - Return repository root without importing engine modules.
- `binary_available` (function, `modules/auto_registry.py:458`) `def binary_available(name)` - Return True when a command token can actually execute here.
- `missing_binary` (function, `modules/auto_registry.py:474`) `def missing_binary(command)` - Return the first binary a shell command needs but PATH lacks.
- `verb_gap` (function, `modules/auto_registry.py:486`) `def verb_gap(verb)` - Return a human reason when an automation verb cannot run, else ''.
- `verb_available` (function, `modules/auto_registry.py:498`) `def verb_available(verb)` - Return True when every binary an automation verb needs is installed.
- `service_tokens` (function, `modules/auto_registry.py:503`) `def service_tokens(service_text)` - Normalize a service asset value into matchable tokens.
- `_parse_trigger_lines` (function, `modules/auto_registry.py:514`) `def _parse_trigger_lines(lines, start)` - Parse a YAML trigger value starting at line index.
- `iter_addon_triggers` (function, `modules/auto_registry.py:545`) `def iter_addon_triggers()` - Scan enabled lazyaddons for (name, trigger tokens) pairs.
- `iter_tool_triggers` (function, `modules/auto_registry.py:581`) `def iter_tool_triggers()` - Scan active pwntomate tools for (toolname, trigger tokens) pairs.
- `addon_hits_for` (function, `modules/auto_registry.py:604`) `def addon_hits_for(service_text, limit)` - Rank addon/tool names matching one service value.
- `propose_addon_intents` (function, `modules/auto_registry.py:630`) `def propose_addon_intents(service_texts, target, limit)` - Propose addon intents for discovered services.
- `is_routable_command` (function, `modules/auto_registry.py:674`) `def is_routable_command(line)` - Return True when the loop executor must route via the shell.
- `verbs` (function, `modules/auto_registry.py:692`) `def verbs()` - Return every canonical automation verb name.
- `is_shell_verb` (function, `modules/auto_registry.py:697`) `def is_shell_verb(token)` - Return True when ``token`` names a loop-routable shell verb.
- `cover_all_enabled` (function, `modules/auto_registry.py:721`) `def cover_all_enabled()` - Return whether exploitation should exercise every vector, not just one.
- `build_command` (function, `modules/auto_registry.py:737`) `def build_command(verb, target)` - Build the shell command line for ``verb`` bound to ``target``.
- `verbs_for` (function, `modules/auto_registry.py:750`) `def verbs_for(text)` - Return enabled verbs whose keywords appear in the text.
- `propose_intents` (function, `modules/auto_registry.py:756`) `def propose_intents(goal, target, finding_texts)` - Propose ``auto <verb>`` intent summaries for planner candidates.
- `_atomic_steps` (function, `modules/auto_registry.py:781`) `def _atomic_steps(verb, text)` - Build a non-interactive atomic staging line from intent text.
- `_playbook_steps` (function, `modules/auto_registry.py:800`) `def _playbook_steps(text)` - Build an apt_playbook staging line from intent text.
- `_apt_chain_steps` (function, `modules/auto_registry.py:815`) `def _apt_chain_steps(embedded, target, strict)` - Build the one-line apt_chain invocation from intent fragments.
- `_chain_name_for_playbook` (function, `modules/auto_registry.py:844`) `def _chain_name_for_playbook(playbook)` - Map a playbook slug to its registered ray-chain file name.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 108
- Cross-boundary resolved imports (EXTRACTED): 132

## Connections

- [EXTRACTED] depends_on community 7 <-> 10 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/auto_registry.py.

## Risks

- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/atomic_exploit_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/reactive_engine.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/credential_vault.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `cli/engagement_hooks.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `core/hardening.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `modules/killchain.py` -> `modules/world_model.py` -> `modules/cli_auth.py` -> `core/config.py`
- [cycle] `utils.py` -> `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `utils.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_cli_bridge.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_installer.py` -> `core/config.py`
- [cycle] `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_installer.py` -> `core/config.py`

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `modules/reverse-shell.c`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/lazy_agent.py` -> `modules/loop_ai_bridge.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/engine_mediator.py` -> `modules/autonomous_exploit_engine.py` -> `modules/db.py` be broken with an interface?
- What would break if the most connected file in modules/selection changed?
- Should modules/selection be split, given cohesion 0.57?

## Sources

- `modules/auto_registry.py`
- `modules/campaign_blacklist.py`
- `modules/chain_match.py`
- `modules/reverse-shell.c`
- `modules/rootkit/rootkit.c`
- `modules/selection/__init__.py`
- `modules/selection/_phase_categories.py`
- `modules/selection/adversary.py`
- `modules/selection/atomic.py`
- `modules/selection/base.py`
- `modules/selection/bridge.py`
- `modules/selection/chain.py`
- `modules/selection/cred_spray.py`
- `modules/selection/edb.py`
- `modules/selection/intel.py`
- `modules/selection/lazyscript.py`
- `modules/selection/module.py`
- `modules/selection/parquet.py`
- `modules/selection/playbook.py`
- `modules/selection/poc.py`
- *... and 20 more*
