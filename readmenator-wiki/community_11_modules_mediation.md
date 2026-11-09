# modules/mediation

*Community 11 | 22 files | cohesion 0.44*

## Definition

This community groups 22 file(s) rooted at `modules/mediation` with dominant language py (cohesion 0.44). Central symbols: `AIExploitChainer`, `ActivityLogPort`, `AutoPivotEngine`, `AutonomousExploitEngine`, `BinaryAttacker`, `BinaryFinder`, `ChainMediator`, `DashboardEdge`. Core file: `tests/test_mediation.py` (52 symbols). Documented purpose: Autonomous exploitation and LOLBAS command set.  New chingon commands: auto_pwn, rich_tui, lolbas_list, lolbas_use, exploit_chain, stealth..

## Files

### `modules/mediation` (8 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/mediation/__init__.py` | py | utility | 0 | yes |
| `modules/mediation/chain_mediator.py` | py | utility | 8 | yes |
| `modules/mediation/contracts.py` | py | utility | 12 | yes |
| `modules/mediation/engine_mediator.py` | py | utility | 11 | yes |
| `modules/mediation/feedback_mediator.py` | py | utility | 3 | yes |
| `modules/mediation/hub.py` | py | utility | 8 | yes |
| `modules/mediation/intel_mediator.py` | py | utility | 9 | yes |

### `modules` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `modules/ai_exploit_chain.py` | py | utility | 11 | yes |
| `modules/auto_pivot.py` | py | utility | 23 | yes |
| `modules/autonomous_exploit_engine.py` | py | utility | 46 | yes |
| `modules/dashboard_engine.py` | py | utility | 16 | yes |
| `modules/lazy_intel.py` | py | utility | 14 | yes |
| `modules/lazy_orchestrator_feedback.py` | py | utility | 11 | yes |

### `contrib/legacy` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `contrib/legacy/lazypwn.py` | py | utility | 15 | no |
| `contrib/legacy/lazyvsftp.py` | py | utility | 3 | no |
| `contrib/legacy/sql.py` | py | utility | 3 | no |

### `tests` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_engine_mediator.py` | py | testing | 22 | yes |
| `tests/test_loop_supervision.py` | py | testing | 9 | yes |
| `tests/test_mediation.py` | py | testing | 52 | yes |

### `cli/commands` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `cli/commands/pwn.py` | py | utility | 8 | yes |

*... and 2 more files in this community.*


## Key Symbols

- `PwnCommandSet` (class, `cli/commands/pwn.py:28`) `class PwnCommandSet(LazyOwnCommandSet)` - Autonomous exploitation, LOLBAS, and advanced attack commands.
- `do_auto_pwn` (method, `cli/commands/pwn.py:35`) `def do_auto_pwn(self, line)` - Run the full autonomous exploitation chain against the target.
- `do_rich_tui` (method, `cli/commands/pwn.py:109`) `def do_rich_tui(self, line)` - Launch the Rich-based live dashboard TUI.
- `do_exploit_chain` (method, `cli/commands/pwn.py:158`) `def do_exploit_chain(self, line)` - AI-driven multi-step exploit chaining with fallback strategies.
- `do_lolbas_list` (method, `cli/commands/pwn.py:245`) `def do_lolbas_list(self, line)` - List available LOLBAS (Living Off The Land) techniques from plugins.
- `do_lolbas_use` (method, `cli/commands/pwn.py:302`) `def do_lolbas_use(self, line)` - Execute a specific LOLBAS technique.
- `do_stealth_on` (method, `cli/commands/pwn.py:394`) `def do_stealth_on(self, line)` - Enable stealth mode for subsequent operations.
- `do_stealth_off` (method, `cli/commands/pwn.py:422`) `def do_stealth_off(self, line)` - Disable stealth mode.
- `BinaryFinder` (class, `contrib/legacy/lazypwn.py:24`) `class BinaryFinder`
- `__init__` (method, `contrib/legacy/lazypwn.py:25`) `def __init__(self)`
- `find_suid_binaries` (method, `contrib/legacy/lazypwn.py:28`) `def find_suid_binaries(self)`
- `find_capabilities_binaries` (method, `contrib/legacy/lazypwn.py:36`) `def find_capabilities_binaries(self)`
- `find_executable_binaries` (method, `contrib/legacy/lazypwn.py:44`) `def find_executable_binaries(self)`
- `find_specific_name_binaries` (method, `contrib/legacy/lazypwn.py:52`) `def find_specific_name_binaries(self, names)`
- `process_output` (method, `contrib/legacy/lazypwn.py:61`) `def process_output(self, output)`
- `get_found_binaries` (method, `contrib/legacy/lazypwn.py:67`) `def get_found_binaries(self)`
- `BinaryAttacker` (class, `contrib/legacy/lazypwn.py:70`) `class BinaryAttacker`
- `__init__` (method, `contrib/legacy/lazypwn.py:71`) `def __init__(self, binary_path)`
- `analyze_with_ltrace` (method, `contrib/legacy/lazypwn.py:76`) `def analyze_with_ltrace(self)`
- `extract_strings` (method, `contrib/legacy/lazypwn.py:83`) `def extract_strings(self)`
- `prepare_attack` (method, `contrib/legacy/lazypwn.py:90`) `def prepare_attack(self)`
- `exploit_with_pwntools` (method, `contrib/legacy/lazypwn.py:170`) `def exploit_with_pwntools(self)`
- `main` (function, `contrib/legacy/lazypwn.py:181`) `def main()`
- `connect` (function, `contrib/legacy/lazyvsftp.py:7`) `def connect(host, port)`
- `exploit` (function, `contrib/legacy/lazyvsftp.py:16`) `def exploit(host, port)`
- `handle_backdoor` (function, `contrib/legacy/lazyvsftp.py:61`) `def handle_backdoor(s)`
- `def_handler` (function, `contrib/legacy/sql.py:8`) `def def_handler(sig, frame)`
- `getUnicode` (function, `contrib/legacy/sql.py:15`) `def getUnicode(sqli)`
- `makeRequest` (function, `contrib/legacy/sql.py:22`) `def makeRequest(sqli_modified)`
- `ExploitChainContext` (class, `modules/ai_exploit_chain.py:223`) `class ExploitChainContext` - Mutable context tracking state across chained exploit attempts.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 54
- Cross-boundary resolved imports (EXTRACTED): 115

## Connections

- [EXTRACTED] depends_on community 6 <-> 11 (strength 0.9): Extracted import edge crosses communities: cli/apt_chain_support.py imports modules/mediation/__init__.py.

## Risks

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
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/recommender.py` -> `modules/ai_fallback.py` -> `modules/llm_orchestrator.py`
- [cycle] `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `core/payload_schema.py`

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `contrib/legacy/lazypwn.py`)? What purpose do they serve?
- Can the cycle `core/config.py` -> `core/payload_schema.py` -> `modules/llm_factory.py` -> `modules/llm_orchestrator.py` -> `modules/lazy_engine.py` -> `modules/lazy_loop.py` -> `modules/loop/__init__.py` -> `modules/loop/worker_agentic.py` -> `modules/harness.py` -> `modules/orchestrator_config.py` -> `modules/auto_registry.py` -> `modules/lazy_orchestrator_feedback.py` -> `modules/lazy_intel.py` -> `modules/mediation/__init__.py` -> `modules/mediation/contracts.py` -> `modules/mediation/hub.py` -> `modules/mediation/telemetry_mediator.py` -> `modules/loop_ai_bridge.py` -> `skills/hive_mind.py` -> `skills/lazyown_groq_agents.py` -> `skills/lazyown_mcp.py` -> `modules/exploitgym_gym.py` -> `modules/redteam_gym.py` be broken with an interface?
- What would break if the most connected file in modules/mediation changed?
- Should modules/mediation be split, given cohesion 0.44?

## Sources

- `cli/commands/pwn.py`
- `contrib/legacy/lazypwn.py`
- `contrib/legacy/lazyvsftp.py`
- `contrib/legacy/sql.py`
- `modules/ai_exploit_chain.py`
- `modules/auto_pivot.py`
- `modules/autonomous_exploit_engine.py`
- `modules/dashboard_engine.py`
- `modules/lazy_intel.py`
- `modules/lazy_orchestrator_feedback.py`
- `modules/mediation/__init__.py`
- `modules/mediation/chain_mediator.py`
- `modules/mediation/contracts.py`
- `modules/mediation/engine_mediator.py`
- `modules/mediation/feedback_mediator.py`
- `modules/mediation/hub.py`
- `modules/mediation/intel_mediator.py`
- `modules/mediation/telemetry_mediator.py`
- `modules/rich_tui.py`
- `tests/test_engine_mediator.py`
- *... and 2 more*
